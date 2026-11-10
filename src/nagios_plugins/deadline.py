# SPDX-FileCopyrightText: 2026 Thomas Vincent
# SPDX-License-Identifier: Apache-2.0
"""Bound a whole plugin run so it reports UNKNOWN before the scheduler kills it.

Per-request timeouts do not cover everything a check can block on: name
resolution runs before a socket timeout applies, retries multiply the budget and
a child process can outlive the call that waits for it. :class:`Deadline` wraps
the run and, ``margin`` seconds after ``--timeout``, ends it:

* On POSIX in the main thread a ``SIGALRM`` timer raises :class:`PluginTimeout`,
  so ``finally`` blocks run and connections close. Async plugins bound their
  coroutine with the same instant through :func:`hard_remaining`, because an
  exception raised inside the event loop could land in an unrelated task.
* A watchdog thread is the fallback where no alarm is available (Windows, a
  non-main thread) and the backstop when the main thread cannot be interrupted,
  for example inside a blocking C call. It writes the UNKNOWN result itself and
  exits the process with status 3.

Child processes registered with :func:`track_child` are killed on either path.
"""

from __future__ import annotations

import asyncio
import contextvars
import os
import signal
import sys
import threading
import time
from collections.abc import Iterator
from contextlib import contextmanager, suppress
from types import FrameType, TracebackType
from typing import Any, Protocol

#: Seconds after ``--timeout`` at which the run is ended, so a plugin's own
#: request timeouts (which use ``--timeout``) report their specific error first.
DEADLINE_MARGIN = 1.0
#: Seconds the watchdog waits after the alarm before exiting the process itself.
WATCHDOG_GRACE = 1.0
#: Exit status written by the watchdog: Nagios UNKNOWN.
_UNKNOWN = 3


class PluginTimeout(BaseException):
    """The run deadline expired.

    Derives from ``BaseException`` so that ``except Exception`` in a check
    cannot swallow it and report a result after the deadline.
    """


class _Killable(Protocol):
    """A child process handle: :class:`subprocess.Popen` or an asyncio process."""

    def kill(self) -> None:
        """Send SIGKILL (or TerminateProcess on Windows)."""


# Re-entrant: the SIGALRM handler runs on the main thread, possibly while that
# thread is inside track_child, and must not deadlock on its own lock.
_children_lock = threading.RLock()
_children: set[_Killable] = set()
_active: contextvars.ContextVar[Deadline | None] = contextvars.ContextVar(
    "nagios_plugins_deadline", default=None
)


@contextmanager
def track_child(process: _Killable) -> Iterator[None]:
    """Kill ``process`` if the run deadline expires while it is registered."""
    with _children_lock:
        _children.add(process)
    try:
        yield
    finally:
        with _children_lock:
            _children.discard(process)


def _kill_children() -> None:
    """Kill every registered child; one that already exited is ignored."""
    with _children_lock:
        children = list(_children)
    for child in children:
        with suppress(ProcessLookupError, OSError, RuntimeError):
            child.kill()


def remaining_time() -> float | None:
    """Return the seconds left of the current run's ``--timeout``, or None outside a run.

    Retries and per-attempt timeouts use this budget so they end with the
    plugin's own error before the hard deadline.
    """
    deadline = _active.get()
    return None if deadline is None else max(0.0, deadline.soft_end - time.monotonic())


def hard_remaining() -> float | None:
    """Return the seconds until the current run is ended, or None outside a run."""
    deadline = _active.get()
    return None if deadline is None else max(0.0, deadline.hard_end - time.monotonic())


def _loop_running() -> bool:
    """Return whether an asyncio event loop is running in this thread."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return False
    return True


class Deadline:
    """Context manager that ends a plugin run ``margin`` seconds after ``timeout``.

    Args:
        timeout: The plugin's ``--timeout`` in seconds.
        timeout_output: The complete UNKNOWN result the watchdog writes to stdout.
        margin: Seconds after ``timeout`` at which the run is ended.
        grace: Seconds the watchdog waits after the alarm before exiting.
    """

    def __init__(
        self,
        timeout: float,
        timeout_output: str,
        *,
        margin: float | None = None,
        grace: float | None = None,
    ) -> None:
        """Prepare the deadline; nothing is armed until the context is entered."""
        self.timeout = timeout
        self.margin = DEADLINE_MARGIN if margin is None else margin
        self.grace = WATCHDOG_GRACE if grace is None else grace
        self._timeout_output = timeout_output
        self._lock = threading.Lock()
        self._finished = False
        self._closing = False
        self._watchdog: threading.Timer | None = None
        self._previous_handler: Any = None
        self._alarm = False
        self._token: contextvars.Token[Deadline | None] | None = None
        self.soft_end = self.hard_end = 0.0

    @staticmethod
    def _alarm_available() -> bool:
        """SIGALRM handlers can only be installed from the main thread on POSIX."""
        return (
            hasattr(signal, "setitimer") and threading.current_thread() is threading.main_thread()
        )

    def __enter__(self) -> Deadline:
        """Arm the alarm (when available) and the watchdog thread."""
        now = time.monotonic()
        self.soft_end = now + self.timeout
        self.hard_end = self.soft_end + self.margin
        watchdog_delay = self.timeout + self.margin
        if self._alarm_available():
            self._previous_handler = signal.signal(signal.SIGALRM, self._on_alarm)
            signal.setitimer(signal.ITIMER_REAL, self.timeout + self.margin)
            self._alarm = True
            watchdog_delay += self.grace
        self._watchdog = threading.Timer(watchdog_delay, self._on_watchdog)
        self._watchdog.daemon = True
        self._watchdog.start()
        self._token = _active.set(self)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Disarm both mechanisms; afterwards the watchdog can no longer exit.

        An alarm that fires before ``_closing`` is set raises here, and the
        ``finally`` still restores the handler and stops the watchdog.
        """
        try:
            self._closing = True
            if self._alarm:
                signal.setitimer(signal.ITIMER_REAL, 0)
        finally:
            with self._lock:
                self._finished = True
            if self._watchdog is not None:
                self._watchdog.cancel()
                self._watchdog.join()
            if self._alarm:
                signal.signal(signal.SIGALRM, self._previous_handler)
            if self._token is not None:
                _active.reset(self._token)

    def _on_alarm(self, signum: int, frame: FrameType | None) -> None:
        """Kill children, then interrupt synchronous code with PluginTimeout.

        While an event loop runs, the coroutine's own bound (see
        :func:`hard_remaining`) cancels it instead, so nothing is raised here.
        """
        if self._closing:
            return
        _kill_children()
        if not _loop_running():
            raise PluginTimeout

    def _on_watchdog(self) -> None:
        """Write the UNKNOWN result and exit unless the run has already finished."""
        with self._lock:
            if self._finished:
                return
            _kill_children()
            # The run is abandoned: no other stdout writer exists while the lock is held.
            with suppress(Exception):
                sys.stdout.write(self._timeout_output + "\n")
                sys.stdout.flush()
            with suppress(Exception):
                sys.stderr.flush()
            os._exit(_UNKNOWN)

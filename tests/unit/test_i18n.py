# SPDX-FileCopyrightText: 2026 Thomas Vincent <thomasvincent@gmail.com>
# SPDX-License-Identifier: Apache-2.0
"""Tests for 20-locale i18n support in nagios-plugins-collection."""

from __future__ import annotations

import argparse
import re
from collections.abc import Iterator

import pytest

from nagios_plugins.base import CheckResult, NagiosPlugin, Status
from nagios_plugins.i18n import (
    DEFAULT_LOCALE,
    SUPPORTED_LOCALES,
    detect_locale,
    get_locale,
    load_catalog,
    normalize_locale,
    set_locale,
    t,
)

PLACEHOLDER_RE = re.compile(r"\{[a-zA-Z0-9_]+\}")


@pytest.fixture(autouse=True)
def _reset_locale(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    for var in ("LC_ALL", "LC_MESSAGES", "LANG"):
        monkeypatch.delenv(var, raising=False)
    set_locale(None)
    yield
    set_locale(None)


def test_all_20_locales_load_with_key_and_placeholder_parity() -> None:
    """Every Tier 1 locale loads cleanly with 100% key and placeholder parity."""
    assert len(SUPPORTED_LOCALES) == 20
    en = load_catalog(DEFAULT_LOCALE)
    assert len(en) > 0
    for locale in SUPPORTED_LOCALES:
        catalog = load_catalog(locale)
        assert set(catalog.keys()) == set(en.keys()), locale
        for key, en_val in en.items():
            assert catalog[key].strip(), (locale, key)
            assert sorted(PLACEHOLDER_RE.findall(catalog[key])) == sorted(
                PLACEHOLDER_RE.findall(en_val)
            ), (locale, key)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        (None, "en"),
        ("", "en"),
        ("C", "en"),
        ("POSIX", "en"),
        ("de_DE.UTF-8", "de"),
        ("zh_TW", "zh-TW"),
        ("zh_HK.UTF-8", "zh-TW"),
        ("zh-TW-u-nu-hanidec", "zh-TW"),
        ("zh-HK-u-nu-hanidec", "zh-TW"),
        ("zh-Hant-TW", "zh-TW"),
        ("zh-Hans-TW", "zh-CN"),
        ("zh_CN.UTF-8", "zh-CN"),
        ("zh", "zh-CN"),
        ("pt_BR.UTF-8", "pt-BR"),
        ("pt_PT", "pt-BR"),
        ("x-private", "en"),
        ("xx_YY", "en"),
    ],
)
def test_normalize_locale(raw: str | None, expected: str) -> None:
    """POSIX and BCP 47 locale strings map to canonical supported locales."""
    assert normalize_locale(raw) == expected


def test_env_precedence_and_override(monkeypatch: pytest.MonkeyPatch) -> None:
    """LC_ALL > LC_MESSAGES > LANG > en precedence and runtime overrides work."""
    assert detect_locale() == "en"
    monkeypatch.setenv("LANG", "fr_FR.UTF-8")
    assert detect_locale() == "fr"
    monkeypatch.setenv("LC_MESSAGES", "pl_PL.UTF-8")
    assert detect_locale() == "pl"
    monkeypatch.setenv("LC_ALL", "sv_SE.UTF-8")
    assert detect_locale() == "sv"
    assert detect_locale("tr") == "tr"

    assert set_locale("vi") == "vi"
    assert get_locale() == "vi"
    assert set_locale(None) == "sv"
    assert get_locale() == "sv"


def test_plugin_lang_preserves_nagios_status_prefix(capsys: pytest.CaptureFixture[str]) -> None:
    """Status prefixes remain English Nagios tokens while message body localizes."""

    class BoomPlugin(NagiosPlugin):
        """Sample plugin that raises an unhandled exception."""

        def check(self, args: argparse.Namespace) -> CheckResult:
            raise RuntimeError("boom")

    assert t("error.unhandled_exception", error="boom") == "Unhandled exception: boom"
    assert t("unknown.key") == "unknown.key"

    code = BoomPlugin().run(["--lang", "de"])
    out = capsys.readouterr().out
    assert code == Status.UNKNOWN.value
    assert out.startswith("UNKNOWN - ")
    assert t("error.unhandled_exception", locale="de", error="boom") in out

    with pytest.raises(SystemExit) as help_exc:
        BoomPlugin().run(["--lang", "de", "--help"])
    assert help_exc.value.code == 0
    help_out = " ".join(capsys.readouterr().out.split())
    assert " ".join(t("cli.lang_help", locale="de").split()) in help_out

    with pytest.raises(SystemExit) as err_exc:
        BoomPlugin().run(["--lang", "de", "--timeout", "0"])
    assert err_exc.value.code == Status.UNKNOWN.value
    err_out = capsys.readouterr().out
    assert err_out.startswith("UNKNOWN - ")
    assert t("error.min_one_second", locale="de", value="'0'") in err_out

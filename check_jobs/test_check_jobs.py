import pytest
import check_jobs

def test_help():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        check_jobs.help()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 3

def test_main():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        check_jobs.main([])
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 3

def test_main_success():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        check_jobs.main(["-url=https://www.example.com/status"])
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0

def test_main_warning():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        check_jobs.main(["-url=https://www.example.com/warning"])
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1

def test_main_unknown():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        check_jobs.main(["-url=https://www.example.com/invalid"])
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 3

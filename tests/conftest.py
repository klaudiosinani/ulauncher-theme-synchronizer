import pytest

from tests.support.gi import install_gi_stubs
from tests.support.ulauncher import install_ulauncher_stubs


def pytest_sessionstart(session: pytest.Session) -> None:
    install_ulauncher_stubs()
    install_gi_stubs()

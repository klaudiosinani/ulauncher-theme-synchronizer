from dataclasses import dataclass

import pytest

from src.orchestration.launcher.ulauncher_commands_provider import UlauncherCommandsProvider


@dataclass
class UnderTestContext:
    under_test: UlauncherCommandsProvider


@pytest.fixture
def under_test_context() -> UnderTestContext:
    under_test = UlauncherCommandsProvider()
    return UnderTestContext(under_test)


class TestUlauncherCommandsProvider:
    def test_given_default_constructor_when_get_pgrep_then_returns_pgrep_command(
        self, under_test_context: UnderTestContext
    ) -> None:
        result = under_test_context.under_test.get_pgrep()

        assert result == ["pgrep", "-x", "ulauncher"]

    def test_given_default_constructor_when_get_pidof_then_returns_pidof_command(
        self, under_test_context: UnderTestContext
    ) -> None:
        result = under_test_context.under_test.get_pidof()

        assert result == ["pidof", "ulauncher"]

    def test_given_default_constructor_when_get_start_then_returns_start_command(
        self, under_test_context: UnderTestContext
    ) -> None:
        result = under_test_context.under_test.get_start()

        assert result == ["bash", "-c", "sleep 1 && ulauncher --hide-window"]

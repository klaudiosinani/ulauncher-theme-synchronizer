from dataclasses import dataclass
from unittest.mock import MagicMock

import pytest

from src.feature.synchronization.mode.mode import Mode
from src.feature.synchronization.theme.theme_activation_service import ThemeActivationService
from src.feature.synchronization.theme.theme_resolution_service import ThemeResolutionService
from src.orchestration.launcher.ulauncher_service import UlauncherService


@dataclass
class UnderTestContext:
    under_test: ThemeActivationService
    ulauncher_service: MagicMock
    theme_resolution_service: MagicMock


@pytest.fixture
def under_test_context() -> UnderTestContext:
    ulauncher_service = MagicMock(spec=UlauncherService)
    theme_resolution_service = MagicMock(spec=ThemeResolutionService)
    under_test = ThemeActivationService(ulauncher_service, theme_resolution_service)

    return UnderTestContext(under_test, ulauncher_service, theme_resolution_service)


class TestThemeActivationService:
    def test_given_mode_when_activate_then_resolves_theme_for_mode(self, under_test_context: UnderTestContext) -> None:
        # given
        mode = MagicMock(spec=Mode)
        under_test_context.theme_resolution_service.resolve.return_value = "dark"

        # when
        under_test_context.under_test.activate(mode)

        # then
        under_test_context.theme_resolution_service.resolve.assert_called_once_with(mode)

    def test_given_resolved_theme_when_activate_then_activates_theme_in_ulauncher(
        self, under_test_context: UnderTestContext
    ) -> None:
        # given
        mode = MagicMock(spec=Mode)
        under_test_context.theme_resolution_service.resolve.return_value = "dark"

        # when
        under_test_context.under_test.activate(mode)

        # then
        under_test_context.ulauncher_service.activate_theme.assert_called_once_with("dark")

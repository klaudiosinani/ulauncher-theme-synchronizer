from dataclasses import dataclass
from unittest.mock import MagicMock, patch

import pytest

from src.orchestration.launcher.ulauncher_process_service import UlauncherProcessService
from src.orchestration.launcher.ulauncher_service import UlauncherService
from src.orchestration.launcher.ulauncher_settings_service import UlauncherSettingsService


@dataclass
class UnderTestContext:
    under_test: UlauncherService
    ulauncher_settings_service: MagicMock
    ulauncher_process_service: MagicMock


@pytest.fixture
def under_test_context() -> UnderTestContext:
    ulauncher_settings_service = MagicMock(spec=UlauncherSettingsService)
    ulauncher_process_service = MagicMock(spec=UlauncherProcessService)
    under_test = UlauncherService(ulauncher_settings_service, ulauncher_process_service)

    return UnderTestContext(under_test, ulauncher_settings_service, ulauncher_process_service)


class TestUlauncherService:
    def test_given_theme_already_active_when_activate_theme_then_does_not_persist_or_restart(
        self, under_test_context: UnderTestContext
    ) -> None:
        # given
        under_test_context.ulauncher_settings_service.retrieve_theme.return_value = "dark"

        # when
        under_test_context.under_test.activate_theme("dark")

        # then
        under_test_context.ulauncher_settings_service.persist_theme.assert_not_called()
        under_test_context.ulauncher_process_service.restart.assert_not_called()

    def test_given_different_theme_active_when_activate_theme_then_persists_new_theme(
        self, under_test_context: UnderTestContext
    ) -> None:
        # given
        under_test_context.ulauncher_settings_service.retrieve_theme.return_value = "light"

        # when
        under_test_context.under_test.activate_theme("dark")

        # then
        under_test_context.ulauncher_settings_service.persist_theme.assert_called_once_with("dark")

    def test_given_different_theme_active_when_activate_theme_then_restarts_process(
        self, under_test_context: UnderTestContext
    ) -> None:
        # given
        under_test_context.ulauncher_settings_service.retrieve_theme.return_value = "light"

        with patch("src.orchestration.launcher.ulauncher_service.logger.info") as logger:
            # when
            under_test_context.under_test.activate_theme("dark")

        # then
        under_test_context.ulauncher_process_service.restart.assert_called_once_with()
        logger.assert_called_once_with("Activated Ulauncher theme: %s", "dark")

    def test_given_theme_already_active_when_activate_theme_then_exists_and_logs_already_active_theme(
        self, under_test_context: UnderTestContext
    ) -> None:
        # given
        under_test_context.ulauncher_settings_service.retrieve_theme.return_value = "dark-theme"

        with patch("src.orchestration.launcher.ulauncher_service.logger.info") as info_mock:
            # when
            under_test_context.under_test.activate_theme("dark-theme")

        # then
        info_mock.assert_called_once_with("Ulauncher theme already active: %s", "dark-theme")

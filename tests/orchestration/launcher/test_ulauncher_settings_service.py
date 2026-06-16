from dataclasses import dataclass
from unittest.mock import MagicMock

import pytest

from src.orchestration.launcher.ulauncher_settings_repository import UlauncherSettingsRepository
from src.orchestration.launcher.ulauncher_settings_service import THEME_KEY, UlauncherSettingsService


@dataclass
class UnderTestContext:
    under_test: UlauncherSettingsService
    ulauncher_settings_repository: MagicMock


@pytest.fixture
def under_test_context() -> UnderTestContext:
    ulauncher_settings_repository = MagicMock(spec=UlauncherSettingsRepository)

    under_test = UlauncherSettingsService(ulauncher_settings_repository)

    return UnderTestContext(under_test, ulauncher_settings_repository)


class TestUlauncherSettingsService:
    def test_given_theme_present_when_retrieve_theme_then_returns_theme(
        self, under_test_context: UnderTestContext
    ) -> None:
        under_test_context.ulauncher_settings_repository.retrieve.return_value = {THEME_KEY: "dark-theme"}

        result = under_test_context.under_test.retrieve_theme()

        assert result == "dark-theme"
        under_test_context.ulauncher_settings_repository.retrieve.assert_called_once_with()

    def test_given_theme_missing_when_retrieve_theme_then_raises_key_error(
        self, under_test_context: UnderTestContext
    ) -> None:
        under_test_context.ulauncher_settings_repository.retrieve.return_value = {}

        with pytest.raises(KeyError, match=r"Property 'theme-name' not found in Ulauncher settings"):
            under_test_context.under_test.retrieve_theme()

        under_test_context.ulauncher_settings_repository.retrieve.assert_called_once_with()

    def test_given_theme_when_persist_theme_then_updates_settings_and_persists_them(
        self, under_test_context: UnderTestContext
    ) -> None:
        settings = {"show-recent-apps": "5", THEME_KEY: "light"}
        under_test_context.ulauncher_settings_repository.retrieve.return_value = settings

        under_test_context.under_test.persist_theme("dark")

        under_test_context.ulauncher_settings_repository.retrieve.assert_called_once_with()
        under_test_context.ulauncher_settings_repository.persist.assert_called_once_with(
            {"show-recent-apps": "5", THEME_KEY: "dark"}
        )

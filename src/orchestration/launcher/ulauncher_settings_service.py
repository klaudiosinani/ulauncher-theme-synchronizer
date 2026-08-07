from typing import Final

from src.orchestration.launcher.ulauncher_settings_repository import UlauncherSettingsRepository
from src.orchestration.log import logging_service

logger = logging_service.get(__name__)

THEME_KEY: Final = "theme-name"


class UlauncherSettingsService:
    def __init__(self, ulauncher_settings_repository: UlauncherSettingsRepository) -> None:
        self._ulauncher_settings_repository = ulauncher_settings_repository

    def retrieve_theme(self) -> str:
        return self._retrieve_property(THEME_KEY)

    def persist_theme(self, theme: str) -> None:
        self._persist_property(THEME_KEY, theme)

    def _retrieve_property(self, key: str) -> str:
        settings = self._ulauncher_settings_repository.retrieve()

        if key not in settings:
            raise KeyError(f"Property '{key}' not found in Ulauncher settings")

        value = settings[key]

        if not isinstance(value, str):
            raise TypeError(f"Property '{key}' in Ulauncher settings is not a string: {type(value).__name__}")

        return value

    def _persist_property(self, key: str, value: str) -> None:
        settings = self._ulauncher_settings_repository.retrieve()
        settings[key] = value
        self._ulauncher_settings_repository.persist(settings)

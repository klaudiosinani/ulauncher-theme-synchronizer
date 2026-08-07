from src.orchestration.launcher.ulauncher_process_service import UlauncherProcessService
from src.orchestration.launcher.ulauncher_settings_service import UlauncherSettingsService
from src.orchestration.log import logging_service

logger = logging_service.get(__name__)


class UlauncherService:
    def __init__(
        self, ulauncher_settings_service: UlauncherSettingsService, ulauncher_process_service: UlauncherProcessService
    ) -> None:
        self._ulauncher_settings_service = ulauncher_settings_service
        self._ulauncher_process_service = ulauncher_process_service

    def activate_theme(self, theme: str) -> None:
        if self._is_theme_already_active(theme):
            logger.info("Ulauncher theme already active: %s", theme)
            return

        self._ulauncher_settings_service.persist_theme(theme)

        if not self._ulauncher_process_service.restart():
            logger.warning("Persisted Ulauncher theme but failed to restart: %s", theme)
            return

        logger.info("Activated Ulauncher theme: %s", theme)

    def _is_theme_already_active(self, theme: str) -> bool:
        return self._ulauncher_settings_service.retrieve_theme() == theme

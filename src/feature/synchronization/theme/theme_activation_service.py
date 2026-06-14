from src.feature.synchronization.mode.mode import Mode
from src.feature.synchronization.theme.theme_resolution_service import ThemeResolutionService
from src.orchestration.launcher.ulauncher_service import UlauncherService


class ThemeActivationService:
    def __init__(
        self,
        ulauncher_service: UlauncherService,
        theme_resolution_service: ThemeResolutionService,
    ) -> None:
        self._ulauncher_service = ulauncher_service
        self._theme_resolution_service = theme_resolution_service

    def activate(self, mode: Mode) -> None:
        theme_name = self._theme_resolution_service.resolve(mode)
        self._ulauncher_service.activate_theme(theme_name)

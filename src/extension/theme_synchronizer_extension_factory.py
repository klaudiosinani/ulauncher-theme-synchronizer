from gi.repository import Gio
from ulauncher.api.shared.event import (
    KeywordQueryEvent,
    PreferencesEvent,
    SystemExitEvent,
)

from src.extension.theme_synchronizer_extension import ThemeSynchronizerExtension
from src.feature.status.display_status_event_handler import DisplayStatusEventHandler
from src.feature.status.keyword_query_event_listener import KeywordQueryEventListener
from src.feature.synchronization.lifecycle.preferences_event_listener import PreferencesEventListener
from src.feature.synchronization.lifecycle.system_exit_event_listener import SystemExitEventListener
from src.feature.synchronization.mode.gio_settings_factory import GioSettingsFactory
from src.feature.synchronization.mode.gnome_desktop_settings import GnomeDesktopSettings
from src.feature.synchronization.mode.mode_event_handler import ModeEventHandler
from src.feature.synchronization.mode.mode_parser import ModeParser
from src.feature.synchronization.mode.mode_retrieval_service import ModeRetrievalService
from src.feature.synchronization.theme.theme_activation_service import ThemeActivationService
from src.feature.synchronization.theme.theme_parser import ThemeParser
from src.feature.synchronization.theme.theme_resolution_service import ThemeResolutionService
from src.feature.synchronization.watcher.operating_system_mode_watcher import OperatingSystemModeWatcher
from src.orchestration.file.atomic_file_service import AtomicFileService
from src.orchestration.launcher.ulauncher_commands_provider import UlauncherCommandsProvider
from src.orchestration.launcher.ulauncher_process_service import UlauncherProcessService
from src.orchestration.launcher.ulauncher_service import UlauncherService
from src.orchestration.launcher.ulauncher_settings_repository import UlauncherSettingsRepository
from src.orchestration.launcher.ulauncher_settings_service import UlauncherSettingsService
from src.orchestration.path.path_retrieval_service import PathRetrievalService


class ThemeSynchronizerExtensionFactory:
    def create(self) -> ThemeSynchronizerExtension:
        theme_synchronizer_extension = ThemeSynchronizerExtension()

        gio_settings = self._compose_gio_settings()
        mode_retrieval_service = self._compose_mode_retrieval_service()
        ulauncher_settings_service = self._compose_ulauncher_settings_service()

        display_status_event_handler = DisplayStatusEventHandler(
            mode_retrieval_service, ulauncher_settings_service, gio_settings
        )

        operating_system_mode_watcher = self._compose_operating_system_mode_watcher(
            mode_retrieval_service, ulauncher_settings_service, gio_settings, theme_synchronizer_extension
        )

        keyword_query_event_listener = KeywordQueryEventListener(display_status_event_handler)
        preferences_event_listener = PreferencesEventListener(operating_system_mode_watcher)
        system_exit_event_listener = SystemExitEventListener(operating_system_mode_watcher)

        theme_synchronizer_extension.subscribe(KeywordQueryEvent, keyword_query_event_listener)
        theme_synchronizer_extension.subscribe(PreferencesEvent, preferences_event_listener)
        theme_synchronizer_extension.subscribe(SystemExitEvent, system_exit_event_listener)

        return theme_synchronizer_extension

    def _compose_gio_settings(self) -> Gio.Settings:
        gio_settings_factory = GioSettingsFactory()
        return gio_settings_factory.create()

    def _compose_mode_retrieval_service(self) -> ModeRetrievalService:
        mode_parser = ModeParser()
        return ModeRetrievalService(mode_parser)

    def _compose_ulauncher_settings_service(self) -> UlauncherSettingsService:
        path_retrieval_service = PathRetrievalService()
        atomic_file_service = AtomicFileService()
        ulauncher_settings_repository = UlauncherSettingsRepository(path_retrieval_service, atomic_file_service)
        return UlauncherSettingsService(ulauncher_settings_repository)

    def _compose_operating_system_mode_watcher(
        self,
        mode_retrieval_service: ModeRetrievalService,
        ulauncher_settings_service: UlauncherSettingsService,
        gio_settings: Gio.Settings,
        theme_synchronizer_extension: ThemeSynchronizerExtension,
    ) -> OperatingSystemModeWatcher:
        ulauncher_commands_provider = UlauncherCommandsProvider()
        ulauncher_process_service = UlauncherProcessService(ulauncher_commands_provider)
        ulauncher_service = UlauncherService(ulauncher_settings_service, ulauncher_process_service)

        theme_parser = ThemeParser()
        theme_resolution_service = ThemeResolutionService(theme_parser, theme_synchronizer_extension)

        theme_activation_service = ThemeActivationService(ulauncher_service, theme_resolution_service)

        mode_event_handler = ModeEventHandler(mode_retrieval_service, theme_activation_service)

        return OperatingSystemModeWatcher(
            gio_settings,
            mode_event_handler,
            GnomeDesktopSettings.COLOR_SCHEME_KEY,
        )

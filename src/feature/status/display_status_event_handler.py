from gi.repository import Gio
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

from src.feature.status.keyword_query_event_handler import KeywordQueryEventHandler
from src.feature.synchronization.mode.mode_retrieval_service import ModeRetrievalService
from src.orchestration.launcher.ulauncher_settings_service import UlauncherSettingsService


class DisplayStatusEventHandler(KeywordQueryEventHandler):
    def __init__(
        self,
        mode_retrieval_service: ModeRetrievalService,
        ulauncher_settings_service: UlauncherSettingsService,
        gio_settings: Gio.Settings,
    ) -> None:
        self._mode_retrieval_service = mode_retrieval_service
        self._ulauncher_settings_service = ulauncher_settings_service
        self._gio_settings = gio_settings

    def handle(self, extension: Extension) -> RenderResultListAction:
        active_mode = self._mode_retrieval_service.retrieve(self._gio_settings)
        active_theme = self._ulauncher_settings_service.retrieve_theme()

        return RenderResultListAction(
            [
                ExtensionResultItem(
                    icon="images/icon.png",
                    name="Theme Synchronizer",
                    description=f"Active mode: {active_mode.value} — Selected theme: {active_theme}",
                    on_enter=HideWindowAction(),
                )
            ]
        )

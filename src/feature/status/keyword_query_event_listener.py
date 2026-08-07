from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.event import KeywordQueryEvent

from src.feature.status.display_status_event_handler import DisplayStatusEventHandler


class KeywordQueryEventListener(EventListener):
    def __init__(self, display_status_event_handler: DisplayStatusEventHandler) -> None:
        self._display_status_event_handler = display_status_event_handler

    def on_event(self, event: KeywordQueryEvent, extension: Extension) -> RenderResultListAction:
        return self._display_status_event_handler.handle()

from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.event import BaseEvent

from src.feature.synchronization.watcher.operating_system_mode_watcher import OperatingSystemModeWatcher


class SystemExitEventListener(EventListener):
    def __init__(self, operating_system_mode_watcher: OperatingSystemModeWatcher) -> None:
        self._operating_system_mode_watcher = operating_system_mode_watcher

    def on_event(self, event: BaseEvent, extension: Extension) -> None:
        self._operating_system_mode_watcher.stop()

from gi.repository import Gio, GLib

from src.feature.synchronization.mode.gnome_desktop_settings import GnomeDesktopSettings
from src.feature.synchronization.mode.mode_event_handler import ModeEventHandler


class ModeEventListener:
    def __init__(self, gio_settings: Gio.Settings, mode_event_handler: ModeEventHandler) -> None:
        self._gio_settings = gio_settings
        self._mode_event_handler = mode_event_handler

    def listen(self) -> None:
        self._gio_settings.connect(f"changed::{GnomeDesktopSettings.COLOR_SCHEME_KEY}", self._mode_event_handler.handle)

        main_loop = GLib.MainLoop()
        main_loop.run()

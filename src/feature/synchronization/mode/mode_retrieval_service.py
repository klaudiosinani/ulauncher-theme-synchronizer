from gi.repository import Gio

from src.feature.synchronization.mode.gnome_desktop_settings import GnomeDesktopSettings
from src.feature.synchronization.mode.mode import Mode
from src.feature.synchronization.mode.mode_parser import ModeParser


class ModeRetrievalService:
    def __init__(self, mode_parser: ModeParser) -> None:
        self._mode_parser = mode_parser

    def retrieve(self, gio_desktop_settings: Gio.Settings) -> Mode:
        mode = gio_desktop_settings.get_string(GnomeDesktopSettings.COLOR_SCHEME_KEY)
        return self._mode_parser.parse(mode)

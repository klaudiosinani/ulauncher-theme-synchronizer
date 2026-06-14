from gi.repository import Gio

from src.feature.synchronization.mode.gnome_desktop_settings import GnomeDesktopSettings


class GioSettingsFactory:
    def create(self) -> Gio.Settings:
        return Gio.Settings.new(GnomeDesktopSettings.INTERFACE_SCHEMA)

import types
from unittest.mock import MagicMock

from tests.support.module_registry import package, register


class GioSettingsStub:
    def connect(self, detailed_signal: str, callback):
        return 1

    def disconnect(self, detailed_signal: str):
        return 1

    @staticmethod
    def new(schema_id: str):
        return MagicMock(name=f"GioSettings({schema_id})", spec=GioSettingsStub)


class GLibMainLoopStub:
    def run(self) -> None:
        pass

    def quit(self) -> None:
        pass


def install_gi_stubs() -> None:
    gi_module = package("gi")
    repository_module = package("gi.repository")
    overrides_module = package("gi.overrides")

    gio_module = types.ModuleType("gi.repository.Gio")
    glib_module = types.ModuleType("gi.repository.GLib")
    gio_overrides_module = types.ModuleType("gi.overrides.Gio")

    gio_module.Settings = GioSettingsStub
    glib_module.MainLoop = GLibMainLoopStub
    gio_overrides_module.Gio = gio_module

    gi_module.repository = repository_module
    gi_module.overrides = overrides_module
    repository_module.Gio = gio_module
    repository_module.GLib = glib_module
    overrides_module.Gio = gio_overrides_module

    register(
        {
            "gi": gi_module,
            "gi.repository": repository_module,
            "gi.repository.Gio": gio_module,
            "gi.repository.GLib": glib_module,
            "gi.overrides": overrides_module,
            "gi.overrides.Gio": gio_overrides_module,
        }
    )

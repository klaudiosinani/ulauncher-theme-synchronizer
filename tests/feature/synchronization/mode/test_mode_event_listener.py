from dataclasses import dataclass
from unittest.mock import MagicMock, patch

import pytest
from gi.repository import Gio, GLib

from src.feature.synchronization.mode.gnome_desktop_settings import GnomeDesktopSettings
from src.feature.synchronization.mode.mode_event_handler import ModeEventHandler
from src.feature.synchronization.mode.mode_event_listener import ModeEventListener


@dataclass
class UnderTestContext:
    under_test: ModeEventListener
    gio_settings: MagicMock
    mode_event_handler: MagicMock


@pytest.fixture
def under_test_context() -> UnderTestContext:
    gio_settings = MagicMock(spec=Gio.Settings)
    mode_event_handler = MagicMock(spec=ModeEventHandler)

    under_test = ModeEventListener(gio_settings, mode_event_handler)

    return UnderTestContext(under_test, gio_settings, mode_event_handler)


class TestModeEventListener:
    def test_given_gio_settings_and_mode_event_handler_when_listen_then_connects_color_scheme_signal_and_runs_main_loop(
        self, under_test_context: UnderTestContext
    ) -> None:
        # given
        main_loop = MagicMock(spec=GLib.MainLoop)

        with patch(
            "src.feature.synchronization.mode.mode_event_listener.GLib.MainLoop", return_value=main_loop
        ) as main_loop_class:
            # when
            under_test_context.under_test.listen()

        # then
        under_test_context.gio_settings.connect.assert_called_once_with(
            f"changed::{GnomeDesktopSettings.COLOR_SCHEME_KEY}",
            under_test_context.mode_event_handler.handle,
        )
        main_loop_class.assert_called_once_with()
        main_loop.run.assert_called_once_with()

from collections.abc import Generator
from dataclasses import dataclass
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from gi.repository import Gio, GLib

from src.feature.synchronization.mode.mode_event_handler import ModeEventHandler
from src.feature.synchronization.watcher.operating_system_mode_watcher import OperatingSystemModeWatcher


@dataclass
class UnderTestContext:
    under_test: OperatingSystemModeWatcher
    gio_settings: MagicMock
    mode_event_handler: MagicMock


@dataclass
class RuntimeContext:
    main_loop: MagicMock
    thread: MagicMock
    main_loop_class: MagicMock
    thread_class: MagicMock


@pytest.fixture
def under_test_context() -> UnderTestContext:
    gio_settings = MagicMock(spec=Gio.Settings)
    mode_event_handler = MagicMock(spec=ModeEventHandler)

    under_test = OperatingSystemModeWatcher(gio_settings, mode_event_handler, "color-scheme")

    return UnderTestContext(under_test, gio_settings, mode_event_handler)


@pytest.fixture
def runtime_context() -> Generator[RuntimeContext, Any, None]:
    main_loop = MagicMock(spec=GLib.MainLoop)
    thread = MagicMock()

    with (
        patch(
            "src.feature.synchronization.watcher.operating_system_mode_watcher.GLib.MainLoop", return_value=main_loop
        ) as main_loop_class,
        patch(
            "src.feature.synchronization.watcher.operating_system_mode_watcher.threading.Thread", return_value=thread
        ) as thread_class,
    ):
        yield RuntimeContext(main_loop, thread, main_loop_class, thread_class)


class TestOperatingSystemModeWatcher:
    def test_given_not_started_when_start_then_connects_signal_creates_main_loop_starts_thread_and_logs_started(
        self, under_test_context: UnderTestContext, runtime_context: RuntimeContext
    ) -> None:
        # given
        under_test_context.gio_settings.connect.return_value = 123

        with patch("src.feature.synchronization.watcher.operating_system_mode_watcher.logger.info") as logger:
            # when
            under_test_context.under_test.start()

        # then
        under_test_context.gio_settings.connect.assert_called_once_with(
            "changed::color-scheme", under_test_context.mode_event_handler.handle
        )
        runtime_context.main_loop_class.assert_called_once_with()
        runtime_context.thread_class.assert_called_once_with(
            target=under_test_context.under_test._execute_loop, daemon=True
        )
        runtime_context.thread.start.assert_called_once_with()
        logger.assert_called_once_with("Operating System mode watcher started")

    def test_given_already_started_when_start_then_logs_and_does_not_start_again(
        self, under_test_context: UnderTestContext, runtime_context: RuntimeContext
    ) -> None:
        # given
        under_test_context.gio_settings.connect.return_value = 123
        under_test_context.under_test.start()

        with patch("src.feature.synchronization.watcher.operating_system_mode_watcher.logger.debug") as logger:
            # when
            under_test_context.under_test.start()

        # then
        under_test_context.gio_settings.connect.assert_called_once_with(
            "changed::color-scheme", under_test_context.mode_event_handler.handle
        )
        runtime_context.thread.start.assert_called_once_with()
        logger.assert_called_once_with("Operating System mode watcher already started")

    def test_given_started_when_stop_then_disconnects_handler_quits_loop_clears_state_and_logs_stopped(
        self, under_test_context: UnderTestContext, runtime_context: RuntimeContext
    ) -> None:
        # given
        under_test_context.gio_settings.connect.return_value = 123
        under_test_context.under_test.start()

        with patch("src.feature.synchronization.watcher.operating_system_mode_watcher.logger.info") as logger:
            # when
            under_test_context.under_test.stop()

        # then
        under_test_context.gio_settings.disconnect.assert_called_once_with(123)
        runtime_context.main_loop.quit.assert_called_once_with()
        assert under_test_context.under_test._handler_id is None
        assert under_test_context.under_test._glib_loop is None
        assert under_test_context.under_test._thread is None
        assert under_test_context.under_test._is_started is False
        logger.assert_called_once_with("Operating System mode watcher stopped")

    def test_given_not_started_when_stop_then_logs_and_does_nothing(self, under_test_context: UnderTestContext) -> None:
        with patch("src.feature.synchronization.watcher.operating_system_mode_watcher.logger.debug") as logger:
            # when
            under_test_context.under_test.stop()

        # then
        under_test_context.gio_settings.disconnect.assert_not_called()
        logger.assert_called_once_with("Operating System mode watcher already stopped")

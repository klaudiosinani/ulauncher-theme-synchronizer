import threading

from gi.repository import Gio, GLib

from src.feature.synchronization.mode.mode_event_handler import ModeEventHandler
from src.orchestration.log import logging_service

logger = logging_service.get(__name__)


class OperatingSystemModeWatcher:
    def __init__(self, gio_settings: Gio.Settings, mode_event_handler: ModeEventHandler, key: str) -> None:
        self._gio_settings = gio_settings
        self._mode_event_handler = mode_event_handler
        self._key = key
        self._lock = threading.Lock()
        self._is_started = False
        self._handler_id: int | None = None
        self._glib_loop: GLib.MainLoop | None = None
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        with self._lock:
            if self._is_started:
                logger.debug("Operating System mode watcher already started")
                return

            self._handler_id = self._gio_settings.connect(f"changed::{self._key}", self._mode_event_handler.handle)

            self._glib_loop = GLib.MainLoop()
            self._thread = threading.Thread(target=self._execute_loop, daemon=True)
            self._thread.start()
            self._is_started = True

            logger.info("Operating System mode watcher started")

    def stop(self) -> None:
        with self._lock:
            if not self._is_started:
                logger.debug("Operating System mode watcher already stopped")
                return

            if self._handler_id is not None:
                self._gio_settings.disconnect(self._handler_id)
                self._handler_id = None

            if self._glib_loop is not None:
                self._glib_loop.quit()
                self._glib_loop = None

            self._thread = None
            self._is_started = False

            logger.info("Operating System mode watcher stopped")

    def _execute_loop(self) -> None:
        glib_loop = self._glib_loop

        if glib_loop is not None:
            glib_loop.run()

import os
import signal
import subprocess
import time

from src.orchestration.launcher.ulauncher_commands_provider import UlauncherCommandsProvider
from src.orchestration.log import logging_service

logger = logging_service.get(__name__)

_TIMEOUT = 10.0
_INTERVAL = 0.1


class UlauncherProcessService:
    def __init__(self, ulauncher_commands_provider: UlauncherCommandsProvider) -> None:
        self._ulauncher_commands_provider = ulauncher_commands_provider

    def retrieve_pids(self) -> set[int]:
        for command in (self._ulauncher_commands_provider.get_pgrep(), self._ulauncher_commands_provider.get_pidof()):
            try:
                result = subprocess.run(command, capture_output=True, text=True, timeout=1)
                pids = {int(p) for p in result.stdout.strip().split() if p.strip()}

                if pids:
                    return pids

            except Exception:
                logger.exception("PID lookup command failed: command=%s", command, exc_info=True)
                continue

        return set()

    def start(self) -> None:
        subprocess.Popen(
            self._ulauncher_commands_provider.get_start(),
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def stop(self, pids: set[int]) -> None:
        for pid in pids:
            os.kill(pid, signal.SIGTERM)

    def restart(self) -> None:
        try:
            pids = self.retrieve_pids()
            self.start()
            new_pids = self._retrieve_new_pids(pids)

            if len(new_pids) == 0:
                logger.warning(
                    "New Ulauncher process did not appear within timeout: timeout=%s interval=%s", _TIMEOUT, _INTERVAL
                )
                return

            self.stop(pids)
            logger.info("Ulauncher restarted (previous pids=%s, new pids=%s)", pids, new_pids)

        except Exception as exc:
            logger.exception("Failed to restart Ulauncher: %s", exc)

    def _retrieve_new_pids(self, pids: set[int]) -> set[int]:
        timeout = time.monotonic() + _TIMEOUT

        while time.monotonic() < timeout:
            current_pids = self.retrieve_pids()
            new_pids = current_pids - pids

            if new_pids:
                return new_pids

            time.sleep(_INTERVAL)

        return set()

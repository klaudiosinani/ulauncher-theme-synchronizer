import os
import signal
import subprocess

from src.orchestration.launcher.ulauncher_commands_provider import UlauncherCommandsProvider
from src.orchestration.log import logging_service

logger = logging_service.get(__name__)


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
                logger.exception("PID lookup command failed: command=%s", command)
                continue

        return set()

    def start(self) -> int:
        process = subprocess.Popen(
            self._ulauncher_commands_provider.get_start(),
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        return process.pid

    def stop(self, pids: set[int]) -> None:
        for pid in pids:
            os.kill(pid, signal.SIGTERM)

    def restart(self) -> bool:
        try:
            pids = self.retrieve_pids()
            new_pid = self.start()
            logger.info("Restarting Ulauncher: previous pids=%s, new pid=%s", pids, new_pid)
            self.stop(pids)
            return True

        except Exception as exc:
            logger.exception("Failed to restart Ulauncher: %s", exc)
            return False

from typing import Final

# We delay the new instance so the previous one may release the Ulauncher DBus name before it starts
START_DELAY_SECONDS: Final = 1


class UlauncherCommandsProvider:
    def __init__(self) -> None:
        self._pgrep: Final = ["pgrep", "-x", "ulauncher"]
        self._pidof: Final = ["pidof", "ulauncher"]
        self._start: Final = ["bash", "-c", f"sleep {START_DELAY_SECONDS} && ulauncher --hide-window"]

    def get_pgrep(self) -> list[str]:
        return list(self._pgrep)

    def get_pidof(self) -> list[str]:
        return list(self._pidof)

    def get_start(self) -> list[str]:
        return list(self._start)

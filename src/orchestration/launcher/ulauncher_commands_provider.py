class UlauncherCommandsProvider:
    def __init__(self) -> None:
        self._pgrep = ["pgrep", "-x", "ulauncher"]
        self._pidof = ["pidof", "ulauncher"]
        self._start = ["bash", "-c", "sleep 1 && ulauncher --hide-window"]

    def get_pgrep(self) -> list[str]:
        return self._pgrep

    def get_pidof(self) -> list[str]:
        return self._pidof

    def get_start(self) -> list[str]:
        return self._start

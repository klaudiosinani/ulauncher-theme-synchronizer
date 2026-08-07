from src.feature.synchronization.mode.mode import Mode
from src.feature.synchronization.theme.theme import Theme


class ThemeParser:
    def parse(self, mode: Mode) -> Theme:
        if mode == Mode.DARK:
            return Theme.DARK

        return Theme.LIGHT

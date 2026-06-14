from src.feature.synchronization.mode.mode import Mode

DARK_KEYWORD = "dark"


class ModeParser:
    def parse(self, mode: str) -> Mode:
        formatted_mode = mode.lower()

        if DARK_KEYWORD in formatted_mode:
            return Mode.DARK

        return Mode.LIGHT

from ulauncher.api.client.Extension import Extension

from src.feature.synchronization.mode.mode import Mode
from src.feature.synchronization.theme.theme_parser import ThemeParser


class ThemeResolutionService:
    def __init__(self, theme_parser: ThemeParser, extension: Extension) -> None:
        self._theme_parser = theme_parser
        self._extension = extension

    def resolve(self, mode: Mode) -> str:
        theme = self._theme_parser.parse(mode)
        preferences: dict[str, str] = self._extension.preferences

        if theme.value not in preferences:
            raise KeyError(f"Preference '{theme.value}' not found in extension preferences")

        return preferences[theme.value]

import os
import pathlib
from typing import Final

ULAUNCHER_SETTINGS_JSON: Final = "~/.config/ulauncher/settings.json"


class PathRetrievalService:
    def __init__(self) -> None:
        self._ulauncher_settings_file_path = pathlib.Path(os.path.expanduser(ULAUNCHER_SETTINGS_JSON))

    def retrieve_ulauncher_settings_file_path(self) -> pathlib.Path:
        return self._ulauncher_settings_file_path

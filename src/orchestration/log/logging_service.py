import logging
import os
import pathlib
import tempfile

_LOGGER_ID = "ulauncher-theme-synchronizer"
_FORMAT = "%(asctime)s | %(levelname)s | %(name)s: %(funcName)s() | %(message)s"
_FILE_LOGGING_VARIABLE = "ULAUNCHER_THEME_SYNCHRONIZER_FILE_LOG"
_LOG_FILE_PATH = pathlib.Path(tempfile.gettempdir()) / f"{_LOGGER_ID}.log"


def _is_file_logging_enabled() -> bool:
    return os.environ.get(_FILE_LOGGING_VARIABLE, "").strip().lower() in ("1", "true")


def _configure() -> None:
    logger = logging.getLogger(_LOGGER_ID)

    if logger.handlers:
        return

    formatter = logging.Formatter(_FORMAT)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)

    if _is_file_logging_enabled():
        file_handler = logging.FileHandler(_LOG_FILE_PATH, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.propagate = False


def get(name: str) -> logging.Logger:
    _configure()
    return logging.getLogger(f"{_LOGGER_ID}.{name}")

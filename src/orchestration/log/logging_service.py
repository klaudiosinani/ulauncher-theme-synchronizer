import logging

_LOGGER_ID = "ulauncher-theme-synchronizer"
_FORMAT = "%(asctime)s | %(levelname)s | %(name)s: %(funcName)s() | %(message)s"


def _configure() -> None:
    logger = logging.getLogger(_LOGGER_ID)

    if logger.handlers:
        return

    formatter = logging.Formatter(_FORMAT)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.propagate = False


def get(name: str) -> logging.Logger:
    _configure()
    return logging.getLogger(f"{_LOGGER_ID}.{name}")

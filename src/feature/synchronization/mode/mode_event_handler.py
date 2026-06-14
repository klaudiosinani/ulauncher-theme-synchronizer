from gi.repository import Gio

from src.feature.synchronization.mode.mode_retrieval_service import ModeRetrievalService
from src.feature.synchronization.theme.theme_activation_service import ThemeActivationService
from src.orchestration.log import logging_service

logger = logging_service.get(__name__)


class ModeEventHandler:
    def __init__(
        self, mode_retrieval_service: ModeRetrievalService, theme_activation_service: ThemeActivationService
    ) -> None:
        self._mode_retrieval_service = mode_retrieval_service
        self._theme_activation_service = theme_activation_service

    def handle(self, gio_settings: Gio.Settings, _: str) -> None:
        mode = self._mode_retrieval_service.retrieve(gio_settings)
        logger.debug("Detected Operating System mode change: %s", mode.value)
        self._theme_activation_service.activate(mode)

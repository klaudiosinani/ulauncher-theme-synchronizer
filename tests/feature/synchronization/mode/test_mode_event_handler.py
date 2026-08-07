from dataclasses import dataclass
from unittest.mock import MagicMock, patch

import pytest
from gi.repository import Gio

from src.feature.synchronization.mode.mode import Mode
from src.feature.synchronization.mode.mode_event_handler import ModeEventHandler
from src.feature.synchronization.mode.mode_retrieval_service import ModeRetrievalService
from src.feature.synchronization.theme.theme_activation_service import ThemeActivationService

COLOR_SCHEME_KEY = "color-scheme"


@dataclass
class UnderTestContext:
    under_test: ModeEventHandler
    gio_settings: MagicMock
    mode_retrieval_service: MagicMock
    theme_activation_service: MagicMock


@pytest.fixture
def under_test_context() -> UnderTestContext:
    gio_settings = MagicMock(spec=Gio.Settings)
    mode_retrieval_service = MagicMock(spec=ModeRetrievalService)
    theme_activation_service = MagicMock(spec=ThemeActivationService)

    under_test = ModeEventHandler(mode_retrieval_service, theme_activation_service)

    return UnderTestContext(
        under_test=under_test,
        gio_settings=gio_settings,
        mode_retrieval_service=mode_retrieval_service,
        theme_activation_service=theme_activation_service,
    )


class TestModeEventHandler:
    def test_given_dark_mode_when_handle_then_activates_theme_for_retrieved_mode(
        self, under_test_context: UnderTestContext
    ) -> None:
        # given
        under_test_context.mode_retrieval_service.retrieve.return_value = Mode.DARK

        # when
        under_test_context.under_test.handle(under_test_context.gio_settings, COLOR_SCHEME_KEY)

        # then
        under_test_context.mode_retrieval_service.retrieve.assert_called_once_with(under_test_context.gio_settings)
        under_test_context.theme_activation_service.activate.assert_called_once_with(Mode.DARK)

    def test_given_light_mode_when_handle_then_activates_theme_for_retrieved_mode(
        self, under_test_context: UnderTestContext
    ) -> None:
        # given
        under_test_context.mode_retrieval_service.retrieve.return_value = Mode.LIGHT

        # when
        under_test_context.under_test.handle(under_test_context.gio_settings, COLOR_SCHEME_KEY)

        # then
        under_test_context.theme_activation_service.activate.assert_called_once_with(Mode.LIGHT)

    def test_given_mode_change_when_handle_then_logs_detected_mode(self, under_test_context: UnderTestContext) -> None:
        # given
        under_test_context.mode_retrieval_service.retrieve.return_value = Mode.DARK

        with patch("src.feature.synchronization.mode.mode_event_handler.logger.debug") as debug:
            # when
            under_test_context.under_test.handle(under_test_context.gio_settings, COLOR_SCHEME_KEY)

        # then
        debug.assert_called_once_with("Detected Operating System mode change: %s", Mode.DARK.value)

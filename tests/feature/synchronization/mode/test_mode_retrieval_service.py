from dataclasses import dataclass
from unittest.mock import MagicMock

import pytest

from src.feature.synchronization.mode.gnome_desktop_settings import GnomeDesktopSettings
from src.feature.synchronization.mode.mode import Mode
from src.feature.synchronization.mode.mode_parser import ModeParser
from src.feature.synchronization.mode.mode_retrieval_service import ModeRetrievalService


@dataclass
class UnderTestContext:
    under_test: ModeRetrievalService
    mode_parser: MagicMock
    gio_desktop_settings: MagicMock


@pytest.fixture
def under_test_context() -> UnderTestContext:
    mode_parser = MagicMock(ModeParser)
    gio_desktop_settings = MagicMock()
    under_test = ModeRetrievalService(mode_parser)

    return UnderTestContext(under_test, mode_parser, gio_desktop_settings)


class TestModeRetrievalService:
    def test_given_dark_color_scheme_when_retrieve_then_returns_dark_mode(
        self, under_test_context: UnderTestContext
    ) -> None:
        # given
        under_test_context.gio_desktop_settings.get_string.return_value = "prefer-dark"
        under_test_context.mode_parser.parse.return_value = Mode.DARK

        # when
        result = under_test_context.under_test.retrieve(under_test_context.gio_desktop_settings)

        # then
        assert result is Mode.DARK
        under_test_context.gio_desktop_settings.get_string.assert_called_once_with(
            GnomeDesktopSettings.COLOR_SCHEME_KEY
        )
        under_test_context.mode_parser.parse.assert_called_once_with("prefer-dark")

    def test_given_light_color_scheme_when_retrieve_then_returns_light_mode(
        self, under_test_context: UnderTestContext
    ) -> None:
        # given
        under_test_context.gio_desktop_settings.get_string.return_value = "prefer-light"
        under_test_context.mode_parser.parse.return_value = Mode.LIGHT

        # when
        result = under_test_context.under_test.retrieve(under_test_context.gio_desktop_settings)

        # then
        assert result is Mode.LIGHT
        under_test_context.gio_desktop_settings.get_string.assert_called_once_with(
            GnomeDesktopSettings.COLOR_SCHEME_KEY
        )
        under_test_context.mode_parser.parse.assert_called_once_with("prefer-light")

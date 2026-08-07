from dataclasses import dataclass
from unittest.mock import MagicMock

import pytest

from src.feature.synchronization.mode.mode import Mode
from src.feature.synchronization.theme.theme import Theme
from src.feature.synchronization.theme.theme_parser import ThemeParser
from src.feature.synchronization.theme.theme_resolution_service import ThemeResolutionService

_PREFERENCES = {
    Theme.DARK.value: "hyperocean",
    Theme.LIGHT.value: "hypersky",
}


@dataclass
class UnderTestContext:
    under_test: ThemeResolutionService
    theme_parser: MagicMock
    extension: MagicMock


@pytest.fixture
def under_test_context() -> UnderTestContext:
    theme_parser = MagicMock(ThemeParser)
    extension = MagicMock()

    under_test = ThemeResolutionService(theme_parser, extension)

    return UnderTestContext(under_test, theme_parser, extension)


class TestThemeResolutionService:
    def test_given_dark_mode_when_resolve_then_returns_dark_theme_preference(
        self, under_test_context: UnderTestContext
    ) -> None:
        # given
        under_test_context.theme_parser.parse.return_value = Theme.DARK
        under_test_context.extension.preferences = _PREFERENCES

        # when
        result = under_test_context.under_test.resolve(Mode.DARK)

        # then
        assert result == "hyperocean"
        under_test_context.theme_parser.parse.assert_called_once_with(Mode.DARK)

    def test_given_light_mode_when_resolve_then_returns_light_theme_preference(
        self, under_test_context: UnderTestContext
    ) -> None:
        # given
        under_test_context.theme_parser.parse.return_value = Theme.LIGHT
        under_test_context.extension.preferences = _PREFERENCES

        # when
        result = under_test_context.under_test.resolve(Mode.LIGHT)

        # then
        assert result == "hypersky"
        under_test_context.theme_parser.parse.assert_called_once_with(Mode.LIGHT)

    def test_given_missing_preference_when_resolve_then_raises_key_error(
        self, under_test_context: UnderTestContext
    ) -> None:
        # given
        under_test_context.theme_parser.parse.return_value = Theme.DARK
        under_test_context.extension.preferences = {}

        # when & then
        with pytest.raises(KeyError, match=r"Preference 'dark_theme' not found in extension preferences"):
            under_test_context.under_test.resolve(Mode.DARK)

from dataclasses import dataclass

import pytest

from src.feature.synchronization.mode.mode import Mode
from src.feature.synchronization.theme.theme import Theme
from src.feature.synchronization.theme.theme_parser import ThemeParser


@dataclass
class UnderTestContext:
    under_test: ThemeParser


@pytest.fixture
def under_test_context() -> UnderTestContext:
    return UnderTestContext(ThemeParser())


class TestThemeParser:
    def test_given_dark_mode_when_parse_called_then_returns_dark_theme(
        self, under_test_context: UnderTestContext
    ) -> None:
        # when
        result = under_test_context.under_test.parse(Mode.DARK)

        # then
        assert result is Theme.DARK

    def test_given_light_mode_when_parse_called_then_returns_light_theme(
        self, under_test_context: UnderTestContext
    ) -> None:
        # when
        result = under_test_context.under_test.parse(Mode.LIGHT)

        # then
        assert result is Theme.LIGHT

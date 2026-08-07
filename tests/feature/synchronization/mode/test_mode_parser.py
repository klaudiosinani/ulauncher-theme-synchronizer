from src.feature.synchronization.mode.mode import Mode
from src.feature.synchronization.mode.mode_parser import ModeParser


class TestModeParser:
    def test_given_dark_keyword_when_parse_then_returns_dark_mode(self) -> None:
        # given
        under_test = ModeParser()

        # when & then
        assert under_test.parse("dark") is Mode.DARK
        assert under_test.parse("Dark") is Mode.DARK
        assert under_test.parse("DARK_MODE") is Mode.DARK
        assert under_test.parse("prefer-dark-theme") is Mode.DARK

    def test_given_non_dark_mode_when_parse_then_returns_light_mode(self) -> None:
        # given
        under_test = ModeParser()

        # when & then
        assert under_test.parse("light") is Mode.LIGHT
        assert under_test.parse("LIGHT") is Mode.LIGHT
        assert under_test.parse("system") is Mode.LIGHT
        assert under_test.parse("") is Mode.LIGHT

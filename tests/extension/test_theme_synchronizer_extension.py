from ulauncher.api.client.Extension import Extension

from src.extension.theme_synchronizer_extension import ThemeSynchronizerExtension


class TestThemeSynchronizerExtension:
    def test_given_valid_imports_when_instantiated_then_it_creates_extension_instance(self) -> None:
        # when
        extension = ThemeSynchronizerExtension()

        # then
        assert isinstance(extension, ThemeSynchronizerExtension)
        assert isinstance(extension, Extension)

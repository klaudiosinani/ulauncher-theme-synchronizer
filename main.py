from src.extension.theme_synchronizer_extension_factory import ThemeSynchronizerExtensionFactory


def main() -> None:
    theme_synchronizer_extension_factory = ThemeSynchronizerExtensionFactory()
    theme_synchronizer_extension = theme_synchronizer_extension_factory.create()
    theme_synchronizer_extension.run()


if __name__ == "__main__":
    main()

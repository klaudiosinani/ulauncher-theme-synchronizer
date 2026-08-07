import sys
import types


def package(name: str) -> types.ModuleType:
    module = types.ModuleType(name)
    module.__path__ = []
    return module


def register(modules: dict[str, types.ModuleType]) -> None:
    sys.modules.update(modules)

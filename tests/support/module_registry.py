import sys
import types
from typing import Any


def package(name: str) -> Any:
    module = types.ModuleType(name)
    module.__path__ = []
    return module


def register(modules: dict[str, types.ModuleType]) -> None:
    sys.modules.update(modules)

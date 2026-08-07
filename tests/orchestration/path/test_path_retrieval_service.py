import os
import pathlib
from dataclasses import dataclass
from unittest.mock import patch

import pytest

from src.orchestration.path.path_retrieval_service import PathRetrievalService


@dataclass
class UnderTestContext:
    under_test: PathRetrievalService
    mock_home: pathlib.Path


@pytest.fixture
def under_test_context(tmp_path: pathlib.Path) -> UnderTestContext:
    mock_home = tmp_path

    def mock_expanduser(path: str) -> str:
        if path.startswith("~"):
            return str(mock_home) + path[1:]
        return path

    with patch.object(os.path, "expanduser", mock_expanduser):
        under_test = PathRetrievalService()
        return UnderTestContext(under_test, mock_home)


class TestPathRetrievalService:
    def test_given_default_constructor_when_retrieve_settings_file_path_then_returns_expanded_json_path(
        self, under_test_context: UnderTestContext
    ) -> None:
        # when
        result = under_test_context.under_test.retrieve_ulauncher_settings_file_path()

        # then
        assert isinstance(result, pathlib.Path)
        assert result == under_test_context.mock_home / ".config" / "ulauncher" / "settings.json"
        assert result.is_absolute()

from dataclasses import dataclass
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src.orchestration.file.atomic_file_service import AtomicFileService
from src.orchestration.launcher.ulauncher_settings_repository import UlauncherSettingsRepository
from src.orchestration.path.path_retrieval_service import PathRetrievalService

_SETTINGS_DATASET = {"theme": "dark"}


@dataclass
class UnderTestContext:
    under_test: UlauncherSettingsRepository
    settings_file_path: MagicMock
    path_retrieval_service: MagicMock
    atomic_file_service: MagicMock


@pytest.fixture
def under_test_context() -> UnderTestContext:
    settings_file_path = MagicMock(spec=Path)

    path_retrieval_service = MagicMock(spec=PathRetrievalService)
    path_retrieval_service.retrieve_ulauncher_settings_file_path.return_value = settings_file_path

    atomic_file_service = MagicMock(spec=AtomicFileService)

    under_test = UlauncherSettingsRepository(path_retrieval_service, atomic_file_service)

    return UnderTestContext(under_test, settings_file_path, path_retrieval_service, atomic_file_service)


class TestUlauncherSettingsRepository:
    def test_given_settings_json_file_when_retrieve_then_returns_deserialized_dictionary(
        self, under_test_context: UnderTestContext
    ) -> None:
        under_test_context.settings_file_path.read_text.return_value = '{"theme": "dark"}'

        result = under_test_context.under_test.retrieve()

        assert result == _SETTINGS_DATASET
        under_test_context.path_retrieval_service.retrieve_ulauncher_settings_file_path.assert_called_once_with()
        under_test_context.settings_file_path.read_text.assert_called_once_with(encoding="utf-8")

    def test_given_settings_dataset_when_persist_then_serializes_to_json_and_writes_atomically_with_correct_indentation(
        self, under_test_context: UnderTestContext
    ) -> None:
        under_test_context.under_test.persist(_SETTINGS_DATASET)

        under_test_context.path_retrieval_service.retrieve_ulauncher_settings_file_path.assert_called_once_with()
        under_test_context.atomic_file_service.write.assert_called_once_with(
            under_test_context.settings_file_path, '{\n  "theme": "dark"\n}'
        )

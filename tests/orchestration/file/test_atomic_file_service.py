from dataclasses import dataclass
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.orchestration.file.atomic_file_service import AtomicFileService


@dataclass
class UnderTestContext:
    under_test: AtomicFileService
    path: Path


@pytest.fixture
def under_test_context(tmp_path: Path) -> UnderTestContext:
    return UnderTestContext(
        under_test=AtomicFileService(),
        path=tmp_path / "settings.json",
    )


class TestAtomicFileService:
    def test_given_path_and_content_when_write_then_replaces_destination_with_temporary_file(
        self, under_test_context: UnderTestContext
    ) -> None:
        # given
        temporary_file = MagicMock()
        temporary_file.name = "/tmp/settings.tmp"
        temporary_file.fileno.return_value = 123

        with (
            patch("src.orchestration.file.atomic_file_service.tempfile.NamedTemporaryFile") as temporary_named_file,
            patch("src.orchestration.file.atomic_file_service.os.fsync") as fsync,
            patch("src.orchestration.file.atomic_file_service.os.replace") as replace,
        ):
            # when
            temporary_named_file.return_value.__enter__.return_value = temporary_file

            under_test_context.under_test.write(under_test_context.path, "content")

        # then
        temporary_named_file.assert_called_once_with(
            mode="w", encoding="utf-8", dir=under_test_context.path.parent, delete=False, suffix=".tmp"
        )
        temporary_file.write.assert_called_once_with("content")
        temporary_file.flush.assert_called_once_with()
        fsync.assert_called_once_with(123)
        replace.assert_called_once_with(temporary_file.name, under_test_context.path)

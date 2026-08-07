import os
import tempfile
from contextlib import suppress
from pathlib import Path


class AtomicFileService:
    def write(self, path: Path, content: str, encoding: str = "utf-8") -> None:
        temporary_file_path: str | None = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding=encoding, dir=path.parent, delete=False, suffix=".tmp"
            ) as temporary_file:
                temporary_file.write(content)
                temporary_file.flush()
                os.fsync(temporary_file.fileno())
                temporary_file_path = temporary_file.name

            os.replace(temporary_file_path, path)

        except Exception:
            if temporary_file_path is not None:
                with suppress(OSError):
                    os.unlink(temporary_file_path)

            raise

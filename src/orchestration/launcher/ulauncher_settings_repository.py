import json
from typing import Any

from src.orchestration.file.atomic_file_service import AtomicFileService
from src.orchestration.path.path_retrieval_service import PathRetrievalService


class UlauncherSettingsRepository:
    def __init__(self, path_retrieval_service: PathRetrievalService, atomic_file_service: AtomicFileService) -> None:
        self._path_retrieval_service = path_retrieval_service
        self._atomic_file_service = atomic_file_service

    def retrieve(self) -> dict[str, Any]:
        path = self._path_retrieval_service.retrieve_ulauncher_settings_file_path()
        dataset = path.read_text(encoding="utf-8")
        return json.loads(dataset)

    def persist(self, data: dict[str, Any]) -> None:
        path = self._path_retrieval_service.retrieve_ulauncher_settings_file_path()
        content = json.dumps(data, indent=2)
        self._atomic_file_service.write(path, content)

from abc import ABC, abstractmethod

from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction


class KeywordQueryEventHandler(ABC):
    @abstractmethod
    def handle(self) -> RenderResultListAction: ...

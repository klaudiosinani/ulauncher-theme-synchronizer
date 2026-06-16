from dataclasses import dataclass
from unittest.mock import MagicMock

import pytest
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.event import BaseEvent

from src.feature.synchronization.lifecycle.preferences_event_listener import PreferencesEventListener
from src.feature.synchronization.watcher.operating_system_mode_watcher import OperatingSystemModeWatcher


@dataclass
class UnderTestContext:
    under_test: PreferencesEventListener
    operating_system_mode_watcher: MagicMock


@pytest.fixture
def under_test_context() -> UnderTestContext:
    operating_system_mode_watcher = MagicMock(spec=OperatingSystemModeWatcher)
    under_test = PreferencesEventListener(operating_system_mode_watcher)

    return UnderTestContext(under_test, operating_system_mode_watcher)


class TestPreferencesEventListener:
    def test_given_event_and_extension_when_on_event_then_starts_operating_system_mode_watcher(
        self, under_test_context: UnderTestContext
    ) -> None:
        # given
        event = MagicMock(spec=BaseEvent)
        extension = MagicMock(spec=Extension)

        # when
        under_test_context.under_test.on_event(event, extension)

        # then
        under_test_context.operating_system_mode_watcher.start.assert_called_once_with()

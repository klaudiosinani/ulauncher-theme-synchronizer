import types
from unittest.mock import MagicMock

from tests.support.module_registry import package, register


class ExtensionStub:
    def __init__(self) -> None:
        self.subscribe = MagicMock()
        self.run = MagicMock()


class EventListenerStub:
    pass


class BaseEventStub:
    pass


class KeywordQueryEventStub:
    pass


class PreferencesEventStub:
    pass


class SystemExitEventStub:
    pass


class HideWindowActionStub:
    pass


class RenderResultListActionStub:
    pass


class ExtensionResultItemStub:
    pass


def install_ulauncher_stubs() -> None:
    ulauncher_module = package("ulauncher")
    api_module = package("ulauncher.api")
    client_module = package("ulauncher.api.client")
    shared_module = package("ulauncher.api.shared")
    action_package_module = package("ulauncher.api.shared.action")
    item_package_module = package("ulauncher.api.shared.item")

    extension_module = types.ModuleType("ulauncher.api.client.Extension")
    event_listener_module = types.ModuleType("ulauncher.api.client.EventListener")
    event_module = types.ModuleType("ulauncher.api.shared.event")
    hide_window_action_module = types.ModuleType("ulauncher.api.shared.action.HideWindowAction")
    render_result_list_action_module = types.ModuleType("ulauncher.api.shared.action.RenderResultListAction")
    extension_result_item_module = types.ModuleType("ulauncher.api.shared.item.ExtensionResultItem")

    extension_module.Extension = ExtensionStub
    event_listener_module.EventListener = EventListenerStub
    event_module.BaseEvent = BaseEventStub
    event_module.KeywordQueryEvent = KeywordQueryEventStub
    event_module.PreferencesEvent = PreferencesEventStub
    event_module.SystemExitEvent = SystemExitEventStub
    hide_window_action_module.HideWindowAction = HideWindowActionStub
    render_result_list_action_module.RenderResultListAction = RenderResultListActionStub
    extension_result_item_module.ExtensionResultItem = ExtensionResultItemStub

    ulauncher_module.api = api_module
    api_module.client = client_module
    api_module.shared = shared_module
    client_module.Extension = extension_module
    client_module.EventListener = event_listener_module
    shared_module.event = event_module
    shared_module.action = action_package_module
    shared_module.item = item_package_module
    action_package_module.HideWindowAction = hide_window_action_module
    action_package_module.RenderResultListAction = render_result_list_action_module
    item_package_module.ExtensionResultItem = extension_result_item_module

    register(
        {
            "ulauncher": ulauncher_module,
            "ulauncher.api": api_module,
            "ulauncher.api.client": client_module,
            "ulauncher.api.shared": shared_module,
            "ulauncher.api.shared.action": action_package_module,
            "ulauncher.api.shared.item": item_package_module,
            "ulauncher.api.client.Extension": extension_module,
            "ulauncher.api.client.EventListener": event_listener_module,
            "ulauncher.api.shared.event": event_module,
            "ulauncher.api.shared.action.HideWindowAction": hide_window_action_module,
            "ulauncher.api.shared.action.RenderResultListAction": render_result_list_action_module,
            "ulauncher.api.shared.item.ExtensionResultItem": extension_result_item_module,
        }
    )

from collections.abc import Generator
from contextlib import ExitStack, contextmanager
from dataclasses import dataclass
from typing import Any
from unittest.mock import MagicMock, call, patch

from ulauncher.api.shared.event import KeywordQueryEvent, PreferencesEvent, SystemExitEvent

from src.extension.theme_synchronizer_extension import ThemeSynchronizerExtension
from src.extension.theme_synchronizer_extension_factory import ThemeSynchronizerExtensionFactory

_MODULE = "src.extension.theme_synchronizer_extension_factory"


@dataclass
class UnderTestContext:
    under_test: ThemeSynchronizerExtensionFactory
    gio_settings: MagicMock
    mode_retrieval_service: MagicMock
    ulauncher_settings_service: MagicMock
    operating_system_mode_watcher: MagicMock
    display_status_event_handler: MagicMock
    keyword_query_event_listener: MagicMock
    preferences_event_listener: MagicMock
    system_exit_event_listener: MagicMock
    display_status_event_handler_class: MagicMock | None = None
    keyword_query_event_listener_class: MagicMock | None = None
    preferences_event_listener_class: MagicMock | None = None
    system_exit_event_listener_class: MagicMock | None = None
    compose_operating_system_mode_watcher: MagicMock | None = None


class TestThemeSynchronizerExtensionFactory:
    def test_given_valid_composed_dependencies_when_create_then_returns_extension_instance(
        self,
    ) -> None:
        # given
        with self._arrange_under_test_context() as context:
            # when
            result = context.under_test.create()

        # then
        assert isinstance(result, ThemeSynchronizerExtension)

    def test_given_composed_dependencies_when_create_then_watcher_receives_correct_arguments(
        self,
    ) -> None:
        # given
        with self._arrange_under_test_context() as context:
            # when
            result = context.under_test.create()

        # then
        context.compose_operating_system_mode_watcher.assert_called_once_with(
            context.mode_retrieval_service,
            context.ulauncher_settings_service,
            context.gio_settings,
            result,
        )

    def test_given_composed_dependencies_when_create_then_display_status_handler_receives_correct_arguments(
        self,
    ) -> None:
        # given
        with self._arrange_under_test_context() as context:
            # when
            context.under_test.create()

        # then
        context.display_status_event_handler_class.assert_called_once_with(
            context.mode_retrieval_service,
            context.ulauncher_settings_service,
            context.gio_settings,
        )

    def test_given_created_listeners_when_create_then_extension_subscribes_all_event_listeners_in_order(
        self,
    ) -> None:
        # given
        with self._arrange_under_test_context() as context:
            # when
            result = context.under_test.create()

        # then
        context.keyword_query_event_listener_class.assert_called_once_with(context.display_status_event_handler)
        context.preferences_event_listener_class.assert_called_once_with(context.operating_system_mode_watcher)
        context.system_exit_event_listener_class.assert_called_once_with(context.operating_system_mode_watcher)

        assert result.subscribe.call_args_list == [
            call(KeywordQueryEvent, context.keyword_query_event_listener),
            call(PreferencesEvent, context.preferences_event_listener),
            call(SystemExitEvent, context.system_exit_event_listener),
        ]

    @contextmanager
    def _arrange_under_test_context(self) -> Generator[UnderTestContext, Any, None]:
        context = self._create_under_test_context()

        with ExitStack() as stack:
            patched_methods = _enter_object_patches(
                stack=stack,
                target=context.under_test,
                return_values_by_method_name=self._get_factory_method_return_values(context),
            )
            patched_classes = _enter_module_patches(
                stack=stack,
                return_values_by_name=self._get_module_class_return_values(context),
            )

            context.compose_operating_system_mode_watcher = patched_methods["_compose_operating_system_mode_watcher"]
            context.display_status_event_handler_class = patched_classes["DisplayStatusEventHandler"]
            context.keyword_query_event_listener_class = patched_classes["KeywordQueryEventListener"]
            context.preferences_event_listener_class = patched_classes["PreferencesEventListener"]
            context.system_exit_event_listener_class = patched_classes["SystemExitEventListener"]

            yield context

    def _create_under_test_context(self) -> UnderTestContext:
        return UnderTestContext(
            under_test=ThemeSynchronizerExtensionFactory(),
            gio_settings=MagicMock(),
            mode_retrieval_service=MagicMock(),
            ulauncher_settings_service=MagicMock(),
            operating_system_mode_watcher=MagicMock(),
            display_status_event_handler=MagicMock(),
            keyword_query_event_listener=MagicMock(),
            preferences_event_listener=MagicMock(),
            system_exit_event_listener=MagicMock(),
        )

    def _get_factory_method_return_values(
        self,
        context: UnderTestContext,
    ) -> dict[str, object]:
        return {
            "_compose_gio_settings": context.gio_settings,
            "_compose_mode_retrieval_service": context.mode_retrieval_service,
            "_compose_ulauncher_settings_service": context.ulauncher_settings_service,
            "_compose_operating_system_mode_watcher": context.operating_system_mode_watcher,
        }

    def _get_module_class_return_values(
        self,
        context: UnderTestContext,
    ) -> dict[str, object]:
        return {
            "DisplayStatusEventHandler": context.display_status_event_handler,
            "KeywordQueryEventListener": context.keyword_query_event_listener,
            "PreferencesEventListener": context.preferences_event_listener,
            "SystemExitEventListener": context.system_exit_event_listener,
        }


def _enter_object_patches(
    stack: ExitStack,
    target: object,
    return_values_by_method_name: dict[str, object],
) -> dict[str, MagicMock]:
    return {
        method_name: stack.enter_context(patch.object(target, method_name, return_value=return_value))
        for method_name, return_value in return_values_by_method_name.items()
    }


def _enter_module_patches(
    stack: ExitStack,
    return_values_by_name: dict[str, object],
) -> dict[str, MagicMock]:
    return {
        name: stack.enter_context(patch(f"{_MODULE}.{name}", return_value=return_value))
        for name, return_value in return_values_by_name.items()
    }

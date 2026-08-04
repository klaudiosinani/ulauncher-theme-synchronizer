# pyright: reportPrivateUsage=false
import signal
import subprocess
from dataclasses import dataclass
from unittest.mock import MagicMock, call, patch

import pytest

from src.orchestration.launcher.ulauncher_commands_provider import UlauncherCommandsProvider
from src.orchestration.launcher.ulauncher_process_service import UlauncherProcessService

ULAUNCHER_RESTARTED_PID = 200

ULAUNCHER_PID = 100


@dataclass
class UnderTestContext:
    under_test: UlauncherProcessService


@pytest.fixture
def under_test_context() -> UnderTestContext:
    ulauncher_commands_provider = UlauncherCommandsProvider()
    under_test = UlauncherProcessService(ulauncher_commands_provider)

    return UnderTestContext(under_test=under_test)


class TestUlauncherProcessService:
    def test_given_pgrep_returns_pids_when_retrieve_pids_then_returns_parsed_pids(
        self, under_test_context: UnderTestContext
    ) -> None:
        # given
        pgrep_outcome = MagicMock()
        pgrep_outcome.stdout = "123\n456\n"

        with patch(
            "src.orchestration.launcher.ulauncher_process_service.subprocess.run", return_value=pgrep_outcome
        ) as run:
            # when
            result = under_test_context.under_test.retrieve_pids()

        # then
        assert result == {123, 456}
        run.assert_called_once_with(["pgrep", "-x", "ulauncher"], capture_output=True, text=True, timeout=1)

    def test_given_pgrep_returns_no_pids_and_pidof_returns_pids_when_retrieve_pids_then_returns_pidof_pids(
        self, under_test_context: UnderTestContext
    ) -> None:
        # given
        pgrep_outcome = MagicMock()
        pgrep_outcome.stdout = ""

        pidof_outcome = MagicMock()
        pidof_outcome.stdout = "1234 5678"

        with patch(
            "src.orchestration.launcher.ulauncher_process_service.subprocess.run",
            side_effect=[pgrep_outcome, pidof_outcome],
        ) as run:
            # when
            actual = under_test_context.under_test.retrieve_pids()

        # then
        assert actual == {1234, 5678}
        assert run.call_args_list == [
            call(["pgrep", "-x", "ulauncher"], capture_output=True, text=True, timeout=1),
            call(["pidof", "ulauncher"], capture_output=True, text=True, timeout=1),
        ]

    def test_given_both_pid_lookup_commands_fail_when_retrieve_pids_then_returns_empty_set(
        self, under_test_context: UnderTestContext
    ) -> None:
        # given
        pgrep_outcome = Exception("pgrep failed")
        pidof_outcome = Exception("pidof failed")
        outcomes = [pgrep_outcome, pidof_outcome]

        with patch("src.orchestration.launcher.ulauncher_process_service.subprocess.run", side_effect=outcomes):
            # when
            actual = under_test_context.under_test.retrieve_pids()

        # then
        assert actual == set()

    def test_given_start_when_start_then_starts_process_with_expected_command(
        self, under_test_context: UnderTestContext
    ) -> None:
        with patch("src.orchestration.launcher.ulauncher_process_service.subprocess.Popen") as popen:
            # when
            under_test_context.under_test.start()

        # then
        popen.assert_called_once_with(
            ["bash", "-c", "sleep 1 && ulauncher --hide-window"],
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def test_given_pids_when_stop_then_sends_sigterm_to_each_pid(self, under_test_context: UnderTestContext) -> None:
        # given
        ulauncher_pids = {1234, 5678}

        with patch("src.orchestration.launcher.ulauncher_process_service.os.kill") as kill:
            # when
            under_test_context.under_test.stop(ulauncher_pids)

        kill.assert_has_calls([call(1234, signal.SIGTERM), call(5678, signal.SIGTERM)], any_order=True)

    def test_given_new_process_appears_when_restart_then_starts_and_stops_previous_pids(
        self, under_test_context: UnderTestContext
    ) -> None:
        # given
        with (
            patch.object(under_test_context.under_test, "retrieve_pids", side_effect=[{ULAUNCHER_PID}]),
            patch.object(under_test_context.under_test, "start", side_effect=[{ULAUNCHER_RESTARTED_PID}]) as start,
            patch.object(under_test_context.under_test, "stop") as stop,
            patch("src.orchestration.launcher.ulauncher_process_service.logger.info") as logger,
        ):
            # when
            under_test_context.under_test.restart()

        # then
        start.assert_called_once_with()
        stop.assert_called_once_with({ULAUNCHER_PID})
        logger.info()
        logger.assert_called_once_with(
            "Restarting Ulauncher: previous pids=%s, new pid=%s", {ULAUNCHER_PID}, {ULAUNCHER_RESTARTED_PID}
        )

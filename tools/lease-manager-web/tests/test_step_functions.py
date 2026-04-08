import json
from unittest.mock import MagicMock, call, patch

from lease_manager_web.aws.step_functions import start_and_poll


def _make_sf_mock(statuses: list[str]) -> MagicMock:
    """Build a mock Step Functions client that returns the given sequence of statuses."""
    mock_sf = MagicMock()
    mock_sf.start_execution.return_value = {"executionArn": "arn:aws:states:::execution/test/1"}
    mock_sf.describe_execution.side_effect = [{"status": s} for s in statuses]
    return mock_sf


def test_returns_success_on_first_poll():
    mock_sf = _make_sf_mock(["SUCCEEDED"])
    with patch("lease_manager_web.aws.sessions.step_functions", return_value=mock_sf), \
         patch("time.sleep"):
        ok, status = start_and_poll("arn:aws:states:::stateMachine/test")

    assert ok is True
    assert status is None


def test_returns_failure_on_failed_status():
    mock_sf = _make_sf_mock(["FAILED"])
    with patch("lease_manager_web.aws.sessions.step_functions", return_value=mock_sf), \
         patch("time.sleep"):
        ok, status = start_and_poll("arn:aws:states:::stateMachine/test")

    assert ok is False
    assert status == "FAILED"


def test_polls_until_terminal_state():
    mock_sf = _make_sf_mock(["RUNNING", "RUNNING", "SUCCEEDED"])
    with patch("lease_manager_web.aws.sessions.step_functions", return_value=mock_sf), \
         patch("time.sleep") as mock_sleep:
        ok, status = start_and_poll("arn:aws:states:::stateMachine/test")

    assert ok is True
    assert mock_sleep.call_count == 2
    mock_sleep.assert_has_calls([call(10), call(10)])


def test_passes_input_payload_as_json():
    mock_sf = _make_sf_mock(["SUCCEEDED"])
    payload = {"user_id": "u1", "duration": "1h"}
    with patch("lease_manager_web.aws.sessions.step_functions", return_value=mock_sf), \
         patch("time.sleep"):
        start_and_poll("arn:aws:states:::stateMachine/test", input_payload=payload)

    call_kwargs = mock_sf.start_execution.call_args[1]
    assert "input" in call_kwargs
    assert json.loads(call_kwargs["input"]) == payload


def test_omits_input_when_payload_is_none():
    mock_sf = _make_sf_mock(["SUCCEEDED"])
    with patch("lease_manager_web.aws.sessions.step_functions", return_value=mock_sf), \
         patch("time.sleep"):
        start_and_poll("arn:aws:states:::stateMachine/test", input_payload=None)

    call_kwargs = mock_sf.start_execution.call_args[1]
    assert "input" not in call_kwargs

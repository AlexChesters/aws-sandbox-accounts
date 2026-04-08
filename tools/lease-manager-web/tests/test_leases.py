from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from lease_manager_web.aws.leases import expire_lease, get_lease, list_active_leases


def _dynamo_string(value: str) -> dict:
    return {"S": value}


def _dynamo_map(d: dict) -> dict:
    return {"M": {k: {"S": v} for k, v in d.items()}}


def _dynamo_response(*items: dict) -> dict:
    return {"Items": list(items)}


def test_list_active_leases_returns_lease_data():
    lease_id = "lease-abc-123"
    active_item = {
        "pk": _dynamo_string("lease_status#active"),
        "data": _dynamo_map({"ids": lease_id}),
    }
    # The active item's "data" field is a map of {lease_id: ...}; the code iterates active["data"]
    # Active item deserialised: {"pk": "lease_status#active", "data": {"some-id": "some-val"}}
    # We need active["data"] to be a dict we can iterate as lease_ids

    lease_data_item = {
        "pk": _dynamo_string(f"lease_id#{lease_id}"),
        "data": _dynamo_map({"user": "user-1", "expires": "2026-12-01T00:00:00.000"}),
    }

    mock_db = MagicMock()

    # First query returns the active-set item; subsequent queries return individual lease items
    mock_db.query.side_effect = [
        # Active set response — data is a DynamoDB map with lease_id keys
        {
            "Items": [
                {
                    "pk": {"S": "lease_status#active"},
                    "data": {"M": {lease_id: {"S": "1"}}},
                }
            ]
        },
        # Individual lease response
        {
            "Items": [
                {
                    "pk": {"S": f"lease_id#{lease_id}"},
                    "data": {
                        "M": {
                            "user": {"S": "user-1"},
                            "expires": {"S": "2026-12-01T00:00:00.000"},
                        }
                    },
                }
            ]
        },
    ]

    with patch("lease_manager_web.aws.sessions.dynamo", return_value=mock_db):
        result = list_active_leases()

    assert lease_id in result
    assert result[lease_id]["user"] == "user-1"
    assert result[lease_id]["expires"] == "2026-12-01T00:00:00.000"


def test_get_lease_queries_correct_pk():
    lease_id = "lease-xyz"
    mock_db = MagicMock()
    mock_db.query.return_value = {
        "Items": [
            {
                "pk": {"S": f"lease_id#{lease_id}"},
                "data": {"M": {"user": {"S": "u1"}, "expires": {"S": "2026-01-01T00:00:00.000"}}},
            }
        ]
    }

    with patch("lease_manager_web.aws.sessions.dynamo", return_value=mock_db):
        result = get_lease(lease_id)

    mock_db.query.assert_called_once()
    call_kwargs = mock_db.query.call_args[1]
    assert call_kwargs["ExpressionAttributeValues"][":pk_val"] == {"S": f"lease_id#{lease_id}"}
    assert result["data"]["user"] == "u1"


def test_expire_lease_writes_past_expiration():
    lease_id = "lease-exp-1"
    lease_data = {"user": "u1", "expires": "2026-12-31T12:00:00.000"}

    mock_db = MagicMock()

    with patch("lease_manager_web.aws.sessions.dynamo", return_value=mock_db):
        expire_lease(lease_id, lease_data)

    mock_db.put_item.assert_called_once()
    call_kwargs = mock_db.put_item.call_args[1]
    assert call_kwargs["Item"]["pk"] == {"S": f"lease_id#{lease_id}"}

    # The expires value in lease_data should have been set to the past
    new_expires = datetime.fromisoformat(lease_data["expires"])
    assert new_expires < datetime.now(timezone.utc).replace(tzinfo=None)

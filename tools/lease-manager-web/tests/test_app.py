import threading
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from lease_manager_web.app import _enrich_leases, app
from lease_manager_web.jobs import JobStatus, Job


@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# ---------------------------------------------------------------------------
# _enrich_leases
# ---------------------------------------------------------------------------

def test_enrich_leases_adds_expected_fields():
    raw = {
        "lease-1": {
            "user": "user-id-1",
            "expires": "2099-12-31T12:00:00.000000",
        }
    }
    with patch("lease_manager_web.aws.identities.get_username", return_value="alice"):
        result = _enrich_leases(raw)

    assert "lease-1" in result
    enriched = result["lease-1"]
    assert enriched["username"] == "alice"
    assert "expires_iso" in enriched
    assert "expires_human" in enriched
    # Original fields still present
    assert enriched["user"] == "user-id-1"


# ---------------------------------------------------------------------------
# GET /
# ---------------------------------------------------------------------------

def test_index_returns_200(client):
    with patch("lease_manager_web.aws.leases.list_active_leases", return_value={}), \
         patch("lease_manager_web.aws.identities.get_username", return_value="u"):
        resp = client.get("/")
    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# GET /leases
# ---------------------------------------------------------------------------

def test_leases_partial_returns_200(client):
    with patch("lease_manager_web.aws.leases.list_active_leases", return_value={}), \
         patch("lease_manager_web.aws.identities.get_username", return_value="u"):
        resp = client.get("/leases")
    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# GET /create
# ---------------------------------------------------------------------------

def test_create_get_returns_200(client):
    with patch("lease_manager_web.aws.identities.list_users", return_value=[("alice", "uid-1")]):
        resp = client.get("/create")
    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# POST /create
# ---------------------------------------------------------------------------

def test_create_post_missing_fields_renders_error(client):
    with patch("lease_manager_web.aws.identities.list_users", return_value=[]):
        resp = client.post("/create", data={"user_id": "", "duration": ""})
    assert resp.status_code == 200
    assert b"required" in resp.data.lower()


def test_create_post_valid_redirects_to_job(client):
    with patch("lease_manager_web.app.create_job", return_value="job-123"), \
         patch("threading.Thread") as mock_thread:
        mock_thread.return_value = MagicMock()
        resp = client.post("/create", data={"user_id": "uid-1", "duration": "1h"})
    assert resp.status_code == 302
    assert "/jobs/job-123" in resp.headers["Location"]


# ---------------------------------------------------------------------------
# GET /invalidate
# ---------------------------------------------------------------------------

def test_invalidate_get_returns_200(client):
    resp = client.get("/invalidate")
    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# POST /invalidate
# ---------------------------------------------------------------------------

def test_invalidate_post_missing_lease_id_renders_error(client):
    resp = client.post("/invalidate", data={"lease_id": ""})
    assert resp.status_code == 200
    assert b"required" in resp.data.lower()


def test_invalidate_post_valid_redirects_to_job(client):
    with patch("lease_manager_web.app.create_job", return_value="job-456"), \
         patch("threading.Thread") as mock_thread:
        mock_thread.return_value = MagicMock()
        resp = client.post("/invalidate", data={"lease_id": "lease-abc"})
    assert resp.status_code == 302
    assert "/jobs/job-456" in resp.headers["Location"]


# ---------------------------------------------------------------------------
# GET /jobs/<job_id>
# ---------------------------------------------------------------------------

def test_job_page_returns_200_for_existing_job(client):
    job = Job(id="job-789", status=JobStatus.RUNNING)
    with patch("lease_manager_web.app.get_job", return_value=job):
        resp = client.get("/jobs/job-789")
    assert resp.status_code == 200


def test_job_page_returns_404_for_unknown_job(client):
    with patch("lease_manager_web.app.get_job", return_value=None):
        resp = client.get("/jobs/no-such-job")
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# GET /jobs/<job_id>/status
# ---------------------------------------------------------------------------

def test_job_status_returns_200_for_existing_job(client):
    job = Job(id="job-789", status=JobStatus.SUCCEEDED, message="Done")
    with patch("lease_manager_web.app.get_job", return_value=job):
        resp = client.get("/jobs/job-789/status")
    assert resp.status_code == 200

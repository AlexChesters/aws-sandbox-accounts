import uuid

from lease_manager_web.jobs import JobStatus, create_job, get_job, update_job


def test_create_job_returns_uuid():
    job_id = create_job()
    # Should be a valid UUID
    uuid.UUID(job_id)


def test_create_job_registers_running_status():
    job_id = create_job()
    job = get_job(job_id)
    assert job is not None
    assert job.id == job_id
    assert job.status == JobStatus.RUNNING
    assert job.message == ""
    assert job.detail == ""


def test_get_job_returns_none_for_unknown_id():
    assert get_job("nonexistent-id") is None


def test_update_job_modifies_fields():
    job_id = create_job()
    update_job(job_id, JobStatus.SUCCEEDED, "Done", "All good")
    job = get_job(job_id)
    assert job.status == JobStatus.SUCCEEDED
    assert job.message == "Done"
    assert job.detail == "All good"


def test_update_job_noop_for_unknown_id():
    # Should not raise
    update_job("nonexistent-id", JobStatus.FAILED, "oops")

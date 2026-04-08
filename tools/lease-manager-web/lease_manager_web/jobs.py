import threading
import uuid
from dataclasses import dataclass, field
from enum import Enum


class JobStatus(Enum):
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


@dataclass
class Job:
    id: str
    status: JobStatus = field(default=JobStatus.RUNNING)
    message: str = ""
    detail: str = ""


_jobs: dict[str, Job] = {}
_lock = threading.Lock()


def create_job() -> str:
    job_id = str(uuid.uuid4())
    with _lock:
        _jobs[job_id] = Job(id=job_id)
    return job_id


def update_job(job_id: str, status: JobStatus, message: str = "", detail: str = "") -> None:
    with _lock:
        job = _jobs.get(job_id)
        if job:
            job.status = status
            job.message = message
            job.detail = detail


def get_job(job_id: str) -> Job | None:
    with _lock:
        return _jobs.get(job_id)

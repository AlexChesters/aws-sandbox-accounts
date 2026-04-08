import threading
from datetime import datetime, timezone

import humanize
from flask import Flask, abort, redirect, render_template, request, url_for

from lease_manager_web.aws import identities, leases, step_functions
from lease_manager_web.jobs import JobStatus, create_job, get_job, update_job

app = Flask(__name__)

DURATIONS = [
    ("5 minutes", "5m"),
    ("30 minutes", "30m"),
    ("1 hour", "1h"),
    ("3 hours", "3h"),
    ("6 hours", "6h"),
    ("12 hours", "12h"),
    ("24 hours", "24h"),
    ("3 days", "3d"),
    ("7 days", "7d"),
]


def _enrich_leases(raw_leases: dict[str, dict]) -> dict[str, dict]:
    enriched = {}
    for lease_id, data in raw_leases.items():
        expiry_date = datetime.fromisoformat(data["expires"])
        expiry_utc = expiry_date.replace(tzinfo=timezone.utc)
        enriched[lease_id] = {
            **data,
            "username": identities.get_username(data["user"]),
            "expires_iso": expiry_date.isoformat(),
            "expires_human": humanize.naturaltime(expiry_utc, when=datetime.now(timezone.utc)),
        }
    return enriched


@app.get("/")
def index():
    raw = leases.list_active_leases()
    active_leases = _enrich_leases(raw)
    return render_template("index.html", leases=active_leases)


@app.get("/leases")
def leases_partial():
    raw = leases.list_active_leases()
    active_leases = _enrich_leases(raw)
    return render_template("partials/leases_table.html", leases=active_leases)


@app.get("/create")
def create_get():
    users = identities.list_users()
    return render_template("create.html", users=users, durations=DURATIONS)


@app.post("/create")
def create_post():
    user_id = request.form.get("user_id", "").strip()
    duration = request.form.get("duration", "").strip()

    if not user_id or not duration:
        users = identities.list_users()
        return render_template(
            "create.html", users=users, durations=DURATIONS, error="All fields are required."
        )

    job_id = create_job()
    t = threading.Thread(target=_create_lease_worker, args=(job_id, user_id, duration), daemon=True)
    t.start()
    return redirect(url_for("job_page", job_id=job_id))


def _create_lease_worker(job_id: str, user_id: str, duration: str) -> None:
    try:
        succeeded, status = step_functions.start_and_poll(
            step_functions.LEASE_CREATOR_ARN,
            input_payload={"user_id": user_id, "duration": duration},
        )
        if succeeded:
            update_job(job_id, JobStatus.SUCCEEDED, "Lease created successfully.")
        else:
            update_job(job_id, JobStatus.FAILED, f"Step function failed: {status}")
    except Exception as exc:
        update_job(job_id, JobStatus.FAILED, "Unexpected error.", str(exc))


@app.get("/invalidate")
def invalidate_get():
    lease_id = request.args.get("lease_id", "")
    return render_template("invalidate.html", lease_id=lease_id)


@app.post("/invalidate")
def invalidate_post():
    lease_id = request.form.get("lease_id", "").strip()

    if not lease_id:
        return render_template("invalidate.html", lease_id="", error="Lease ID is required.")

    job_id = create_job()
    t = threading.Thread(target=_invalidate_lease_worker, args=(job_id, lease_id), daemon=True)
    t.start()
    return redirect(url_for("job_page", job_id=job_id))


def _invalidate_lease_worker(job_id: str, lease_id: str) -> None:
    try:
        lease = leases.get_lease(lease_id)
        leases.expire_lease(lease_id, lease["data"])

        succeeded, status = step_functions.start_and_poll(step_functions.LEASE_JANITOR_ARN)
        if succeeded:
            update_job(job_id, JobStatus.SUCCEEDED, f"Lease {lease_id} invalidated successfully.")
        else:
            update_job(job_id, JobStatus.FAILED, f"Step function failed: {status}")
    except Exception as exc:
        update_job(job_id, JobStatus.FAILED, "Unexpected error.", str(exc))


@app.get("/jobs/<job_id>")
def job_page(job_id: str):
    job = get_job(job_id)
    if job is None:
        abort(404)
    return render_template("job.html", job=job)


@app.get("/jobs/<job_id>/status")
def job_status(job_id: str):
    job = get_job(job_id)
    if job is None:
        abort(404)
    return render_template("partials/job_status.html", job=job)

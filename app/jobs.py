import time
import uuid
from datetime import datetime
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from . import models

FAKE_RESULT_URL = "https://example.com/docs/demo"

def create_job(db: Session, repo_url: str) -> str:
    job_id = str(uuid.uuid4())
    job = models.Job(
        id=job_id,
        repo_url=repo_url,
        status="pending",
        result_url=None,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job_id

def run_job_background(job_id: str, db_session_factory):
    db = db_session_factory()
    try:
        job = db.query(models.Job).filter(models.Job.id == job_id).first()
        if not job:
            return

        job.status = "running"
        job.updated_at = datetime.utcnow()
        db.commit()

        # Simulate long processing
        time.sleep(10)

        job.status = "done"
        job.result_url = FAKE_RESULT_URL
        job.updated_at = datetime.utcnow()
        db.commit()
    finally:
        db.close()

def enqueue_job(background_tasks: BackgroundTasks, job_id: str, db_session_factory):
    background_tasks.add_task(run_job_background, job_id, db_session_factory)

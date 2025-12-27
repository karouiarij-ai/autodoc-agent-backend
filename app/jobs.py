import time
import uuid
import logging
from datetime import datetime, timezone
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from . import models

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FAKE_RESULT_URL = "https://example.com/docs/demo"

def create_job(db: Session, repo_url: str) -> str:
    job_id = str(uuid.uuid4())
    job = models.Job(
        id=job_id,
        repo_url=str(repo_url),
        status="pending",
        result_url=None,
        error_message=None,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    logger.info(f"Created job {job_id} for repo: {repo_url}")
    return job_id

def run_job_background(job_id: str, db_session_factory):
    db = db_session_factory()
    try:
        job = db.query(models.Job).filter(models.Job.id == job_id).first()
        if not job:
            logger.error(f"Job {job_id} not found")
            return

        logger.info(f"Starting job {job_id}")
        job.status = "running"
        job.updated_at = datetime.now(timezone.utc)
        db.commit()

        try:
            # Simulate long processing
            time.sleep(10)

            # In real implementation, this would clone repo, analyze, and generate docs
            # For now, we simulate success
            job.status = "done"
            job.result_url = FAKE_RESULT_URL
            job.error_message = None
            logger.info(f"Job {job_id} completed successfully")
            
        except Exception as e:
            # Handle job processing errors
            logger.error(f"Job {job_id} failed: {str(e)}")
            job.status = "error"
            job.result_url = None
            job.error_message = str(e)
        
        job.updated_at = datetime.now(timezone.utc)
        db.commit()
        
    except Exception as e:
        logger.error(f"Critical error in job {job_id}: {str(e)}")
        try:
            if job:
                job.status = "error"
                job.error_message = f"Critical error: {str(e)}"
                job.updated_at = datetime.now(timezone.utc)
                db.commit()
        except:
            logger.error(f"Failed to update job {job_id} status after error")
    finally:
        db.close()

def enqueue_job(background_tasks: BackgroundTasks, job_id: str, db_session_factory):
    background_tasks.add_task(run_job_background, job_id, db_session_factory)
    logger.info(f"Enqueued job {job_id}")

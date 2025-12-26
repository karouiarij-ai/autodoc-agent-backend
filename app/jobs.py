"""Background job logic for documentation generation"""
import time
import threading
from sqlalchemy.orm import Session

from app import models


def create_documentation_job(db: Session, repo_url: str) -> models.Job:
    """Create a new documentation generation job"""
    # Create job record
    job = models.Job(repo_url=repo_url, status="pending")
    db.add(job)
    db.commit()
    db.refresh(job)
    
    # Start background task
    thread = threading.Thread(target=process_job, args=(job.id, repo_url))
    thread.daemon = True
    thread.start()
    
    return job


def process_job(job_id: int, repo_url: str):
    """Background task to process documentation generation"""
    from app.db import SessionLocal
    
    db = SessionLocal()
    try:
        # Update status to processing
        job = db.query(models.Job).filter(models.Job.id == job_id).first()
        if job:
            job.status = "processing"
            db.commit()
        
        # Simulate long-running task (replace with actual documentation generation)
        time.sleep(10)
        
        # Update status to completed
        job = db.query(models.Job).filter(models.Job.id == job_id).first()
        if job:
            job.status = "completed"
            job.result_url = f"https://docs.example.com/{job_id}"
            db.commit()
            
    except Exception as e:
        # Handle errors
        job = db.query(models.Job).filter(models.Job.id == job_id).first()
        if job:
            job.status = "failed"
            db.commit()
    finally:
        db.close()

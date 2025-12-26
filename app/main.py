from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from .db import Base, engine, SessionLocal
from . import models, schemas
from .jobs import create_job, enqueue_job

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Autodoc Agent Backend")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/jobs", response_model=schemas.JobResponse)
def create_job_endpoint(
    payload: schemas.CreateJobRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    job_id = create_job(db, payload.repo_url)
    enqueue_job(background_tasks, job_id, SessionLocal)

    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    return schemas.JobResponse(
        id=job.id,
        repo_url=job.repo_url,
        status=job.status,
        result_url=job.result_url,
    )

@app.get("/jobs/{job_id}", response_model=schemas.JobResponse)
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return schemas.JobResponse(
        id=job.id,
        repo_url=job.repo_url,
        status=job.status,
        result_url=job.result_url,
    )

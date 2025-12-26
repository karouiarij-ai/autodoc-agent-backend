"""FastAPI application with job management endpoints"""
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.db import engine, get_db
from app.jobs import create_documentation_job

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AutoDoc Agent Backend",
    description="Automated documentation generation service",
    version="1.0.0"
)


@app.get("/")
def read_root():
    """Health check endpoint"""
    return {"message": "AutoDoc Agent Backend is running", "status": "healthy"}


@app.post("/jobs", response_model=schemas.JobResponse, status_code=201)
def create_job(job_request: schemas.CreateJobRequest, db: Session = Depends(get_db)):
    """Create a new documentation generation job"""
    job = create_documentation_job(db, job_request.repo_url)
    return job


@app.get("/jobs", response_model=List[schemas.JobResponse])
def list_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all documentation jobs"""
    jobs = db.query(models.Job).offset(skip).limit(limit).all()
    return jobs


@app.get("/jobs/{job_id}", response_model=schemas.JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get job details by ID"""
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

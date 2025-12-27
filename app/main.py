import logging
from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .db import Base, engine, SessionLocal
from . import models, schemas
from .jobs import create_job, enqueue_job

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Autodoc Agent Backend",
    description="API for autonomous codebase documentation generation",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    try:
        job_id = create_job(db, payload.repo_url)
        enqueue_job(background_tasks, job_id, SessionLocal)

        job = db.query(models.Job).filter(models.Job.id == job_id).first()
        return schemas.JobResponse(
            id=job.id,
            repo_url=job.repo_url,
            status=job.status,
            result_url=job.result_url,
            error_message=job.error_message,
        )
    except Exception as e:
        logger.error(f"Error creating job: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create job: {str(e)}")

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
        error_message=job.error_message,
    )

@app.get("/health")
def health_check():
    return {"status": "healthy"}

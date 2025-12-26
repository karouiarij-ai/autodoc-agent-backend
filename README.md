# Autonomous Codebase Documenter – Backend

FastAPI + SQLite backend for submitting GitHub repositories as jobs and polling their status.

## Features

- Submit GitHub repository URLs for documentation generation
- Background job processing with status tracking
- RESTful API endpoints for job creation and status polling
- SQLite database for persistent job storage

## Endpoints

### POST /jobs
Create a new documentation generation job.

**Request:**
```json
{
  "repo_url": "https://github.com/username/repository"
}
```

**Response:**
```json
{
  "id": "uuid-string",
  "repo_url": "https://github.com/username/repository",
  "status": "pending",
  "result_url": null
}
```

### GET /jobs/{job_id}
Get the status of a specific job.

**Response:**
```json
{
  "id": "uuid-string",
  "repo_url": "https://github.com/username/repository",
  "status": "done",
  "result_url": "https://example.com/docs/demo"
}
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
uvicorn app.main:app --reload
```

3. Access the API at `http://localhost:8000`

4. View interactive API docs at `http://localhost:8000/docs`

## Job Status Flow

- **pending**: Job created, waiting to start
- **running**: Job is being processed
- **done**: Job completed successfully

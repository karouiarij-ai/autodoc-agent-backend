from pydantic import BaseModel, HttpUrl
from typing import Optional

class CreateJobRequest(BaseModel):
    repo_url: HttpUrl

class JobResponse(BaseModel):
    id: str
    repo_url: HttpUrl
    status: str
    result_url: Optional[str] = None

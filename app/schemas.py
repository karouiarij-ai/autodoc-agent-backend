from pydantic import BaseModel, HttpUrl, field_validator
from typing import Optional

class CreateJobRequest(BaseModel):
    repo_url: HttpUrl

class JobResponse(BaseModel):
    id: str
    repo_url: str
    status: str
    result_url: Optional[str] = None
    error_message: Optional[str] = None
    
    class Config:
        from_attributes = True

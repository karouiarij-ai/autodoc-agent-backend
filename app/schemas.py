"""Pydantic schemas for request/response validation"""
from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional


class CreateJobRequest(BaseModel):
    """Schema for creating a new job"""
    repo_url: str

    class Config:
        json_schema_extra = {
            "example": {
                "repo_url": "https://github.com/username/repository"
            }
        }


class JobResponse(BaseModel):
    """Schema for job response"""
    id: int
    repo_url: str
    status: str
    result_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

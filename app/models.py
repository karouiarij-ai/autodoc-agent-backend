"""SQLAlchemy database models"""
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db import Base


class Job(Base):
    """Job model for documentation generation tasks"""
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    repo_url = Column(String, nullable=False, index=True)
    status = Column(String, default="pending")  # pending, processing, completed, failed
    result_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

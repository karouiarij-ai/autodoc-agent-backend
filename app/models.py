from sqlalchemy import Column, String, DateTime
from datetime import datetime
from .db import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    repo_url = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")
    result_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

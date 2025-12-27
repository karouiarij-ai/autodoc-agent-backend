import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Use absolute path for database to avoid creating multiple databases
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "jobs.db"

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", f"sqlite:///{DATABASE_PATH}"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

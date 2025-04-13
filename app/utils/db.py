import json
import os
from typing import Dict, Any, Optional
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Ensure the database directory exists
os.makedirs('db', exist_ok=True)

# Database URL
DATABASE_URL = "sqlite:///resume.db"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create declarative base
Base = declarative_base()

# Define Resume model
class ResumeSection(Base):
    __tablename__ = "resume"
    
    id = Column(Integer, primary_key=True)
    section = Column(String, nullable=False, unique=True)
    data = Column(Text, nullable=False)
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the SQLAlchemy database with required tables."""
    Base.metadata.create_all(bind=engine)

def get_resume_section(section: str) -> Optional[Dict[str, Any]]:
    """Get a specific section of the resume from the database using SQLAlchemy."""
    session = SessionLocal()
    try:
        result = session.query(ResumeSection).filter(ResumeSection.section == section).first()
        if result:
            return json.loads(result.data)
        return None
    finally:
        session.close()

def get_full_resume() -> Dict[str, Any] | None:
    """Get the complete resume by combining all sections using SQLAlchemy."""
    session = SessionLocal()
    try:
        results = session.query(ResumeSection).all()
        resume = {}
        for section_obj in results:
            resume[section_obj.section] = json.loads(section_obj.data)
        return resume
    finally:
        session.close()

def save_resume_section(section: str, data: Dict[str, Any]):
    """Save or update a section of the resume in the database using SQLAlchemy."""
    session = SessionLocal()
    try:
        data_json = json.dumps(data)
        existing = session.query(ResumeSection).filter(ResumeSection.section == section).first()
        
        if existing:
            existing.data = data_json
        else:
            new_section = ResumeSection(section=section, data=data_json)
            session.add(new_section)
        
        session.commit()
    finally:
        session.close()

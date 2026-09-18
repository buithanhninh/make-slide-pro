"""
web/database.py
Multi-Tenant Database Engine & Relational Models for Make Slide Pro SaaS
Supports SQLite for lightweight/local operation and PostgreSQL for cloud scaling.
"""

from __future__ import annotations

import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "make_slide_pro.db"
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DB_PATH}")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ---------------------------------------------------------------------------
# Multi-Tenant Data Models
# ---------------------------------------------------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), default="")
    role = Column(String(50), default="USER")  # USER | ADMIN
    tier = Column(String(50), default="FREE")  # FREE | PRO | ENTERPRISE
    credits = Column(Integer, default=5)  # 5 free credits on sign up
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")


class Project(Base):
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), index=True, nullable=False)
    title = Column(String(255), nullable=False)
    source_filename = Column(String(255), default="")
    depth_mode = Column(String(50), default="DEEP")  # DEEP | BRIEF
    status = Column(String(50), default="DRAFT")  # DRAFT | BLUEPRINT_READY | RENDERING | COMPLETED | FAILED
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="projects")
    blueprint = relationship("Blueprint", back_populates="project", uselist=False, cascade="all, delete-orphan")
    render_jobs = relationship("RenderJob", back_populates="project", cascade="all, delete-orphan")


class Blueprint(Base):
    __tablename__ = "blueprints"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id"), unique=True, nullable=False)
    total_slides = Column(Integer, default=0)
    macc_score = Column(Float, default=100.0)
    slides_data = Column(Text, default="[]")  # Serialized JSON list of slides
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    project = relationship("Project", back_populates="blueprint")

    def get_slides(self) -> List[Dict[str, Any]]:
        try:
            return json.loads(self.slides_data)
        except Exception:
            return []

    def set_slides(self, slides: List[Dict[str, Any]]):
        self.slides_data = json.dumps(slides, ensure_ascii=False)
        self.total_slides = len(slides)


class RenderJob(Base):
    __tablename__ = "render_jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    theme = Column(String(50), default="ALL")  # ALL | DARK | LIGHT
    progress_percent = Column(Integer, default=0)
    current_stage = Column(String(100), default="INIT")
    error_message = Column(Text, nullable=True)
    slide_previews_data = Column(Text, default="{}")  # JSON: { DARK: [...], LIGHT: [...] }
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    project = relationship("Project", back_populates="render_jobs")

    def get_previews(self) -> Dict[str, Any]:
        try:
            return json.loads(self.slide_previews_data)
        except Exception:
            return {}

    def set_previews(self, previews: Dict[str, Any]):
        self.slide_previews_data = json.dumps(previews, ensure_ascii=False)


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    payment_ref = Column(String(100), unique=True, nullable=False)
    amount = Column(Integer, default=0)
    credits_added = Column(Integer, default=0)
    status = Column(String(50), default="PENDING")  # PENDING | SUCCESS | FAILED
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Initializes all database tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency generator for FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

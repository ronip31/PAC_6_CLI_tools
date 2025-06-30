from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    last_update = Column(DateTime, default=datetime.utcnow)
    metrics = relationship("Metric", back_populates="project", cascade="all, delete-orphan")

class Metric(Base):
    __tablename__ = 'metrics'
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)
    data = Column(JSON)
    hash = Column(String, index=True)
    project = relationship("Project", back_populates="metrics") 
from sqlalchemy.orm import Session
from . import models, schemas
from hashlib import sha256

def get_project_by_name(db: Session, name: str):
    return db.query(models.Project).filter(models.Project.name == name).first()

def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(name=project.name)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def add_metric(db: Session, project: models.Project, metric: schemas.MetricCreate):
    metric_hash = sha256((str(metric.data) + str(metric.timestamp)).encode()).hexdigest()
    exists = db.query(models.Metric).filter_by(project_id=project.id, hash=metric_hash).first()
    if exists:
        return None
    db_metric = models.Metric(
        project_id=project.id,
        timestamp=metric.timestamp,
        data=metric.data,
        hash=metric_hash
    )
    db.add(db_metric)
    project.last_update = metric.timestamp
    db.commit()
    db.refresh(db_metric)
    return db_metric

def get_projects(db: Session):
    return db.query(models.Project).all()

def get_project_metrics(db: Session, project_id: int):
    return db.query(models.Metric).filter(models.Metric.project_id == project_id).all() 
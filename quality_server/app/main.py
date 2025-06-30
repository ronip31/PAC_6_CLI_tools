from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from . import models, schemas, crud, database
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from fastapi.responses import HTMLResponse
from fastapi.requests import Request as FastAPIRequest

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post(
    "/projects",
    response_model=schemas.Project,
    summary="Cadastrar projeto e métricas",
    description="Recebe um projeto e suas métricas no formato amigável. Veja o exemplo abaixo.",
    response_description="Projeto cadastrado com sucesso",
)
def create_project(
    project: schemas.ProjectCreate = Body(
        ...,
        example={
            "name": "MeuProjeto",
            "metrics": [
                {
                    "timestamp": "2024-05-20T12:00:00",
                    "data": {
                        "lines": 100,
                        "comments": 10,
                        "functions": 5
                    }
                }
            ]
        }
    ),
    db: Session = Depends(get_db)
):
    if not project.metrics:
        raise HTTPException(status_code=400, detail="O projeto deve conter pelo menos uma métrica.")
    db_project = crud.get_project_by_name(db, project.name)
    if not db_project:
        db_project = crud.create_project(db, project)
    # Adiciona métricas (deduplicando)
    for metric in project.metrics:
        crud.add_metric(db, db_project, metric)
    return db_project

@app.get("/projects", response_model=list[schemas.Project])
def list_projects(request: FastAPIRequest, db: Session = Depends(get_db)):
    accept = request.headers.get("accept", "")
    projects = crud.get_projects(db)
    if "text/html" in accept:
        return templates.TemplateResponse("projects.html", {"request": request, "projects": projects})
    return projects

@app.get("/projects/{project_id}/history", response_model=list[schemas.Metric])
def project_history(project_id: int, db: Session = Depends(get_db)):
    return crud.get_project_metrics(db, project_id)

@app.post("/upload-raw")
def upload_raw(raw: dict = Body(...), db: Session = Depends(get_db)):
    # Validação básica
    if "timestamp" not in raw or "metrics" not in raw or "file_analyzed" not in raw["metrics"] or "metrics" not in raw["metrics"]:
        raise HTTPException(status_code=400, detail="Formato inválido")
    # Monta o payload no formato esperado
    payload = {
        "name": raw["metrics"]["file_analyzed"],
        "metrics": [
            {
                "timestamp": raw["timestamp"],
                "data": raw["metrics"]["metrics"]
            }
        ]
    }
    from .schemas import ProjectCreate
    project = ProjectCreate(**payload)
    db_project = crud.get_project_by_name(db, project.name)
    if not db_project:
        db_project = crud.create_project(db, project)
    for metric in project.metrics:
        crud.add_metric(db, db_project, metric)
    return {"message": "Projeto salvo com sucesso!", "project": db_project.name}

def remove_inactive_projects():
    db = database.SessionLocal()
    try:
        threshold = datetime.utcnow() - timedelta(days=7)
        projects = crud.get_projects(db)
        for project in projects:
            if project.last_update < threshold:
                db.delete(project)
        db.commit()
    finally:
        db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(remove_inactive_projects, 'interval', days=1)
scheduler.start() 
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime

class MetricBase(BaseModel):
    timestamp: datetime = Field(..., example="2024-05-20T12:00:00")
    data: Dict[str, Any] = Field(..., example={
        "lines": 100,
        "comments": 10,
        "functions": 5
    })

class MetricCreate(MetricBase):
    pass

class Metric(MetricBase):
    id: int
    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    name: str = Field(..., example="MeuProjeto")

class ProjectCreate(ProjectBase):
    metrics: List[MetricCreate] = Field(..., example=[
        {
            "timestamp": "2024-05-20T12:00:00",
            "data": {
                "lines": 100,
                "comments": 10,
                "functions": 5
            }
        }
    ])

class Project(ProjectBase):
    id: int
    last_update: datetime
    metrics: List[Metric] = []
    class Config:
        orm_mode = True 
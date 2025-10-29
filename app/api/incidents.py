from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.db import models
from app.schemas.incidents import IncidentCreate, IncidentRead

router = APIRouter()


@router.post("/", response_model=IncidentRead)
def create_incident(incident: IncidentCreate, db: Session = Depends(get_db)):
    service = (
        db.query(models.Service)
        .filter(models.Service.id == incident.service_id)
        .first()
    )
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    db_incident = models.Incident(**incident.model_dump())
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident


@router.get("/", response_model=List[IncidentRead])
def list_incidents(db: Session = Depends(get_db)):
    return db.query(models.Incident).all()


@router.get("/{incident_id}", response_model=IncidentRead)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = (
        db.query(models.Incident).filter(models.Incident.id == incident_id).first()
    )
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

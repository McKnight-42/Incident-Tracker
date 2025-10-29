from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from app.db.session import get_db
from app.db import models
from app.schemas.services import ServiceCreate, ServiceRead

router = APIRouter()


@router.post("/", response_model=ServiceRead)
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    db_service = models.Service(**service.model_dump())
    db.add(db_service)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Service with this name already exists"
        )
    db.refresh(db_service)
    return db_service


@router.get("/", response_model=List[ServiceRead])
def list_services(db: Session = Depends(get_db)):
    return db.query(models.Service).all()


@router.get("/{service_id}", response_model=ServiceRead)
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

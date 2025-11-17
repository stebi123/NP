from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.consumer import Consumer
from app.schemas.consumer import ConsumerCreate, ConsumerResponse
from app.core.database import get_db
from app.core.security import get_current_user
from typing import List

router = APIRouter(
    prefix="/consumers",
    tags=["Consumers"]
)

@router.post("/", response_model=ConsumerResponse)
def create_consumer(
    consumer: ConsumerCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    new_consumer = Consumer(**consumer.dict())
    db.add(new_consumer)
    db.commit()
    db.refresh(new_consumer)
    return new_consumer


@router.get("/", response_model=List[ConsumerResponse])
def get_consumers(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Consumer).all()


@router.get("/{consumer_id}", response_model=ConsumerResponse)
def get_consumer(
    consumer_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    consumer = db.query(Consumer).filter(Consumer.id == consumer_id).first()
    if not consumer:
        raise HTTPException(404, "Consumer not found")
    return consumer

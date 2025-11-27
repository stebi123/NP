from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import batch as models
from app.models.products import Product
from app.schemas import batch as schemas
from app.core.database import get_db
from app.core.security import get_current_user
from typing import List

router = APIRouter(
    prefix="/batches",
    tags=["Batches"]
)


#  Create a new batch
@router.post("/", response_model=List[schemas.BatchResponse])
def create_batches(
    batches: List[schemas.BatchCreate],
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    created_batches = []

    try:
        for batch in batches:
            # Optional: Check if product exists before linking
            product = db.query(Product).filter(Product.id == batch.product_id).first()
            if not product:
                raise HTTPException(status_code=400, detail=f"Product ID '{batch.product_id}' not found")

            new_batch = models.Batch(**batch.dict())
            db.add(new_batch)
            created_batches.append(new_batch)

        db.commit()

        # Refresh all new objects to return their IDs
        for batch in created_batches:
            db.refresh(batch)

        return created_batches

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


#  Get all batches
@router.get("/", response_model=list[schemas.BatchResponse])
def get_batches(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(models.Batch).all()


#  Get batch by ID
@router.get("/{batch_id}", response_model=schemas.BatchResponse)
def get_batch(
    batch_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    batch = db.query(models.Batch).filter(models.Batch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found")
    return batch


#  Update batch
@router.put("/{batch_id}", response_model=schemas.BatchResponse)
def update_batch(
    batch_id: int,
    updated_data: schemas.BatchCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    batch = db.query(models.Batch).filter(models.Batch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found")

    for key, value in updated_data.dict().items():
        setattr(batch, key, value)

    db.commit()
    db.refresh(batch)
    return batch


#  Delete batch
@router.delete("/{batch_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_batch(
    batch_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    batch = db.query(models.Batch).filter(models.Batch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Batch not found")

    db.delete(batch)
    db.commit()
    return {"detail": "Batch deleted successfully"}

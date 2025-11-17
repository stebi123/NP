from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.batch_pallet import BatchPallet
from app.models.batch import Batch
from app.models.pallet import Pallet
from app.schemas.batch_pallet import BatchPalletCreate, BatchPalletResponse
from app.core.database import get_db
from app.core.security import get_current_user

router = APIRouter(
    prefix="/batch-pallet",
    tags=["Batch-Pallet Mapping"]
)

# ✅ Create batch-pallet record
@router.post("/", response_model=BatchPalletResponse)
def create_batch_pallet(
    data: BatchPalletCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    # Validate batch
    batch = db.query(Batch).filter(Batch.id == data.batch_id).first()
    if not batch:
        raise HTTPException(400, "Batch does not exist")

    # Validate pallet
    pallet = db.query(Pallet).filter(Pallet.id == data.pallet_id).first()
    if not pallet:
        raise HTTPException(400, "Pallet does not exist")

    # Prevent duplicate mapping
    existing = db.query(BatchPallet).filter(
        BatchPallet.batch_id == data.batch_id,
        BatchPallet.pallet_id == data.pallet_id
    ).first()

    if existing:
        raise HTTPException(400, "Batch already stored in this pallet")

    # Validate quantity
    if data.quantity_left > batch.quantity:
        raise HTTPException(400, "Quantity exceeds batch total")

    new_entry = BatchPallet(**data.dict())
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry


# ✅ Get all
@router.get("/", response_model=List[BatchPalletResponse])
def get_all(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(BatchPallet).all()


# ✅ Get by ID
@router.get("/{id}", response_model=BatchPalletResponse)
def get_one(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    bp = db.query(BatchPallet).filter(BatchPallet.id == id).first()
    if not bp:
        raise HTTPException(404, "Batch-pallet record not found")
    return bp


# ✅ Update
@router.put("/{id}", response_model=BatchPalletResponse)
def update(
    id: int,
    data: BatchPalletCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    bp = db.query(BatchPallet).filter(BatchPallet.id == id).first()
    if not bp:
        raise HTTPException(404, "Record not found")

    # Validate quantity
    batch = db.query(Batch).filter(Batch.id == data.batch_id).first()
    if data.quantity_left > batch.quantity:
        raise HTTPException(400, "Quantity exceeds batch available")

    for k, v in data.dict().items():
        setattr(bp, k, v)

    db.commit()
    db.refresh(bp)
    return bp


# ✅ Delete
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    bp = db.query(BatchPallet).filter(BatchPallet.id == id).first()
    if not bp:
        raise HTTPException(404, "Record not found")

    db.delete(bp)
    db.commit()
    return {"detail": "Deleted"}

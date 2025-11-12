from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.staging import Staging
from app.models.products import Product
from app.models.warehouse import Warehouse
from app.schemas.staging import StagingCreate, StagingResponse
from app.core.database import get_db
from app.core.security import get_current_user

router = APIRouter(
    prefix="/staging",
    tags=["Staging"]
)

# ✅ Create staging entry
@router.post("/", response_model=StagingResponse, status_code=status.HTTP_201_CREATED)
def create_staging_entry(
    staging_data: StagingCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Validate product
    product = db.query(Product).filter(Product.id == staging_data.product_id).first()
    if not product:
        raise HTTPException(status_code=400, detail="Product ID not found")

    # Validate warehouse
    warehouse = db.query(Warehouse).filter(Warehouse.id == staging_data.warehouse_id).first()
    if not warehouse:
        raise HTTPException(status_code=400, detail="Warehouse ID not found")

    # Create staging record
    new_staging = Staging(**staging_data.dict())
    db.add(new_staging)
    db.commit()
    db.refresh(new_staging)
    return new_staging


# ✅ Get all staged entries
@router.get("/", response_model=List[StagingResponse])
def get_all_staged_items(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Staging).all()


# ✅ Get specific staging entry
@router.get("/{staging_id}", response_model=StagingResponse)
def get_staging_entry(
    staging_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    staging = db.query(Staging).filter(Staging.id == staging_id).first()
    if not staging:
        raise HTTPException(status_code=404, detail="Staging entry not found")
    return staging


# ✅ Update staging entry (for QC status or reassignment)
@router.put("/{staging_id}", response_model=StagingResponse)
def update_staging_entry(
    staging_id: int,
    updated_data: StagingCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    staging = db.query(Staging).filter(Staging.id == staging_id).first()
    if not staging:
        raise HTTPException(status_code=404, detail="Staging entry not found")

    # Update values
    for key, value in updated_data.dict().items():
        setattr(staging, key, value)

    db.commit()
    db.refresh(staging)
    return staging


# ✅ Mark QC done (shortcut endpoint)
@router.patch("/{staging_id}/qc", response_model=StagingResponse)
def mark_qc_done(
    staging_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    staging = db.query(Staging).filter(Staging.id == staging_id).first()
    if not staging:
        raise HTTPException(status_code=404, detail="Staging entry not found")

    staging.qc_done = True
    db.commit()
    db.refresh(staging)
    return staging


# ✅ Delete staging entry
@router.delete("/{staging_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_staging_entry(
    staging_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    staging = db.query(Staging).filter(Staging.id == staging_id).first()
    if not staging:
        raise HTTPException(status_code=404, detail="Staging entry not found")

    db.delete(staging)
    db.commit()
    return {"detail": "Staging entry deleted successfully"}

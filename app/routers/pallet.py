from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.pallet import Pallet
from app.models.warehouse import Warehouse
from app.schemas.pallet import PalletCreate, PalletResponse
from app.core.database import get_db
from app.core.security import get_current_user

router = APIRouter(
    prefix="/pallets",
    tags=["Pallets"]
)

#  Create Pallet
@router.post("/", response_model=PalletResponse, status_code=status.HTTP_201_CREATED)
def create_pallet(
    pallet: PalletCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Check duplicate pallet_id
    existing = db.query(Pallet).filter(Pallet.pallet_id == pallet.pallet_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Pallet ID already exists")

    # Check warehouse (optional but recommended)
    if pallet.warehouse_id:
        warehouse = db.query(Warehouse).filter(Warehouse.id == pallet.warehouse_id).first()
        if not warehouse:
            raise HTTPException(status_code=400, detail="Warehouse ID not found")

    new_pallet = Pallet(**pallet.dict())
    db.add(new_pallet)
    db.commit()
    db.refresh(new_pallet)
    return new_pallet


#  Get all Pallets
@router.get("/", response_model=List[PalletResponse])
def get_pallets(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Pallet).all()


#  Get Pallet by ID
@router.get("/{pallet_id}", response_model=PalletResponse)
def get_pallet(
    pallet_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    pallet = db.query(Pallet).filter(Pallet.id == pallet_id).first()
    if not pallet:
        raise HTTPException(status_code=404, detail="Pallet not found")
    return pallet


#  Update Pallet
@router.put("/{pallet_id}", response_model=PalletResponse)
def update_pallet(
    pallet_id: int,
    updated_pallet: PalletCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    pallet = db.query(Pallet).filter(Pallet.id == pallet_id).first()
    if not pallet:
        raise HTTPException(status_code=404, detail="Pallet not found")

    # Check warehouse if updated
    if updated_pallet.warehouse_id:
        warehouse = db.query(Warehouse).filter(Warehouse.id == updated_pallet.warehouse_id).first()
        if not warehouse:
            raise HTTPException(status_code=400, detail="Warehouse ID not found")

    for key, value in updated_pallet.dict().items():
        setattr(pallet, key, value)

    db.commit()
    db.refresh(pallet)
    return pallet


#  Delete Pallet
@router.delete("/{pallet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pallet(
    pallet_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    pallet = db.query(Pallet).filter(Pallet.id == pallet_id).first()
    if not pallet:
        raise HTTPException(status_code=404, detail="Pallet not found")

    db.delete(pallet)
    db.commit()
    return {"detail": "Pallet deleted successfully"}

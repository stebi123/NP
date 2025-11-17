from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.warehouse import Warehouse
from app.schemas.warehouse import WarehouseCreate, WarehouseResponse
from app.core.database import get_db
from app.core.security import get_current_user

router = APIRouter(
    prefix="/warehouse",
    tags=["Warehouse"]
)


# ✅ Create Warehouse
@router.post("/", response_model=WarehouseResponse, status_code=status.HTTP_201_CREATED)
def create_warehouse(
    warehouse: WarehouseCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    new_wh = Warehouse(**warehouse.dict())
    db.add(new_wh)
    db.commit()
    db.refresh(new_wh)
    return new_wh


# ✅ Get all Warehouses
@router.get("/", response_model=List[WarehouseResponse])
def get_all_warehouses(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Warehouse).all()


# ✅ Get Warehouse by ID
@router.get("/{warehouse_id}", response_model=WarehouseResponse)
def get_warehouse(
    warehouse_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    wh = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not wh:
        raise HTTPException(404, "Warehouse not found")
    return wh


# ✅ Update Warehouse
@router.put("/{warehouse_id}", response_model=WarehouseResponse)
def update_warehouse(
    warehouse_id: int,
    updated: WarehouseCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    wh = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not wh:
        raise HTTPException(404, "Warehouse not found")

    for key, value in updated.dict().items():
        setattr(wh, key, value)

    db.commit()
    db.refresh(wh)
    return wh


# ❌ Delete Warehouse (Soft Restriction)
# Warehouses may be linked to pallet, batch, company
# So we block delete unless you want cascade delete
@router.delete("/{warehouse_id}", status_code=status.HTTP_400_BAD_REQUEST)
def delete_warehouse_blocked():
    return {"detail": "Warehouse delete blocked — linked to other data. Use disable instead."}

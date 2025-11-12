from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.brand import Brand
from app.schemas.brand import BrandCreate, BrandResponse
from app.core.database import get_db
from app.core.security import get_current_user

router = APIRouter(
    prefix="/brands",
    tags=["Brands"]
)

# ✅ Create Brand
@router.post("/", response_model=BrandResponse, status_code=status.HTTP_201_CREATED)
def create_brand(
    brand: BrandCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    existing = db.query(Brand).filter(Brand.name == brand.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Brand already exists")

    new_brand = Brand(**brand.dict())
    db.add(new_brand)
    db.commit()
    db.refresh(new_brand)
    return new_brand


# ✅ Get all Brands
@router.get("/", response_model=List[BrandResponse])
def get_brands(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Brand).all()


# ✅ Get Brand by ID
@router.get("/{brand_id}", response_model=BrandResponse)
def get_brand(
    brand_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand


# ✅ Update Brand
@router.put("/{brand_id}", response_model=BrandResponse)
def update_brand(
    brand_id: int,
    updated_brand: BrandCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    brand.name = updated_brand.name
    db.commit()
    db.refresh(brand)
    return brand


# ✅ Delete Brand
@router.delete("/{brand_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_brand(
    brand_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    brand = db.query(Brand).filter(Brand.id == brand_id).first()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    db.delete(brand)
    db.commit()
    return {"detail": "Brand deleted successfully"}

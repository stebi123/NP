from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.subcategory import SubCategory
from app.models.category import Category
from app.schemas.subcategory import SubCategoryCreate, SubCategoryResponse
from app.core.database import get_db
from app.core.security import get_current_user

router = APIRouter(
    prefix="/subcategories",
    tags=["Subcategories"]
)

#  Create Subcategory
@router.post("/", response_model=SubCategoryResponse, status_code=status.HTTP_201_CREATED)
def create_subcategory(
    subcategory: SubCategoryCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Check if category exists
    category = db.query(Category).filter(Category.id == subcategory.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Category ID not found")

    # Check if subcategory with same name exists under this category
    existing = (
        db.query(SubCategory)
        .filter(SubCategory.name == subcategory.name, SubCategory.category_id == subcategory.category_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Subcategory already exists in this category")

    new_subcategory = SubCategory(**subcategory.dict())
    db.add(new_subcategory)
    db.commit()
    db.refresh(new_subcategory)
    return new_subcategory


#  Get all Subcategories
@router.get("/", response_model=List[SubCategoryResponse])
def get_subcategories(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(SubCategory).all()


#  Get Subcategory by ID
@router.get("/{subcategory_id}", response_model=SubCategoryResponse)
def get_subcategory(
    subcategory_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    subcategory = db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")
    return subcategory


#  Update Subcategory
@router.put("/{subcategory_id}", response_model=SubCategoryResponse)
def update_subcategory(
    subcategory_id: int,
    updated_subcategory: SubCategoryCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    subcategory = db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")

    # Ensure new category exists (if changed)
    category = db.query(Category).filter(Category.id == updated_subcategory.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Category ID not found")

    subcategory.name = updated_subcategory.name
    subcategory.category_id = updated_subcategory.category_id

    db.commit()
    db.refresh(subcategory)
    return subcategory


#  Delete Subcategory
@router.delete("/{subcategory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subcategory(
    subcategory_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    subcategory = db.query(SubCategory).filter(SubCategory.id == subcategory_id).first()
    if not subcategory:
        raise HTTPException(status_code=404, detail="Subcategory not found")

    db.delete(subcategory)
    db.commit()
    return {"detail": "Subcategory deleted successfully"}

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import products as models
from app.schemas import products as schemas
from app.core.security import get_current_user  # ✅ assuming you already have JWT auth here
from app.core.database import get_db
from typing import List

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# ✅ Create a new product
@router.post("/", response_model=List[schemas.ProductResponse])
def create_products(
    products: List[schemas.ProductCreate],
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    new_products = []
    for product in products:
        new_prod = models.Product(**product.dict())
        db.add(new_prod)
        new_products.append(new_prod)
    db.commit()
    for prod in new_products:
        db.refresh(prod)
    return new_products

# ✅ Get all products
@router.get("/", response_model=list[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    products = db.query(models.Product).all()
    return products


# ✅ Get single product by ID
@router.get("/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


# ✅ Update product by ID
@router.put("/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, updated_data: schemas.ProductCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    for key, value in updated_data.dict().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


# ✅ Delete product
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"detail": "Product deleted successfully"}

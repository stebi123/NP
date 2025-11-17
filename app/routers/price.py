from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.price import Price
from app.models.products import Product
from app.schemas.price import PriceCreate, PriceUpdate, PriceResponse
from app.core.database import get_db
from app.core.security import get_current_user

router = APIRouter(
    prefix="/prices",
    tags=["Prices"]
)

# ✅ Create price
@router.post("/", response_model=PriceResponse)
def create_price(
    price: PriceCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    product = db.query(Product).filter(Product.id == price.product_id).first()
    if not product:
        raise HTTPException(400, "Product not found")

    new_price = Price(**price.dict())
    db.add(new_price)
    db.commit()
    db.refresh(new_price)
    return new_price


# ✅ Get all prices
@router.get("/", response_model=List[PriceResponse])
def get_prices(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Price).all()


# ✅ Get price by ID
@router.get("/{price_id}", response_model=PriceResponse)
def get_price(
    price_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    price = db.query(Price).filter(Price.id == price_id).first()
    if not price:
        raise HTTPException(404, "Price record not found")
    return price


# ✅ Update price
@router.put("/{price_id}", response_model=PriceResponse)
def update_price(
    price_id: int,
    updated: PriceUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    price = db.query(Price).filter(Price.id == price_id).first()
    if not price:
        raise HTTPException(404, "Price record not found")

    for key, value in updated.dict(exclude_unset=True).items():
        setattr(price, key, value)

    db.commit()
    db.refresh(price)
    return price


# ❌ Delete not allowed (to preserve pricing history)
@router.delete("/{price_id}", status_code=400)
def delete_price_blocked():
    return {"detail": "Price deletion is blocked to preserve historical pricing."}

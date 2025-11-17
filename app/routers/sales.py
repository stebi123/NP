from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.sales import Sales
from app.models.batch import Batch
from app.models.pallet import Pallet
from app.models.consumer import Consumer
from app.models.products import Product
from app.models.batch_pallet import BatchPallet

from app.schemas.sales import SaleCreate, SaleResponse
from app.core.database import get_db
from app.core.security import get_current_user

from app.routers.sales_utils import get_batch_pallets_for_sale  # helper

router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)

@router.post("/", response_model=List[SaleResponse])
def create_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == sale.product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")

    consumer = db.query(Consumer).filter(Consumer.id == sale.consumer_id).first()
    if not consumer:
        raise HTTPException(400, "Consumer not found")

    pallets = get_batch_pallets_for_sale(db, sale.product_id, fifo=sale.fifo)

    if not pallets:
        raise HTTPException(400, "No stock available for this product")

    qty_to_sell = sale.quantity_sold
    sales_records = []

    for bp in pallets:
        if qty_to_sell <= 0:
            break

        deduct = min(bp.quantity_left, qty_to_sell)

        # Deduct from batch_pallet
        bp.quantity_left -= deduct

        # Deduct from batch
        batch = db.query(Batch).filter(Batch.batch_no == bp.batch_no).first()
        batch.quantity -= deduct

        # Create sales entry
        sale_entry = Sales(
            batch_id=batch.id,
            pallet_id=bp.pallet_id,
            product_id=sale.product_id,
            consumer_id=sale.consumer_id,
            quantity_sold=deduct,
            sale_price=sale.sale_price
        )
        db.add(sale_entry)
        sales_records.append(sale_entry)

        qty_to_sell -= deduct

        # Auto delete empty pallet records
        if bp.quantity_left == 0:
            db.delete(bp)

    if qty_to_sell > 0:
        raise HTTPException(400, "Not enough stock to complete sale")

    db.commit()

    for s in sales_records:
        db.refresh(s)

    return sales_records

@router.get("/", response_model=List[SaleResponse])
def get_all_sales(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Sales).all()

@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    sale = db.query(Sales).filter(Sales.id == sale_id).first()
    if not sale:
        raise HTTPException(404, "Sale not found")
    return sale

@router.put("/{sale_id}", response_model=SaleResponse)
def update_sale(
    sale_id: int,
    updated: SaleCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    sale = db.query(Sales).filter(Sales.id == sale_id).first()
    if not sale:
        raise HTTPException(404, "Sale not found")

    sale.consumer = updated.consumer
    sale.sale_price = updated.sale_price

    db.commit()
    db.refresh(sale)
    return sale

@router.delete("/{sale_id}", status_code=400)
def delete_sale_blocked():
    return {"detail": "Sale deletion is blocked to prevent stock corruption."}

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.models.sales import Sales
from app.models.batch import Batch
from app.models.pallet import Pallet
from app.models.consumer import Consumer
from app.models.products import Product
from app.models.batch_pallet import BatchPallet

from app.schemas.sales import SaleCreate, SaleResponse, SaleBulkRequest
from app.core.database import get_db
from app.core.security import get_current_user

from app.routers.sales_utils import get_batch_pallets_for_sale  # helper

router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)

# @router.post("/", response_model=List[SaleResponse])
# def create_sale(
#     sale: SaleCreate,
#     db: Session = Depends(get_db),
#     current_user: dict = Depends(get_current_user),
# ):
#     product = db.query(Product).filter(Product.id == sale.product_id).first()
#     if not product:
#         raise HTTPException(404, "Product not found")

#     consumer = db.query(Consumer).filter(Consumer.id == sale.consumer_id).first()
#     if not consumer:
#         raise HTTPException(400, "Consumer not found")

#     pallets = get_batch_pallets_for_sale(db, sale.product_id, fifo=sale.fifo)

#     if not pallets:
#         raise HTTPException(400, "No stock available for this product")

#     qty_to_sell = sale.quantity_sold
#     sales_records = []

#     for bp in pallets:
#         if qty_to_sell <= 0:
#             break

#         deduct = min(bp.quantity_left, qty_to_sell)

#         # Deduct from batch_pallet
#         bp.quantity_left -= deduct

#         # Deduct from batch
#         batch = db.query(Batch).filter(Batch.id == bp.batch_id).first()
#         batch.quantity -= deduct

#         # Create sales entry
#         sale_entry = Sales(
#             batch_id=batch.id,
#             pallet_id=bp.pallet_id,
#             product_id=sale.product_id,
#             consumer_id=sale.consumer_id,
#             quantity_sold=deduct,
#             sale_price=sale.sale_price
#         )
#         db.add(sale_entry)
#         sales_records.append(sale_entry)

#         qty_to_sell -= deduct

#         # Auto delete empty pallet records
#         if bp.quantity_left == 0:
#             db.delete(bp)

#     if qty_to_sell > 0:
#         raise HTTPException(400, "Not enough stock to complete sale")

#     db.commit()

#     for s in sales_records:
#         db.refresh(s)

#     return sales_records

@router.post("/bulk", response_model=List[SaleResponse])
def create_bulk_sale(
    request: SaleBulkRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    all_sales_records = []

    for sale in request.sales:

        # Validate product
        product = db.query(Product).filter(Product.id == sale.product_id).first()
        if not product:
            raise HTTPException(404, f"Product {sale.product_id} not found")

        # Validate consumer
        consumer = db.query(Consumer).filter(Consumer.id == sale.consumer_id).first()
        if not consumer:
            raise HTTPException(400, f"Consumer {sale.consumer_id} not found")

        # FIFO or FEFO batches/pallets
        pallets = get_batch_pallets_for_sale(db, sale.product_id, fifo=sale.fifo)

        if not pallets:
            raise HTTPException(400, f"No stock for product {sale.product_id}")

        qty_to_sell = sale.quantity_sold
        
        # Validate quantity does not exceed total available stock
        available_stock = sum(bp.quantity_left for bp in pallets)

        if sale.quantity_sold > available_stock:
            raise HTTPException( 400,f"Requested quantity {sale.quantity_sold} exceeds available stock {available_stock} for product {sale.product_id}")

        sales_records = []

        for bp in pallets:
            if qty_to_sell <= 0:
                break

            deduct = min(bp.quantity_left, qty_to_sell)

            # Reduce pallet quantity
            bp.quantity_left -= deduct

            # Reduce batch quantity
            batch = db.query(Batch).filter(Batch.id == bp.batch_id).first()
            batch.quantity -= deduct

            # Create sales record row
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

            # Remove empty pallet line
            if bp.quantity_left == 0:
                db.delete(bp)

        if qty_to_sell > 0:
            raise HTTPException(400, f"Not enough stock for product {sale.product_id}")

        all_sales_records.extend(sales_records)

    db.commit()

    for s in all_sales_records:
        db.refresh(s)

    return all_sales_records


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

#get total stock for a product
@router.get("/stock/total/{product_id}")
def get_total_stock_only(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Validate product
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")

    # Get all batches
    batches = db.query(Batch).filter(Batch.product_id == product_id).all()
    if not batches:
        return {
            "product_id": product_id,
            "product_name": product.name,
            "total_stock": 0
        }

    batch_ids = [b.id for b in batches]

    # Get stock from BatchPallet
    total_stock = (
        db.query(func.sum(BatchPallet.quantity_left))
        .filter(BatchPallet.batch_id.in_(batch_ids))
        .scalar()
    ) or 0

    return {
        "product_id": product_id,
        "product_name": product.name,
        "total_stock": total_stock
    }

#get detailed stock for a product

@router.get("/stock/details/{product_id}")
def get_stock_details(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Validate product
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")

    # Fetch batches
    batches = db.query(Batch).filter(Batch.product_id == product_id).all()
    if not batches:
        return {
            "product_id": product_id,
            "product_name": product.name,
            "total_stock": 0,
            "batches": []
        }

    batch_ids = [b.id for b in batches]

    # Fetch pallet stock entries
    batch_pallets = (
        db.query(BatchPallet)
        .filter(BatchPallet.batch_id.in_(batch_ids))
        .all()
    )

    total_stock = sum(bp.quantity_left for bp in batch_pallets)

    detailed = []
    for batch in batches:
        pallets_for_batch = [
            {
                "pallet_id": bp.pallet_id,
                "quantity_left": bp.quantity_left,
                "stored_on": bp.stored_on
            }
            for bp in batch_pallets if bp.batch_id == batch.id
        ]

        detailed.append({
            "batch_id": batch.id,
            "batch_no": batch.batch_no,
            "batch_total": sum(p["quantity_left"] for p in pallets_for_batch),
            "pallets": pallets_for_batch
        })

    return {
        "product_id": product_id,
        "product_name": product.name,
        "total_stock": total_stock,
        "batches": detailed
    }

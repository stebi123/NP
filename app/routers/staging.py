from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, date

from app.models.staging import Staging, QCStatus as QCStatusEnum
from app.models.products import Product
from app.models.warehouse import Warehouse
from app.schemas.staging import StagingCreate, StagingResponse, StagingQCUpdate, QCStatus, StagingBase
from app.core.database import get_db
from app.core.security import get_current_user

router = APIRouter(
    prefix="/staging",
    tags=["Staging"]
)

# Create a new staging entry
# QC fields are automatically set (qc_status=HOLD, qc_done_on=None, approved/rejected=0)
# Only allows product, warehouse, invoice_no, total_quantity

@router.post("/", response_model=StagingResponse, status_code=status.HTTP_201_CREATED)
def create_staging_entry(
    staging_data: StagingBase,
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

    # Create staging record using schema defaults
    new_staging = Staging(
        product_id=staging_data.product_id,
        warehouse_id=staging_data.warehouse_id,
        invoice_no=staging_data.invoice_no,
        received_on=staging_data.received_on,
        total_quantity=staging_data.total_quantity,
        qc_status=QCStatusEnum.HOLD,
        qc_done_on=None,
        approved_quantity=0,
        rejected_quantity=0
    )

    db.add(new_staging)
    db.commit()
    db.refresh(new_staging)
    return new_staging


# Update QC status and quantities
# Validates approved + rejected quantities against total_quantity from DB

@router.patch("/{staging_id}/qc", response_model=StagingResponse)
def update_qc(
    staging_id: int,
    qc_data: StagingQCUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    staging = db.query(Staging).filter(Staging.id == staging_id).first()
    if not staging:
        raise HTTPException(status_code=404, detail="Staging entry not found")

    # Validate quantities against total_quantity from DB
    if qc_data.approved_quantity + qc_data.rejected_quantity > staging.total_quantity:
        raise HTTPException(status_code=400, detail="Sum of approved and rejected exceeds total quantity")

    # Update QC fields
    staging.qc_status = QCStatusEnum[qc_data.qc_status.name]
    staging.qc_done_on = datetime.utcnow()
    staging.approved_quantity = qc_data.approved_quantity
    staging.rejected_quantity = qc_data.rejected_quantity

    db.commit()
    db.refresh(staging)
    return staging

# Get all staged entries
# Returns all staging records including QC and quantities

@router.get("/", response_model=List[StagingResponse])
def get_all_staged_items(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Staging).all()

# Get a specific staging entry by ID

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

# Update a staging entry (general fields)
# QC fields cannot be updated here

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

    for key, value in updated_data.dict().items():
        setattr(staging, key, value)

    db.commit()
    db.refresh(staging)
    return staging

# Delete a staging entry

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

# Filter staging entries
@router.get("/filter", response_model=List[StagingResponse])
def filter_staging_entries(
    qc_status: Optional[QCStatus] = Query(None, description="Filter by QC status"),
    invoice_no: Optional[str] = Query(None, description="Filter by invoice number"),
    product_id: Optional[int] = Query(None, description="Filter by product ID"),
    warehouse_id: Optional[int] = Query(None, description="Filter by warehouse ID"),
    date: Optional[date] = Query(None, description="Filter by exact received_on date"),
    start_date: Optional[datetime] = Query(None, description="Filter received_on from this date (inclusive)"),
    end_date: Optional[datetime] = Query(None, description="Filter received_on up to this date (inclusive)"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    query = db.query(Staging)

    # Apply filters
    if qc_status:
        query = query.filter(Staging.qc_status == QCStatusEnum[qc_status.name])
    if invoice_no:
        query = query.filter(Staging.invoice_no == invoice_no)
    if product_id:
        query = query.filter(Staging.product_id == product_id)
    if warehouse_id:
        query = query.filter(Staging.warehouse_id == warehouse_id)

    # Date filter logic
    if date:
        # Filter by exact date ignoring time
        query = query.filter(
            Staging.received_on == date
        )
    else:
        if start_date:
            query = query.filter(Staging.received_on >= start_date)
        if end_date:
            query = query.filter(Staging.received_on <= end_date)

    results = query.all()
    return results
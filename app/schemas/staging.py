from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional
from enum import Enum

# QCStatus Enum for Pydantic
class QCStatus(str, Enum):
    HOLD = "HOLD"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

# Base schema for shared fields
class StagingBase(BaseModel):
    product_id: int
    warehouse_id: int
    invoice_no: str
    received_on: date
    total_quantity: int

# Schema for creating a staging entry
# QC fields are automatically set and not allowed from client
class StagingCreate(StagingBase):
    qc_status: QCStatus = QCStatus.HOLD
    qc_done_on: datetime
    approved_quantity: int = 0
    rejected_quantity: int = 0

# Schema for QC updates
# Only QC-related fields allowed here
class StagingQCUpdate(BaseModel):
    qc_status: QCStatus
    approved_quantity: int
    rejected_quantity: int

# Schema for API response
# Includes all fields
class StagingResponse(StagingBase):
    id: int
    qc_status: QCStatus
    qc_done_on: Optional[datetime] = None
    approved_quantity: int
    rejected_quantity: int

    class Config:
        from_attributes = True
        use_enum_values = True
from pydantic import BaseModel
from typing import Optional
from datetime import date

class BatchBase(BaseModel):
    batch_no: str
    product_id: int
    manufacture_date: Optional[date] = None
    expiry_date: Optional[date] = None
    quantity: Optional[int] = None
    status: Optional[bool] = True
    sku: Optional[str] = None

class BatchCreate(BatchBase):
    pass

class BatchResponse(BatchBase):
    id: int

    class Config:
        from_attributes = True
  # replaces orm_mode in Pydantic v2


# prod_id → internal code for display
# product_id → FK to the product table
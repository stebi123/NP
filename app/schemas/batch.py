from pydantic import BaseModel, Field
from datetime import date

class BatchBase(BaseModel):
    batch_no: str
    prod_id: str
    manufacture_date: date
    quantity: int
    expiry_date: date
    status: bool = True
    sku: str = Field(..., pattern=r'^[A-Za-z0-9]+$', description="Alphanumeric SKU only")

class BatchCreate(BatchBase):
    pass

class BatchResponse(BatchBase):
    id: int

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2

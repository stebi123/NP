from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PriceBase(BaseModel):
    product_id: int
    mrp: float
    mwp: float

class PriceCreate(PriceBase):
    pass

class PriceUpdate(BaseModel):
    mrp: Optional[float] = None
    mwp: Optional[float] = None

class PriceResponse(PriceBase):
    id: int
    effective_from: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

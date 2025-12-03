from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SaleBase(BaseModel):
    product_id: int
    consumer_id: int
    quantity_sold: int
    sale_price: Optional[float] = None

class SaleCreate(SaleBase):
    fifo: bool = True   # FIFO=True, FEFO=False (expiry-based)

class SaleResponse(BaseModel):
    id: int
    batch_id: int
    pallet_id: Optional[int]
    product_id: int
    consumer_id: int
    quantity_sold: int
    sale_price: Optional[float]
    sale_timestamp: datetime
    
class SaleBulkRequest(BaseModel):
    sales: List[SaleCreate]

    class Config:
        from_attributes = True

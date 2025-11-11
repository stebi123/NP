from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BatchPalletBase(BaseModel):
    # matches your model that uses batch_no FK
    batch_no: str
    pallet_id: int
    quantity_left: Optional[int] = None
    stored_on: Optional[datetime] = None

class BatchPalletCreate(BatchPalletBase):
    pass

class BatchPalletResponse(BatchPalletBase):
    id: int

    class Config:
        from_attributes = True

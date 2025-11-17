from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BatchPalletBase(BaseModel):
    batch_id: int
    pallet_id: int
    quantity_left: int

class BatchPalletCreate(BatchPalletBase):
    pass

class BatchPalletResponse(BatchPalletBase):
    id: int
    stored_on: datetime

    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import Optional

class PalletBase(BaseModel):
    pallet_id: str
    # batch_id: int  # Foreign key to Batch
    dimensions: Optional[str] = None
    capacity: Optional[float] = None
    warehouse_id: Optional[int] = None

class PalletCreate(PalletBase):
    pass

class PalletResponse(PalletBase):
    id: int

    class Config:
        from_attributes = True

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class StagingBase(BaseModel):
    product_id: int
    warehouse_id: int
    received_on: Optional[datetime] = None
    qc_done: Optional[bool] = False

class StagingCreate(StagingBase):
    pass

class StagingResponse(StagingBase):
    id: int

    class Config:
        from_attributes = True

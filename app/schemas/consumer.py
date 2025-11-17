from pydantic import BaseModel
from typing import Optional

class ConsumerBase(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    company: Optional[str] = None

class ConsumerCreate(ConsumerBase):
    pass

class ConsumerResponse(ConsumerBase):
    id: int
    class Config:
        from_attributes = True

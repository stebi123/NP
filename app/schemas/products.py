from pydantic import BaseModel
from typing import Optional


# Base schema (shared properties)
class ProductBase(BaseModel):
    prod_id: str
    name: str
    description: Optional[str] = None
    company_id: int
    category: Optional[str] = None
    sub_category: Optional[str] = None
    unit_of_measure: Optional[str] = None
    weight: Optional[float] = None
    status: Optional[bool] = True
    expiry_in_months: Optional[int] = None
    upc: Optional[str] = None


# Schema for creating a new product
class ProductCreate(ProductBase):
    pass


# Schema for reading product data (response model)
class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True


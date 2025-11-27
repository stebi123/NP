from pydantic import BaseModel, Field
from typing import Optional


# Base schema (shared properties)
class ProductBase(BaseModel):
    prod_id: str
    name: str
    description: Optional[str] = None
    brand_id: int
    category_id: int
    subcategory_id: int
    unit_of_measure: Optional[str] = None
    weight: Optional[float] = None
    status: Optional[bool] = True
    expiry_in_months: Optional[int] = None
    upc: Optional[str] = None
    sku: str = Field(..., pattern=r'^[A-Za-z0-9-]+$', description="Alphanumeric SKU")


# Schema for creating a new product
class ProductCreate(ProductBase):
    pass

# Schema for reading product data (response model)
class ProductResponse(ProductBase):
    id: int
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


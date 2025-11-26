from pydantic import BaseModel

class BrandBase(BaseModel):
    name: str
    company_id: int

class BrandCreate(BrandBase):
    pass

class BrandResponse(BrandBase):
    id: int

    class Config:
        from_attributes = True

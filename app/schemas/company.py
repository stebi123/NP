from pydantic import BaseModel

class CompanyBase(BaseModel):
    name: str
    warehouse_id: int

class CompanyCreate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    id: int

    class Config:
        from_attributes = True

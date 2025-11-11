from pydantic import BaseModel

class WarehouseBase(BaseModel):
    name: str
    location: str
    address: str

class WarehouseCreate(WarehouseBase):
    pass

class WarehouseResponse(WarehouseBase):
    id: int

    class Config:
        from_attributes = True

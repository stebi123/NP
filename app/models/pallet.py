from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.core.database import Base

class Pallet(Base):
    __tablename__ = "pallet"

    id = Column(Integer, primary_key=True, index=True)
    pallet_id = Column(String(100), unique=True, nullable=False)
    dimensions = Column(String(100))
    capacity = Column(Float)
    warehouse_id = Column(Integer, ForeignKey("warehouse.id"))

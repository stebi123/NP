from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Warehouse(Base):
    __tablename__ = "warehouse"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    location = Column(String(255))
    address = Column(String(500))

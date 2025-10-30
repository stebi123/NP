from sqlalchemy import Column, Integer, String, Float, Boolean
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    prod_id = Column(String(100), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    company_id = Column(Integer, nullable=False)
    category = Column(String(100))
    sub_category = Column(String(100))
    unit_of_measure = Column(String(50))
    weight = Column(Float)
    status = Column(Boolean, default=True)
    expiry_in_months = Column(Integer)
    upc = Column(String(100), unique=True)
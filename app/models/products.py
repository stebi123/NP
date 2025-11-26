from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    prod_id = Column(String(100), unique=True, nullable=False) 
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    brand_id = Column(Integer, ForeignKey("brand.id"))  # replaced company_id
    category_id = Column(Integer, ForeignKey("category.id"))
    subcategory_id = Column(Integer, ForeignKey("subcategory.id"))
    unit_of_measure = Column(String(50))
    weight = Column(Float)
    status = Column(Boolean, default=True)
    expiry_in_months = Column(Integer)
    upc = Column(String(100), unique=True)
    sku = Column(String(50), unique=True, nullable=False)  # new field

    # Relationships can be defined here if needed   
    brand = relationship("Brand", back_populates="products")
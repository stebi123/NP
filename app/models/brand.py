from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Brand(Base):
    __tablename__ = "brand"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    company_id = Column(Integer, ForeignKey("company.id"), nullable=False)

    # Relationship object
    company = relationship("Company", back_populates="brands")
    products = relationship("Product", back_populates="brand")
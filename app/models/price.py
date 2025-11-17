from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Price(Base):
    __tablename__ = "price"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    mrp = Column(Float, nullable=False)   # Maximum Retail Price
    mwp = Column(Float, nullable=False)   # Minimum Wholesale Price
    effective_from = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

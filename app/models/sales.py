from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, String
from sqlalchemy.sql import func
from app.core.database import Base

class Sales(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)

    batch_id = Column(Integer, ForeignKey("batch.id"), nullable=False)
    pallet_id = Column(Integer, ForeignKey("pallet.id"), nullable=True)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    consumer_id = Column(Integer, ForeignKey("consumer.id"), nullable=False)
    quantity_sold = Column(Integer, nullable=False)
    sale_price = Column(Float, nullable=True)
    sale_timestamp = Column(DateTime(timezone=True), server_default=func.now())

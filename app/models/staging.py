from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class Staging(Base):
    __tablename__ = "staging"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    warehouse_id = Column(Integer, ForeignKey("warehouse.id"))
    received_on = Column(DateTime(timezone=True), server_default=func.now())
    qc_done = Column(Boolean, default=False)

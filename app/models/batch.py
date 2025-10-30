from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from app.core.database import Base
from app.models.products import Product

class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    batch_no = Column(String(50), unique=True, nullable=False)
    prod_id = Column(String(100), ForeignKey("products.prod_id"), nullable=False)
    manufacture_date = Column(Date, nullable=False)
    quantity = Column(Integer, nullable=False)
    expiry_date = Column(Date, nullable=False)
    status = Column(Boolean, default=True)
    sku = Column(String(50), nullable=False)

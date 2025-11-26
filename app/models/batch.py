from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from app.core.database import Base

class Batch(Base):
    __tablename__ = "batch"

    id = Column(Integer, primary_key=True, index=True)
    batch_no = Column(String(100), unique=True, nullable=False)
    product_id = Column(Integer, ForeignKey("product.id")) 
    manufacture_date = Column(Date)
    expiry_date = Column(Date)
    quantity = Column(Integer)
    status = Column(Boolean, default=True)
    sku = Column(String(50), nullable=False)
    invoice_id = Column(Integer, ForeignKey("invoice.id"))
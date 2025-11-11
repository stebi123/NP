from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class BatchPallet(Base):
    __tablename__ = "batch_pallet"

    id = Column(Integer, primary_key=True, index=True)
    batch_no = Column(String(100), ForeignKey("batch.batch_no"))
    pallet_id = Column(Integer, ForeignKey("pallet.id"))
    quantity_left = Column(Integer)
    stored_on = Column(DateTime(timezone=True), server_default=func.now())

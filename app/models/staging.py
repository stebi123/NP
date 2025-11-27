from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum

# Enum for QC status
class QCStatus(enum.Enum):
    HOLD = 1
    APPROVED = 2
    REJECTED = 3

class Staging(Base):
    __tablename__ = "staging"

    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    product_id = Column(Integer, ForeignKey("product.id"))
    warehouse_id = Column(Integer, ForeignKey("warehouse.id"))
    
    # Invoice number
    invoice_no = Column(String(50), nullable=False, index=True)
    
    # Date received
    received_on = Column(DateTime(timezone=True), server_default=func.now())
    
    # QC fields
    qc_status = Column(Enum(QCStatus), default=QCStatus.HOLD)
    qc_done_on = Column(DateTime(timezone=True))
    
    # Quantity fields
    total_quantity = Column(Integer, default=0)
    approved_quantity = Column(Integer, default=0)
    rejected_quantity = Column(Integer, default=0) # Damaged products included

    # First entry timestamp (always auto-set on creation)
    first_entered_on = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
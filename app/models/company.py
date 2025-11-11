from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    warehouse_id = Column(Integer)

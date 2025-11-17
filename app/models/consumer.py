from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Consumer(Base):
    __tablename__ = "consumer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    address = Column(String(500), nullable=True)
    company = Column(String(255), nullable=True)

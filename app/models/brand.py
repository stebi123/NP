from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Brand(Base):
    __tablename__ = "brand"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)

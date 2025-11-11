from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class SubCategory(Base):
    __tablename__ = "subcategory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"))

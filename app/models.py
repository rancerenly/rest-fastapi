from sqlalchemy import Column, Integer, String
from .database import Base

class Term(Base):
    __tablename__ = 'terms'

    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, index=True)
    description = Column(String)

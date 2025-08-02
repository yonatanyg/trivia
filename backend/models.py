from sqlalchemy import Column, Integer, String
from .database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    director = Column(String, nullable=False)

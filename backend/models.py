from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    director = Column(String, index=True)

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)

    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    answer = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False)

    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)

    question = relationship("Question", back_populates="answers")

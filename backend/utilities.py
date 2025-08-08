"""
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



"""
def correctAnswersId(Question):
    """
    returns list of correct answers ids
    """
    return [answer.id for answer in Question.answers if answer.is_correct]
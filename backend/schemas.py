from pydantic import BaseModel
from typing import List, Optional

class AnswerBase(BaseModel):
    answer: str
    is_correct: bool

class AnswerCreate(AnswerBase):
    pass

class Answer(AnswerBase):
    id: int
    question_id: int

    class Config:
        orm_mode = True
        from_attributes = True


class QuestionBase(BaseModel):
    question: str
    genre: Optional[str] = None  # New field

class QuestionCreate(QuestionBase):
    answers: List[AnswerCreate]

class Question(QuestionBase):
    id: int
    answers: List[Answer] = []

    class Config:
        orm_mode = True
        from_attributes = True


class ScoreboardBase(BaseModel):
    nickname: str
    score: float = 0.0

class ScoreboardCreate(ScoreboardBase):
    pass

class Scoreboard(ScoreboardBase):
    class Config:
        orm_mode = True
        from_attributes = True

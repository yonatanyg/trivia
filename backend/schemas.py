from pydantic import BaseModel
from typing import List, Optional

class MovieBase(BaseModel):
    name: str
    director: str

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int

    class Config:
        orm_mode = True

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

class QuestionBase(BaseModel):
    question: str

class QuestionCreate(QuestionBase):
    answers: List[AnswerCreate]

class Question(QuestionBase):
    id: int
    answers: List[Answer] = []

    class Config:
        orm_mode = True


# Room schemas

class ParticipantBase(BaseModel):
    name: str

class ParticipantCreate(ParticipantBase):
    pass

class Participant(ParticipantBase):
    id: int
    room_id: int

    class Config:
        orm_mode = True

class RoomBase(BaseModel):
    code: str
    state: Optional[str] = "waiting"

class RoomCreate(BaseModel):
    code: str

class Room(RoomBase):
    id: int
    participants: List[Participant] = []

    class Config:
        orm_mode = True

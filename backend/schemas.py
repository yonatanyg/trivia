from pydantic import BaseModel

class MovieBase(BaseModel):
    name: str
    director: str

class MovieCreate(MovieBase):
    pass  # for now same as base, but separated for clarity

class Movie(MovieBase):
    id: int

    class Config:
        orm_mode = True  # this allows SQLAlchemy models to be converted to Pydantic

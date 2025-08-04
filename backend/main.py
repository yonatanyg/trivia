from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas, crud, database, seed

from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Add this middleware configuration BEFORE your routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # or list specific methods
    allow_headers=["*"],  # or list specific headers
)

@app.on_event("startup")
def startup_event():
    db = next(database.get_db())
    seed.seed_data(db)

@app.get("/movies/", response_model=list[schemas.Movie])
def read_movies(db: Session = Depends(database.get_db)):
    return crud.get_movies(db)

@app.post("/movies/", response_model=schemas.Movie)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(database.get_db)):
    return crud.create_movie(db, movie)

@app.get("/questions/", response_model=list[schemas.Question])
def read_questions(db: Session = Depends(database.get_db)):
    return crud.get_questions(db)

@app.post("/questions/", response_model=schemas.Question)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(database.get_db)):
    return crud.create_question(db, question)
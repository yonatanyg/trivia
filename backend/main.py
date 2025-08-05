from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas, crud, database, seed

from fastapi.middleware.cors import CORSMiddleware

# Create tables if not exist
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event to seed DB
@app.on_event("startup")
def startup_event():
    db = next(database.get_db())
    seed.seed_data(db)

# -----------------------------
# Movies Endpoints
# -----------------------------
@app.get("/movies/", response_model=list[schemas.Movie])
def read_movies(db: Session = Depends(database.get_db)):
    return crud.get_movies(db)

@app.post("/movies/", response_model=schemas.Movie)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(database.get_db)):
    return crud.create_movie(db, movie)

# -----------------------------
# Questions Endpoints
# -----------------------------
@app.get("/questions/", response_model=list[schemas.Question])
def read_questions(db: Session = Depends(database.get_db)):
    return crud.get_questions(db)

@app.post("/questions/", response_model=schemas.Question)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(database.get_db)):
    return crud.create_question(db, question)

# -----------------------------
# Rooms Endpoints
# -----------------------------
@app.post("/rooms/", response_model=schemas.Room)
def create_room(room: schemas.RoomCreate = None, db: Session = Depends(database.get_db)):
    return crud.create_room(db, room)

@app.get("/rooms/", response_model=list[schemas.Room])
def list_rooms(db: Session = Depends(database.get_db)):
    return crud.get_rooms(db)

@app.get("/rooms/{code}", response_model=schemas.Room)
def get_room(code: str, db: Session = Depends(database.get_db)):
    db_room = crud.get_room_by_code(db, code)
    if not db_room:
        return {"error": "Room not found"}
    return db_room

@app.put("/rooms/{code}/state", response_model=schemas.Room)
def update_room_state(code: str, state: str, db: Session = Depends(database.get_db)):
    return crud.update_room_state(db, code, state)

@app.delete("/rooms/{code}", response_model=schemas.Room)
def delete_room(code: str, db: Session = Depends(database.get_db)):
    return crud.delete_room(db, code)


# -----------------------------
# Participants Endpoints
# -----------------------------
@app.post("/rooms/{code}/participants", response_model=schemas.Participant)
def add_participant(code: str, participant: schemas.ParticipantCreate, db: Session = Depends(database.get_db)):
    return crud.add_participant(db, code, participant)

@app.get("/rooms/{code}/participants", response_model=list[schemas.Participant])
def list_participants(code: str, db: Session = Depends(database.get_db)):
    return crud.get_participants(db, code)

@app.delete("/participants/{participant_id}", response_model=schemas.Participant)
def remove_participant(participant_id: int, db: Session = Depends(database.get_db)):
    return crud.remove_participant(db, participant_id)


from fastapi import FastAPI, Depends, HTTPException
import logging
from sqlalchemy.orm import Session
import models, schemas, crud, database, seed

import os

from fastapi.middleware.cors import CORSMiddleware
from room_manager import room_manager
# Create tables if not exist
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FRONTEND_URLS = os.getenv("FRONTEND_URLS", "http://localhost:5173,http://localhost:5174")

allow_origins = [origin.strip() for origin in FRONTEND_URLS.split(",")]


app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
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

# -------- Rooms Endpoints (no DB, use room_manager) --------

@app.post("/rooms/")
def create_room():
    logger.info("Test")
    room = room_manager.create_room()
    return {
        "code": room.code,
        "state": room.state,
        "participants": list(room.participants.values())
    }

@app.get("/rooms/")
def list_rooms():
    return [
        {
            "code": room.code,
            "state": room.state,
            "participants": list(room.participants.values())
        }
        for room in room_manager.rooms.values()
    ]

@app.get("/rooms/{code}")
def get_room(code: str):
    room = room_manager.get_room(code)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return {
        "code": room.code,
        "state": room.state,
        "participants": list(room.participants.values())
    }

@app.put("/rooms/{code}/state")
def update_room_state(code: str, state: str):
    room = room_manager.get_room(code)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    room.state = state
    return {
        "code": room.code,
        "state": room.state,
        "participants": list(room.participants.values())
    }

@app.delete("/rooms/{code}")
def delete_room(code: str):
    room = room_manager.get_room(code)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    room_manager.delete_room(code)
    return {"detail": f"Room {code} deleted"}


# -------- Participants Endpoints --------

@app.post("/rooms/{code}/participants")
def add_participant(code: str, participant: dict):
    room = room_manager.get_room(code)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    participant_id = max(room.participants.keys(), default=0) + 1
    room.add_participant(participant_id, participant.get("name", "Anonymous"))
    return {"id": participant_id, "name": participant.get("name", "Anonymous")}

@app.get("/rooms/{code}/participants")
def list_participants(code: str):
    room = room_manager.get_room(code)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return [{"id": pid, **info} for pid, info in room.participants.items()]

@app.delete("/participants/{participant_id}")
def remove_participant(participant_id: int):
    # find participant in all rooms and remove
    for room in room_manager.rooms.values():
        if participant_id in room.participants:
            room.remove_participant(participant_id)
            # optionally delete room if empty
            if room.is_empty():
                room_manager.delete_room(room.code)
            return {"detail": f"Participant {participant_id} removed"}
    raise HTTPException(status_code=404, detail="Participant not found")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
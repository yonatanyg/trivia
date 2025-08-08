from fastapi import FastAPI, Depends, HTTPException, WebSocket, WebSocketDisconnect
import logging
from sqlalchemy.orm import Session
import models, schemas, crud, database, seed
import asyncio
import os

from fastapi.middleware.cors import CORSMiddleware

from room_manager import room_manager
import game_manager 

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
async def add_participant(code: str, participant: dict):
    room = room_manager.get_room(code)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    participant_id = max(room.participants.keys(), default=0) + 1
    name = participant.get("name", "Anonymous")
    avatar = participant.get("avatar", "/avatars/avatar1.png")  # Default fallback

    room.add_participant(participant_id, name,avatar)

    # Broadcast update
    await room.broadcast({
        "event": "participant_joined",
        "id": participant_id,
        "name": name,
        "avatar": avatar,
    })

    return {"id": participant_id, "name": name, "avatar": avatar}

@app.get("/rooms/{code}/participants")
def list_participants(code: str):
    room = room_manager.get_room(code)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return [{"id": pid, **info} for pid, info in room.participants.items()]

@app.delete("/participants/{participant_id}")
def remove_participant(participant_id: int):
    # This endpoint is now optional, as cleanup is handled by WebSocket
    for room in room_manager.rooms.values():
        if participant_id in room.participants:
            room.remove_participant(participant_id)
            if room.is_empty():
                room_manager.delete_room(room.code)
            return {"detail": f"Participant {participant_id} removed"}
    raise HTTPException(status_code=404, detail="Participant not found")


### -- web sockets -- ###

@app.websocket("/ws/rooms/{code}")
async def websocket_endpoint(websocket: WebSocket, code: str, participant_id: int):
    room = room_manager.get_room(code)
    if not room:
        await websocket.close(code=1000, reason="Room not found")
        return

    await room.connect(participant_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            event = data.get("event")

            if event == "set_ready":
                ready = bool(data.get("ready", False))
                room.set_ready(participant_id, ready)

                await room.broadcast({
                    "event": "participant_ready",
                    "id": participant_id,
                    "ready": ready
                })

                if room_manager.is_room_ready_to_start(code):
                    await room.broadcast({
                        "event": "room_ready",
                        "room": code
                    })

            elif event == "start_game":
                if room_manager.is_room_ready_to_start(code):
                    if room.state == "waiting":
                        game = game_manager.GameManager(room, next(database.get_db()))

                        await room.broadcast({
                            "event": "start_game",
                            "message": "The game is starting!",
                            "time": game.timeout_seconds
                        })
                        room.start_game(game)

                        # Run the game in the background, don't await here
                        asyncio.create_task(game.run_game())

            elif event == "player_answered":
                room.game_manager.receive_answer(participant_id, data.get("answer"))

            else:
                await room.broadcast(data)

    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        room.disconnect(participant_id)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
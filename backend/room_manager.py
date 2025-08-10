import uuid
from typing import Dict, List
from fastapi import WebSocket
import asyncio
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GRACE_DELAY = int(os.getenv("GRACE_DELAY", "15"))

class Room:
    def __init__(self, code: str, questions_per_round: int = 5, time_per_round: int = 20, genre: str = None):
        self.code = code
        self.participants: Dict[int, dict] = {}
        self.state = "waiting"
        self.connections: Dict[int, WebSocket] = {}
        self.disconnect_tasks: Dict[int, asyncio.Task] = {}
        self.game_manager = None

        # New attributes
        self.questions_per_round = questions_per_round
        self.time_per_round = time_per_round
        self.genre = genre

        logger.info(f"Room created: code={self.code}, questions_per_round={self.questions_per_round}, time_per_round={self.time_per_round}, genre={self.genre}")

    def add_participant(self, participant_id: int, name: str, avatar: str):
        self.participants[participant_id] = {"name": name, "avatar": avatar, "ready": False}
        logger.info(f"Participant added to room {self.code}: id={participant_id}, name={name}, avatar={avatar}")

    def remove_participant(self, participant_id: int):
        if participant_id in self.participants:
            del self.participants[participant_id]
            logger.info(f"Participant removed from room {self.code}: id={participant_id}")
        else:
            logger.warning(f"Tried to remove non-existing participant {participant_id} from room {self.code}")

    def is_empty(self) -> bool:
        empty = len(self.participants) == 0
        logger.debug(f"Check if room {self.code} is empty: {empty}")
        return empty

    async def connect(self, participant_id: int, websocket: WebSocket):
        await websocket.accept()
        logger.info(f"Participant {participant_id} connected to room {self.code}")
        # Cancel any pending disconnect task if participant reconnects
        if participant_id in self.disconnect_tasks:
            self.disconnect_tasks[participant_id].cancel()
            del self.disconnect_tasks[participant_id]
            logger.info(f"Cancelled disconnect task for participant {participant_id} in room {self.code}")
        self.connections[participant_id] = websocket

    def disconnect(self, participant_id: int):
        if participant_id in self.connections:
            del self.connections[participant_id]
            logger.info(f"Participant {participant_id} disconnected from room {self.code}")

        if participant_id in self.disconnect_tasks:
            logger.info(f"Disconnect task already pending for participant {participant_id} in room {self.code}")
            return

        async def delayed_remove():
            try:
                logger.info(f"Starting grace delay for participant {participant_id} in room {self.code}")
                await asyncio.sleep(GRACE_DELAY)  # from env or default 15 sec
                # Only remove if still disconnected
                if participant_id not in self.connections:
                    logger.info(f"Grace delay expired. Removing participant {participant_id} from room {self.code}")
                    self.remove_participant(participant_id)
                    await self.broadcast({
                        "event": "participant_left",
                        "id": participant_id
                    })
                    if self.is_empty():
                        logger.info(f"Room {self.code} is empty after participant {participant_id} left. Deleting room.")
                        room_manager.delete_room(self.code)
            except asyncio.CancelledError:
                # Task was cancelled due to reconnection
                logger.info(f"Disconnect task cancelled for participant {participant_id} in room {self.code}")

        self.disconnect_tasks[participant_id] = asyncio.create_task(delayed_remove())

    async def broadcast(self, message: dict):
        logger.info(f"Broadcasting message in room {self.code}: {message}")
        for connection in self.connections.values():
            await connection.send_json(message)

    def set_ready(self, participant_id: int, ready: bool):
        if participant_id in self.participants:
            self.participants[participant_id]["ready"] = ready
            logger.info(f"Participant {participant_id} in room {self.code} set ready to {ready}")
        else:
            logger.warning(f"Trying to set ready state for non-existing participant {participant_id} in room {self.code}")

    def start_game(self, game_manager):
        self.game_manager = game_manager
        self.state = "in_game"
        logger.info(f"Game started in room {self.code}")

    def end_game(self):
        self.game_manager = None
        self.state = "waiting"
        logger.info(f"Game ended in room {self.code}")

class RoomManager:
    def __init__(self):
        self.rooms: Dict[str, Room] = {}
        # New mapping to quickly find a room by a participant's WebSocket
        self.websocket_to_participant: Dict[WebSocket, int] = {}
        self.participant_to_room: Dict[int, str] = {}
        logger.info("RoomManager initialized")

    def create_room(self, questions_per_round: int = 5, time_per_round: int = 20, genre: str = None) -> Room:
        while True:
            code = str(uuid.uuid4())[:6].upper()
            if code not in self.rooms:
                break
        room = Room(code, questions_per_round, time_per_round, genre)
        self.rooms[code] = room
        logger.info(f"Room created with code {code}, time per round: {time_per_round}")
        return room

    def get_room(self, code: str) -> Room | None:
        room = self.rooms.get(code)
        if room:
            logger.debug(f"Room fetched: {code}")
        else:
            logger.warning(f"Requested room not found: {code}")
        return room

    def delete_room(self, code: str):
        if code in self.rooms:
            room = self.rooms[code]
            logger.info(f"Deleting room {code}")
            # Cleanup connections and participant mappings before deleting
            for participant_id in list(room.connections.keys()):
                websocket = room.connections[participant_id]
                self.websocket_to_participant.pop(websocket, None)
                self.participant_to_room.pop(participant_id, None)
            del self.rooms[code]
        else:
            logger.warning(f"Tried to delete non-existing room {code}")

    def add_participant(self, code: str, participant_id: int, name: str, avatar: str) -> dict | None:
        room = self.get_room(code)
        if not room:
            logger.warning(f"Cannot add participant {participant_id} to non-existing room {code}")
            return None
        room.add_participant(participant_id, name, avatar)
        self.participant_to_room[participant_id] = code
        logger.info(f"Participant {participant_id} added to room {code}")
        return {"id": participant_id, "name": name, "avatar": avatar, "room": code}

    def remove_participant(self, code: str, participant_id: int) -> bool:
        room = self.get_room(code)
        if not room:
            logger.warning(f"Cannot remove participant {participant_id} from non-existing room {code}")
            return False
        room.remove_participant(participant_id)
        self.participant_to_room.pop(participant_id, None)
        logger.info(f"Participant {participant_id} removed from room {code}")
        return True

    def is_room_ready_to_start(self, code: str):
        room = self.get_room(code)
        if not room or len(room.participants) == 0:
            logger.debug(f"Room {code} not ready to start: no participants or room not found")
            return False
        ready = all(p["ready"] for p in room.participants.values())
        logger.info(f"Room {code} ready to start: {ready}")
        return ready

# Singleton room manager
room_manager = RoomManager()

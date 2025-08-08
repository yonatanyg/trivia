import uuid
from typing import Dict, List
from fastapi import WebSocket

import asyncio

import os

GRACE_DELAY = int(os.getenv("GRACE_DELAY", "15"))

class Room:
    def __init__(self, code: str):
        self.code = code
        self.participants: Dict[int, dict] = {}  # {participant_id: {"name": str,"ready": false}}
        self.state = "waiting"
        self.connections: Dict[int, WebSocket] = {}
        self.disconnect_tasks: Dict[int, asyncio.Task] = {}
        # Add this attribute to hold the game instance (None if no game running)
        self.game_manager = None

    def add_participant(self, participant_id: int, name: str, avatar: str):
        self.participants[participant_id] = {"name": name,"avatar": avatar, "ready": False}

    def remove_participant(self, participant_id: int):
        if participant_id in self.participants:
            del self.participants[participant_id]

    def is_empty(self) -> bool:
        return len(self.participants) == 0

    async def connect(self, participant_id: int, websocket: WebSocket):
        await websocket.accept()
        # Cancel any pending disconnect task if participant reconnects
        if participant_id in self.disconnect_tasks:
            self.disconnect_tasks[participant_id].cancel()
            del self.disconnect_tasks[participant_id]
        self.connections[participant_id] = websocket

    def disconnect(self, participant_id: int):
        if participant_id in self.connections:
            del self.connections[participant_id]

        if participant_id in self.disconnect_tasks:
            # Already a pending removal
            return

        async def delayed_remove():
            try:
                await asyncio.sleep(GRACE_DELAY)  # from env or default 15 sec
                # Only remove if still disconnected
                if participant_id not in self.connections:
                    self.remove_participant(participant_id)
                    await self.broadcast({
                        "event": "participant_left",
                        "id": participant_id
                    })
                    if self.is_empty():
                        room_manager.delete_room(self.code)
            except asyncio.CancelledError:
                # Task was cancelled due to reconnection
                pass

        self.disconnect_tasks[participant_id] = asyncio.create_task(delayed_remove())

    async def broadcast(self, message: dict):
        for connection in self.connections.values():
            await connection.send_json(message)

    def set_ready(self, participant_id: int, ready: bool):
        if participant_id in self.participants:
            self.participants[participant_id]["ready"] = ready

    def start_game(self, game_manager):
        self.game_manager = game_manager
        self.state = "in_game"

    def end_game(self):
        self.game_manager = None
        self.state = "waiting"

class RoomManager:
    def __init__(self):
        self.rooms: Dict[str, Room] = {}
        # New mapping to quickly find a room by a participant's WebSocket
        self.websocket_to_participant: Dict[WebSocket, int] = {}
        self.participant_to_room: Dict[int, str] = {}


    def create_room(self) -> Room:
        while True:
            code = str(uuid.uuid4())[:6].upper()
            if code not in self.rooms:
                break
        room = Room(code)
        self.rooms[code] = room
        return room

    def get_room(self, code: str) -> Room | None:
        return self.rooms.get(code)

    def delete_room(self, code: str):
        if code in self.rooms:
            # Cleanup connections and participant mappings before deleting
            room = self.rooms[code]
            for participant_id in list(room.connections.keys()):
                websocket = room.connections[participant_id]
                self.websocket_to_participant.pop(websocket, None)
                self.participant_to_room.pop(participant_id, None)
            del self.rooms[code]

    def add_participant(self, code: str, participant_id: int, name: str,avatar: str) -> dict | None:
        room = self.get_room(code)
        if not room:
            return None
        room.add_participant(participant_id, name,avatar)
        # Store a mapping from participant ID to room code
        self.participant_to_room[participant_id] = code
        return {"id": participant_id, "name": name,"avatar": avatar, "room": code}

    def remove_participant(self, code: str, participant_id: int) -> bool:
        room = self.get_room(code)
        if not room:
            return False
        room.remove_participant(participant_id)
        self.participant_to_room.pop(participant_id, None)
        return True
    
    def is_room_ready_to_start(self,code: str):
        room = self.get_room(code)
        if not room or len(room.participants) == 0:
            return False
        return all(p["ready"] for p in room.participants.values())

# Singleton room manager
room_manager = RoomManager()
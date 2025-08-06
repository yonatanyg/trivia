import uuid
from typing import Dict, List
from fastapi import WebSocket

class Room:
    def __init__(self, code: str):
        self.code = code
        self.participants: Dict[int, dict] = {}  # {participant_id: {"name": str}}
        self.state = "waiting"
        # Changed to map participant_id to WebSocket for easy lookup
        self.connections: Dict[int, WebSocket] = {}

    def add_participant(self, participant_id: int, name: str):
        self.participants[participant_id] = {"name": name}

    def remove_participant(self, participant_id: int):
        if participant_id in self.participants:
            del self.participants[participant_id]

    def is_empty(self) -> bool:
        return len(self.participants) == 0

    # Modified to accept participant_id
    async def connect(self, participant_id: int, websocket: WebSocket):
        await websocket.accept()
        self.connections[participant_id] = websocket

    # Modified to accept participant_id
    def disconnect(self, participant_id: int):
        if participant_id in self.connections:
            del self.connections[participant_id]

    async def broadcast(self, message: dict):
        # Iterate through connection values
        for connection in self.connections.values():
            await connection.send_json(message)

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

    def add_participant(self, code: str, participant_id: int, name: str) -> dict | None:
        room = self.get_room(code)
        if not room:
            return None
        room.add_participant(participant_id, name)
        # Store a mapping from participant ID to room code
        self.participant_to_room[participant_id] = code
        return {"id": participant_id, "name": name, "room": code}

    def remove_participant(self, code: str, participant_id: int) -> bool:
        room = self.get_room(code)
        if not room:
            return False
        room.remove_participant(participant_id)
        self.participant_to_room.pop(participant_id, None)
        return True

# Singleton room manager
room_manager = RoomManager()
# room_manager.py
import uuid
from typing import Dict

class Room:
    def __init__(self, code: str):
        self.code = code
        self.participants: Dict[int, dict] = {}  # {participant_id: {"name": str}}
        self.state = "waiting"

    def add_participant(self, participant_id: int, name: str):
        self.participants[participant_id] = {"name": name}

    def remove_participant(self, participant_id: int):
        if participant_id in self.participants:
            del self.participants[participant_id]

    def is_empty(self) -> bool:
        return len(self.participants) == 0


class RoomManager:
    def __init__(self):
        self.rooms: Dict[str, Room] = {}

    def create_room(self) -> Room:
        # Generate a unique 6-char uppercase code
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
            del self.rooms[code]

    def add_participant(self, code: str, participant_id: int, name: str) -> dict | None:
        """Adds a participant to a room by code. Returns participant info or None if room not found."""
        room = self.get_room(code)
        if not room:
            return None
        room.add_participant(participant_id, name)
        return {"id": participant_id, "name": name, "room": code}

    def remove_participant(self, code: str, participant_id: int) -> bool:
        """Removes a participant from a room. Returns True if removed, False if not found."""
        room = self.get_room(code)
        if not room:
            return False
        room.remove_participant(participant_id)
        return True


# Singleton room manager
room_manager = RoomManager()

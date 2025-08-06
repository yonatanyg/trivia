import { useNavigate } from "react-router-dom";
import { api } from "./api";
import "./App.css";

export default function App() {
  const navigate = useNavigate();

  // Create room via backend + add creator as participant
  const handleCreateRoom = async () => {
    const nickname = prompt("Enter your nickname:");
    if (!nickname) return;

    try {
      // 1. Create the room
      const resRoom = await api.post("/rooms/");
      const room = resRoom.data;

      // 2. Add the creator as participant
      const resParticipant = await api.post(
        `/rooms/${room.code}/participants/`,
        { name: nickname }
      );
      const participant = resParticipant.data;

      // 3. Navigate with participant state
      navigate(`/room/${room.code}`, { state: { participant } });
    } catch (err) {
      console.error("Failed to create room:", err);
    }
  };

  // Join room
  const handleJoinRoom = async () => {
    const code = prompt("Enter room code:")?.toUpperCase();
    if (!code) return;

    const nickname = prompt("Enter your nickname:");
    if (!nickname) return;

    try {
      // 1. Check if room exists
      await api.get(`/rooms/${code}`);

      // 2. Add participant
      const res = await api.post(`/rooms/${code}/participants/`, {
        name: nickname,
      });
      const participant = res.data;

      // 3. Navigate to room
      navigate(`/room/${code}`, { state: { participant } });
    } catch (err) {
      alert("Room not found or join failed");
      console.error(err);
    }
  };

  const handleAdmin = () => {
    navigate("/admin");
  };

  return (
    <div className="app-container">
      <h1 className="title">Trivia Game</h1>
      <button onClick={handleCreateRoom} className="btn create">
        Create Room
      </button>
      <button onClick={handleJoinRoom} className="btn join">
        Join Room
      </button>
      <button onClick={handleAdmin} className="btn admin">
        Admin
      </button>
    </div>
  );
}

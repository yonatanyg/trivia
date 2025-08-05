import { useNavigate } from "react-router-dom";
import { api } from "./api"; 
import "./App.css";

export default function App() {
  const navigate = useNavigate();

    // Create room via backend
  const handleCreateRoom = async () => {
    try {
      const res = await api.post("/rooms/"); // call FastAPI
      const room = res.data;
      navigate(`/room/${room.code}`); // use the real code from backend
    } catch (err) {
      console.error("Failed to create room:", err);
    }
  };
    // Join room via backend
  const handleJoinRoom = async () => {
    const code = prompt("Enter room code:");
    if (!code) return;

    try {
      const res = await api.get(`/rooms/${code.toUpperCase()}`);
      if (res.data) {
        navigate(`/room/${code.toUpperCase()}`);
      } else {
        alert("Room not found");
      }
    } catch (err) {
      alert("Room not found");
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

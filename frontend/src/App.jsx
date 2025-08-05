import { useNavigate } from "react-router-dom";
import "./App.css";

export default function App() {
  const navigate = useNavigate();

  const handleCreateRoom = () => {
    const fakeRoomId = Math.random().toString(36).substring(2, 8).toUpperCase();
    navigate(`/room/${fakeRoomId}`);
  };

  const handleJoinRoom = () => {
    const code = prompt("Enter room code:");
    if (code) {
      navigate(`/room/${code.toUpperCase()}`);
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

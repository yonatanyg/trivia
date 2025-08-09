// App.jsx
import { useNavigate } from "react-router-dom";
import { api } from "./api";
import "./App.css";
import RoomEnterBox from "./components/RoomEnterBox";

export default function App() {
  const navigate = useNavigate();

  const handleCreate = async ({ nickname, avatar }) => {
    console.log("WehWeh");
    try {
      const resRoom = await api.post("/rooms/");
      const room = resRoom.data;

      const resParticipant = await api.post(
        `/rooms/${room.code}/participants/`,
        { name: nickname, avatar }
      );

      const participant = resParticipant.data;
      navigate(`/room/${room.code}`, { state: { participant } });
    } catch (err) {
      console.error("Failed to create room:", err);
    }
  };

  const handleJoin = async ({ roomCode, nickname, avatar }) => {
    try {
      await api.get(`/rooms/${roomCode}`);
      const res = await api.post(`/rooms/${roomCode}/participants/`, {
        name: nickname,
        avatar,
      });
      const participant = res.data;
      navigate(`/room/${roomCode}`, { state: { participant } });
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
      <div className="room-boxes">
        <RoomEnterBox mode="create" onSubmit={handleCreate} />
        <RoomEnterBox mode="join" onSubmit={handleJoin} />
      </div>
      <button onClick={handleAdmin} className="btn admin">
        Admin
      </button>
    </div>
  );
}

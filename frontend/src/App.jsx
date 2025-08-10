import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "./api";
import "./App.css";
import RoomEnterBox from "./components/RoomEnterBox";

export default function App() {
  const navigate = useNavigate();

  // New states for create mode options in App.jsx
  const [genres, setGenres] = useState([]);
  const [selectedGenre, setSelectedGenre] = useState("");
  const [questionsPerRound, setQuestionsPerRound] = useState(5);
  const [timePerRound, setTimePerRound] = useState(20);

  // Fetch genres once on mount
  useEffect(() => {
    api.get("/genres")
      .then((res) => {
        setGenres(res.data);
        if (res.data.length > 0) setSelectedGenre(res.data[0]);
      })
      .catch(() => {
        setGenres([]);
        setSelectedGenre("");
      });
  }, []);

  const handleCreate = async ({ nickname, avatar }) => {
    try {
      const resRoom = await api.post("/rooms/", {
        questions_per_round: questionsPerRound,
        time_per_round: timePerRound,
        genre: selectedGenre,
      });
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
      <h1 className="title">Trivia Arena</h1>
      <div className="room-boxes">
        <RoomEnterBox
          mode="create"
          onSubmit={handleCreate}
          genres={genres}
          selectedGenre={selectedGenre}
          setSelectedGenre={setSelectedGenre}
          questionsPerRound={questionsPerRound}
          setQuestionsPerRound={setQuestionsPerRound}
          timePerRound={timePerRound}
          setTimePerRound={setTimePerRound}
        />
        <RoomEnterBox mode="join" onSubmit={handleJoin} />
      </div>
      <button onClick={handleAdmin} className="btn admin">
        Admin
      </button>
    </div>
  );
}

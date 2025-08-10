import { useState } from "react";
import "./RoomEnterBox.css";

const avatars = [
  "/avatars/avatar1.png",
  "/avatars/avatar2.png",
  "/avatars/avatar3.png",
  "/avatars/avatar4.png",
  "/avatars/avatar5.png",
  "/avatars/avatar6.png",
  "/avatars/avatar7.png",
  "/avatars/avatar8.png",
  "/avatars/avatar9.png",
  "/avatars/avatar10.png",
  "/avatars/avatar11.png",
  "/avatars/avatar12.png",
  "/avatars/avatar13.png",
];

export default function RoomEnterBox({
  mode,
  onSubmit,
  genres = [],
  selectedGenre,
  setSelectedGenre,
  questionsPerRound,
  setQuestionsPerRound,
  timePerRound,
  setTimePerRound,
}) {
  const [nickname, setNickname] = useState("");
  const [avatarIndex, setAvatarIndex] = useState(0);
  const [roomCode, setRoomCode] = useState("");

  const handleSubmit = () => {
    if (!nickname.trim()) return alert("Enter a nickname!");
    if (mode === "join" && !roomCode.trim()) return alert("Enter a room code!");
    if (mode === "create") {
      if (!questionsPerRound || questionsPerRound < 1)
        return alert("Enter a valid number of questions!");
      if (!timePerRound || timePerRound < 5)
        return alert("Time per round must be at least 5 seconds!");
      if (!selectedGenre) return alert("Select a genre!");
    }

    onSubmit({
      nickname: nickname.trim(),
      avatar: avatars[avatarIndex],
      roomCode: roomCode.trim().toUpperCase(),
      ...(mode === "create" && {
        questionsPerRound: Number(questionsPerRound),
        timePerRound: Number(timePerRound),
        genre: selectedGenre,
      }),
    });
  };

  const nextAvatar = () =>
    setAvatarIndex((prev) => (prev + 1) % avatars.length);
  const prevAvatar = () =>
    setAvatarIndex((prev) => (prev - 1 + avatars.length) % avatars.length);

  return (
    <div className="room-box">
      <h2>{mode === "create" ? "Create Room" : "Join Room"}</h2>

      <label>Nickname</label>
      <input
        type="text"
        value={nickname}
        onChange={(e) => setNickname(e.target.value)}
        placeholder="Your nickname"
      />

      <label>Avatar</label>
      <div className="avatar-picker">
        <button onClick={prevAvatar}>&lt;</button>
        <img src={avatars[avatarIndex]} alt="Avatar" className="avatar-img" />
        <button onClick={nextAvatar}>&gt;</button>
      </div>

      {mode === "create" && (
        <>
          <label>Number of Questions per Round</label>
          <input
            type="number"
            min="1"
            value={questionsPerRound}
            onChange={(e) => setQuestionsPerRound(Number(e.target.value))}
          />

          <label>Time per Round (seconds)</label>
          <input
            type="number"
            min="5"
            value={timePerRound}
            onChange={(e) => setTimePerRound(Number(e.target.value))}
          />

          <label>Genre</label>
          <select
            value={selectedGenre}
            onChange={(e) => setSelectedGenre(e.target.value)}
          >
            {genres.map((genre) => (
              <option key={genre} value={genre}>
                {genre}
              </option>
            ))}
          </select>
        </>
      )}

      {mode === "join" && (
        <>
          <label>Room Code</label>
          <input
            type="text"
            value={roomCode}
            onChange={(e) => setRoomCode(e.target.value)}
            placeholder="ABC123"
          />
        </>
      )}
      <br />
      <button onClick={handleSubmit} className="submit-btn">
        {mode === "create" ? "Create" : "Join"}
      </button>
    </div>
  );
}

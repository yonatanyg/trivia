// RoomEnterBox.jsx
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

export default function RoomEnterBox({ mode, onSubmit }) {
  const [nickname, setNickname] = useState("");
  const [avatarIndex, setAvatarIndex] = useState(0);
  const [roomCode, setRoomCode] = useState("");

  const handleSubmit = () => {
    if (!nickname.trim()) return alert("Enter a nickname!");
    if (mode === "join" && !roomCode.trim()) return alert("Enter a room code!");

    onSubmit({
      nickname: nickname.trim(),
      avatar: avatars[avatarIndex],
      roomCode: roomCode.trim().toUpperCase(),
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

      {mode === "join" && (
        <>
          <label>Room Code</label>
          <input
            type="text"
            value={roomCode}
            onChange={(e) => setRoomCode(e.target.value)}
            placeholder="ABCD"
          />
        </>
      )}

      <button onClick={handleSubmit} className="submit-btn">
        {mode === "create" ? "Create" : "Join"}
      </button>
    </div>
  );
}

import React from "react";
import { Link } from "react-router-dom";
import "./RoomStuff.css";

export default function RoomStuff({
  roomId,
  participant,
  participants,
  ready,
  toggleReady,
  startGame,
  roomStatus,
  roomGenre, // genre prop
}) {
  return (
    <div className="room-container">
      <h2 className="room-title">Room Lobby</h2>
      <p className="room-status">
        Status: <span>{roomStatus}</span>
      </p>

      <div className="room-info">
        <p>
          Room Code: <span className="room-code">{roomId}</span>
        </p>
        <p>
          Genre: <span className="room-genre">{roomGenre || "Any"}</span>
        </p>
        <p>
          You are: <span className="participant-name">{participant.name}</span>
        </p>
      </div>

      <div className="participants-section">
        <h3>Participants</h3>
        <ul className="participants-list">
          {participants.map((p) => (
            <li
              key={p.id}
              className={`participant-item ${
                p.id === participant.id ? "self" : ""
              }`}
            >
              <img
                src={p.avatar}
                alt={`${p.name}'s avatar`}
                className="avatar"
              />
              <span className="name">{p.name}</span>
              {p.ready && <span className="checkmark">✔</span>}
            </li>
          ))}
        </ul>
      </div>

      <div className="buttons">
        <button
          onClick={toggleReady}
          className={`btn ${ready ? "btn-green" : "btn-red"}`}
        >
          {ready ? "Ready" : "Not Ready"}
        </button>

        <button onClick={startGame} className="btn btn-blue">
          Start Game
        </button>

        <Link to="/" className="btn btn-gray">
          Back to Main
        </Link>
      </div>
    </div>
  );
}

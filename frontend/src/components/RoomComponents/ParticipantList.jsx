import React from "react";
import "./ParticipantList.css";

export default function ParticipantList({
  participants,
  scores,
  currentParticipantId,
}) {
  return (
    <div className="participant-list">
      <h3>Players</h3>
      <ul>
        {participants.map((p) => (
          <li
            key={p.id}
            className={`participant-item ${
              p.id === currentParticipantId ? "you" : ""
            }`}
          >
            <img
              src={p.avatar}
              alt={p.name}
              className="participant-avatar-small"
            />
            <div className="participant-info-text">
              <span className="participant-name">{p.name}</span>
              <span className="participant-score">
                {scores?.[p.id] ?? 0} pts
              </span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

import { useState, useEffect } from "react";
import { api } from "../api";
import "./ScoreboardBox.css";

export default function ScoreboardBox({ onClose }) {
  const [scores, setScores] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/scoreboard") // <-- adjust to your backend endpoint
      .then((res) => {
        const data = res.data; // This is an object: { nickname: score, ... }
        // Convert to array of [nickname, score] pairs
        const entries = Object.entries(data);
        setScores(entries);
        setLoading(false);  // <--- set loading to false here
      })
      .catch((err) => {
        console.error("Failed to load scoreboard:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="scoreboard-overlay">
      <div className="scoreboard-box">
        <button className="close-btn" onClick={onClose}>✖</button>
        <h2>Top Scores</h2>
        {loading ? (
          <p>Loading...</p>
        ) : (
          <ol>
          {scores.map(([nickname, score], index) => (
            <li key={index}>
              <span className="nickname">{nickname}</span>
              <span className="score">{score}</span>
            </li>
          ))}

          </ol>
        )}
      </div>
    </div>
  );
}

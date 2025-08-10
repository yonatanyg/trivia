import { useState, useEffect } from "react";
import { api } from "../api";
import "./ScoreboardBox.css";

export default function ScoreboardBox({ onClose }) {
  const [scores, setScores] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/scoreboard")
      .then((res) => {
        const data = res.data; // { nickname: score, ... }
        // Convert to array of [nickname, score] pairs
        const entries = Object.entries(data);
        // Sort descending by score
        entries.sort((a, b) => b[1] - a[1]);
        setScores(entries);
        setLoading(false);
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

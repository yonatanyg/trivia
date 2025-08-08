//import "./GameOverPanel.css";

export default function GameOverPanel({ scores, participants, onExit }) {
  if (!scores || Object.keys(scores).length === 0) return null;

  // Get the highest score
  const maxScore = Math.max(...Object.values(scores));

  // Find the winner(s)
  const winners = participants.filter((p) => scores[p.id] === maxScore);

  return (
    <div className="game-over-panel">
      <h2>🏆 Game Over!</h2>

      <h3>
        Winner{winners.length > 1 ? "s" : ""}:{" "}
        {winners.map((w) => w.name).join(", ")}
      </h3>

      <div className="score-list">
        <h4>Final Scores</h4>
        <ul>
          {participants.map((p) => (
            <li key={p.id}>
              {p.name}: {scores[p.id] ?? 0}
            </li>
          ))}
        </ul>
      </div>

      <button onClick={onExit}>Go Back to Room</button>
    </div>
  );
}

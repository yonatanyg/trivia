import { useState } from "react";

function App() {
  const [movie, setMovie] = useState("");
  const [director, setDirector] = useState("");
  const [pairs, setPairs] = useState([]);

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!movie || !director) return;

    setPairs([...pairs, { movie, director }]);
    setMovie("");
    setDirector("");
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial, sans-serif" }}>
      <h1>🎬 Movie / Director Pairs</h1>

      <form onSubmit={handleSubmit} style={{ marginBottom: "1rem" }}>
        <input
          type="text"
          placeholder="Movie name"
          value={movie}
          onChange={(e) => setMovie(e.target.value)}
          style={{ marginRight: "0.5rem", padding: "0.5rem" }}
        />
        <input
          type="text"
          placeholder="Director name"
          value={director}
          onChange={(e) => setDirector(e.target.value)}
          style={{ marginRight: "0.5rem", padding: "0.5rem" }}
        />
        <button type="submit" style={{ padding: "0.5rem 1rem" }}>
          Add
        </button>
      </form>

      <ul>
        {pairs.map((pair, index) => (
          <li key={index}>
            <strong>{pair.movie}</strong> — {pair.director}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;

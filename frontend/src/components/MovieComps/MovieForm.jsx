import { useState } from "react";

function MovieForm({ onAddPair }) {
  const [movie, setMovie] = useState("");
  const [director, setDirector] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!movie || !director) return;

    onAddPair(movie, director);
    setMovie("");
    setDirector("");
  };

  return (
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
  );
}

export default MovieForm;

import { useState, useEffect } from "react";
import axios from "axios";

import MovieForm from "./components/MovieComps/MovieForm";
import MovieList from "./components/MovieComps/MovieList";

import AddQuestions from "./components/AdminComponents/AddQuestions";
import QuestionsList from "./components/AdminComponents/QuestionsList";

import "./App.css";

function App() {
  const [movies, setMovies] = useState([]);

  // Fetch movies on mount
  useEffect(() => {
    axios
      .get("http://localhost:8000/movies/")
      .then((res) => setMovies(res.data))
      .catch((err) => console.error("Error fetching movies:", err));
  }, []);

  // Add new movie
  const addMovie = async (movie, director) => {
    try {
      const res = await axios.post("http://localhost:8000/movies/", {
        name: movie,
        director: director,
      });
      setMovies([...movies, res.data]);
    } catch (err) {
      console.error("Error adding movie:", err);
    }
  };

  return (
    <div className="app-layout">
      <main className="main-content">
        <h1 className="section-title">❓ Trivia Admin</h1>
        <div className="form-wrapper">
          <AddQuestions />
        </div>
        <div className="question-list-wrapper">
          <QuestionsList />
        </div>
      </main>

      <section className="movies-section">
        <h1 className="section-title">🎬 Movies</h1>
        <div className="form-wrapper">
          <MovieForm onAddPair={addMovie} />
        </div>
        <MovieList
          pairs={movies.map((m) => ({ movie: m.name, director: m.director }))}
        />
      </section>
    </div>
  );
}

export default App;

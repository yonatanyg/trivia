import MovieItem from "./MovieItem";

function MovieList({ pairs }) {
  if (pairs.length === 0) {
    return <p>No movies added yet.</p>;
  }

  return (
    <ul>
      {pairs.map((pair, index) => (
        <MovieItem key={index} movie={pair.movie} director={pair.director} />
      ))}
    </ul>
  );
}

export default MovieList;

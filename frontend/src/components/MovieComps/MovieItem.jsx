function MovieItem({ movie, director }) {
  return (
    <li>
      <strong>{movie}</strong> — {director}
    </li>
  );
}

export default MovieItem;

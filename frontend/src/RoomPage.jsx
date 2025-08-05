import { useParams, Link } from "react-router-dom";

export default function RoomPage() {
  const { roomId } = useParams();

  return (
    <div className="flex flex-col items-center justify-center h-screen gap-6">
      <h2 className="text-2xl font-semibold">Room</h2>
      <p className="text-lg">
        Room Code: <span className="font-mono">{roomId}</span>
      </p>
      <Link
        to="/"
        className="px-4 py-2 bg-gray-500 text-white rounded-lg shadow hover:bg-gray-600"
      >
        Back to Main
      </Link>
    </div>
  );
}

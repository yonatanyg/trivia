import { useEffect } from "react";
import { useParams, Link, useLocation, useNavigate } from "react-router-dom";
import { api } from "./api";

export default function RoomPage() {
  const { roomId } = useParams();
  const location = useLocation();
  const navigate = useNavigate();

  // participant info passed from App.jsx
  const participant = location.state?.participant;
  useEffect(() => {
    if (!participant) {
      navigate("/");
      return;
    }

    const handleBeforeUnload = async () => {
      if (!participant?.id) return;
      alert(participant?.id);
      try {
        await api.delete(`/participants/${participant.id}`);
      } catch (err) {
        console.error("Failed to remove participant:", err);
      }
    };

    window.addEventListener("beforeunload", handleBeforeUnload);

    return () => {
      window.removeEventListener("beforeunload", handleBeforeUnload);
    };
  }, [participant, navigate]);

  if (!participant) return null;

  return (
    <div className="flex flex-col items-center justify-center h-screen gap-6">
      <h2 className="text-2xl font-semibold">Room</h2>
      <p className="text-lg">
        Room Code: <span className="font-mono">{roomId}</span>
      </p>
      <p className="text-lg">
        Nickname: <span className="font-semibold">{participant.name}</span>
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

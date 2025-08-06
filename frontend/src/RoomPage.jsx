import { useEffect, useState } from "react";
import { useParams, Link, useLocation, useNavigate } from "react-router-dom";
import { api } from "./api";

export default function RoomPage() {
  const { roomId } = useParams();
  const location = useLocation();
  const navigate = useNavigate();

  const [participants, setParticipants] = useState([]);
  const participant = location.state?.participant;

  useEffect(() => {
    if (!participant) {
      navigate("/");
      return;
    }

    // Connect to WebSocket using the new deployed URL
    const ws = new WebSocket(
      `wss://trivia-0dqx.onrender.com/ws/rooms/${roomId}?participant_id=${participant.id}`
    );

    ws.onopen = () => {
      console.log("WebSocket connection established");
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      console.log("Received message:", message);

      if (message.event === "participant_joined") {
        setParticipants((prevParticipants) => [
          ...prevParticipants,
          { id: message.id, name: message.name },
        ]);
      } else if (message.event === "participant_left") {
        setParticipants((prevParticipants) =>
          prevParticipants.filter((p) => p.id !== message.id)
        );
      }
    };

    ws.onclose = () => {
      console.log("WebSocket connection closed");
    };

    ws.onerror = (err) => {
      console.error("WebSocket error:", err);
    };

    const fetchParticipants = async () => {
      try {
        const response = await api.get(`/rooms/${roomId}/participants`);
        setParticipants(response.data);
      } catch (err) {
        console.error("Failed to fetch participants:", err);
      }
    };
    fetchParticipants();

    return () => {
      ws.close();
    };
  }, [participant, navigate, roomId]);

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

      <div className="mt-4">
        <h3 className="text-xl font-medium">Participants:</h3>
        <ul className="list-disc list-inside">
          {participants.map((p) => (
            <li key={p.id}>{p.name}</li>
          ))}
        </ul>
      </div>

      <Link
        to="/"
        className="px-4 py-2 bg-gray-500 text-white rounded-lg shadow hover:bg-gray-600"
      >
        Back to Main
      </Link>
    </div>
  );
}

import { createContext, useContext, useState, useRef, useEffect } from "react";
import { useNavigate, useParams, useLocation } from "react-router-dom";
import { api } from "./api";

const RoomContext = createContext();

export const useRoom = () => useContext(RoomContext);

const WS_URL = import.meta.env.VITE_WEBSOCKET_URL;

export function RoomProvider({ children }) {
  const { roomId } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const participant = location.state?.participant;

  const socketRef = useRef(null);
  const timerRef = useRef(null);

  const [participants, setParticipants] = useState([]);
  const [ready, setReady] = useState(false);
  const [inGame, setInGame] = useState(false);
  const [selectedAnswerId, setSelectedAnswerId] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [questionTimer, setQuestionTimer] = useState(null);
  const [correctAnswerId, setCorrectAnswerId] = useState(null);
  const [scores, setScores] = useState({}); // <-- new scores state
  const [gameOver, setGameOver] = useState(false);
  const [roomStatus, setRoomStatus] = useState("waiting");

  useEffect(() => {
    if (!participant) {
      navigate("/");
      return;
    }

    const ws = new WebSocket(
      `${WS_URL}/ws/rooms/${roomId}?participant_id=${participant.id}`
    );

    socketRef.current = ws;

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      console.log("Received message:", message);

      switch (message.event) {
        case "participant_joined":
          setParticipants((prev) => [
            ...prev,
            {
              id: message.id,
              name: message.name,
              avatar: message.avatar,
              ready: false,
            },
          ]);
          break;

        case "participant_left":
          setParticipants((prev) => prev.filter((p) => p.id !== message.id));
          break;

        case "participant_ready":
          setParticipants((prev) =>
            prev.map((p) =>
              p.id === message.id ? { ...p, ready: message.ready } : p
            )
          );
          break;

        case "start_game":
          setInGame(true);
          setRoomStatus("in_game");
          /*setReady(false);
          socketRef.current?.send(
            JSON.stringify({ event: "set_ready", ready: false })
          );*/
          break;

        case "new_question":
          setCurrentQuestion(message.question);
          setQuestionTimer(message.time);
          setSelectedAnswerId(null);
          setCorrectAnswerId(null);
          if (timerRef.current) clearInterval(timerRef.current);
          timerRef.current = setInterval(() => {
            setQuestionTimer((prev) => {
              if (prev <= 1) {
                clearInterval(timerRef.current);
                return 0;
              }
              return prev - 1;
            });
          }, 1000);
          break;

        case "round_results":
          setCorrectAnswerId(message.correctAnswerId);
          setScores(message.scores || {}); // <-- update scores here
          console.log("Correct Answer IDs:", message.correctAnswerId);
          console.log("Scores:", message.scores);
          break;
        case "game_over":
          //present winner
          setGameOver(true);
          setRoomStatus("waiting");
          break;
      }
    };

    ws.onclose = () => console.log("WebSocket connection closed");
    ws.onerror = (err) => console.error("WebSocket error:", err);

    const fetchParticipants = async () => {
      try {
        const res = await api.get(`/rooms/${roomId}/participants`);
        setParticipants(res.data);
      } catch (err) {
        console.error("Failed to fetch participants:", err);
      }
    };
    fetchParticipants();

    const fetchRoomStatus = async () => {
      try {
        const res = await api.get(`/rooms/${roomId}/`);
        setRoomStatus(res.data.state);
      } catch (err) {
        console.error("Failed to fetch room status:", err);
      }
    };
    fetchRoomStatus();

    return () => {
      ws.close();
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [participant, roomId, navigate]);

  const toggleReady = () => {
    const newReady = !ready;
    setReady(newReady);
    socketRef.current?.send(
      JSON.stringify({ event: "set_ready", ready: newReady })
    );
  };

  const startGame = () => {
    socketRef.current?.send(JSON.stringify({ event: "start_game" }));
  };

  const sendAnswer = (answerId) => {
    socketRef.current?.send(
      JSON.stringify({ event: "player_answered", answer: answerId })
    );
  };

  const exitGame = () => {
    setInGame(false);
    setGameOver(false);
    setCurrentQuestion(null);
    setQuestionTimer(null);
    setSelectedAnswerId(null);
    setCorrectAnswerId(null);
    setScores({});
    if (timerRef.current) clearInterval(timerRef.current);
    setReady(false);
    toggleReady();
  };

  return (
    <RoomContext.Provider
      value={{
        roomId,
        participant,
        participants,
        ready,
        toggleReady,
        inGame,
        startGame,
        currentQuestion,
        questionTimer,
        selectedAnswerId,
        setSelectedAnswerId,
        sendAnswer,
        exitGame,
        correctAnswerId,
        scores, // <-- provide scores here
        gameOver,
        roomStatus,
      }}
    >
      {children}
    </RoomContext.Provider>
  );
}

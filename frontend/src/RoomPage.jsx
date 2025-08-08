// RoomPage.jsx
import { RoomProvider, useRoom } from "./RoomContext.jsx";
import RoomStuff from "./components/RoomComponents/RoomStuff";
import GamePanel from "./components/RoomComponents/GamePanel";
import GameOverPanel from "./components/RoomComponents/GameOverPanel";

import "./RoomPage.css";

export default function RoomPageWrapper() {
  return (
    <RoomProvider>
      <RoomPage />
    </RoomProvider>
  );
}

function RoomPage() {
  const {
    participant,
    inGame,
    participants,
    ready,
    toggleReady,
    startGame,
    currentQuestion,
    questionTimer,
    selectedAnswerId,
    setSelectedAnswerId,
    sendAnswer,
    exitGame,
    correctAnswerId,
    scores,
    gameOver,
    roomStatus,
    roomId,
  } = useRoom();

  if (!participant) return null;

  return (
    <div className="container">
      {!inGame ? (
        <RoomStuff
          roomId={roomId}
          participant={participant}
          participants={participants}
          ready={ready}
          toggleReady={toggleReady}
          startGame={startGame}
          roomStatus={roomStatus}
        />
      ) : gameOver ? (
        <GameOverPanel
          scores={scores}
          participants={participants}
          onExit={exitGame}
        />
      ) : (
        <GamePanel
          onExit={exitGame}
          question={currentQuestion}
          timer={questionTimer}
          selectedAnswerId={selectedAnswerId}
          setSelectedAnswerId={setSelectedAnswerId}
          sendAnswer={sendAnswer}
          correctAnswerId={correctAnswerId}
          scores={scores}
          participant={participant}
          participants={participants}
        />
      )}
    </div>
  );
}

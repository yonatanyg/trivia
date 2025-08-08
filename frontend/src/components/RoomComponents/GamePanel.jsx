import React from "react";
import ParticipantList from "./ParticipantList";
import "./GamePanel.css";

export default function GamePanel({
  onExit,
  question,
  timer,
  sendAnswer,
  selectedAnswerId,
  setSelectedAnswerId,
  correctAnswerId,
  scores,
  participant,
  participants,
}) {
  const handleAnswerClick = (answerId) => {
    if (selectedAnswerId !== null) return;
    setSelectedAnswerId(answerId);
    sendAnswer(answerId);
  };

  const currentScore = scores?.[participant?.id] ?? 0;

  return (
    <div className="game-panel">
      <button className="exit-button" onClick={onExit}>
        Exit
      </button>

      <ParticipantList
        participants={participants}
        scores={scores}
        currentParticipantId={participant?.id}
      />

      {question ? (
        <div className="question-block">
          <h2>{question.question}</h2>
          <div className="answers">
            {question.answers.map((answer) => {
              const isCorrect =
                correctAnswerId && correctAnswerId.includes(answer.id);

              return (
                <button
                  key={answer.id}
                  className={`answer-button ${isCorrect ? "correct" : ""}`}
                  disabled={selectedAnswerId !== null}
                  onClick={() => handleAnswerClick(answer.id)}
                >
                  {answer.answer}
                </button>
              );
            })}
          </div>
          <div className="timer">⏳ {timer}s</div>
        </div>
      ) : (
        <p>Waiting for question...</p>
      )}
    </div>
  );
}

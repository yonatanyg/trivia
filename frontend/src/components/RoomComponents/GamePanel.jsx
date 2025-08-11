import React, { useMemo } from "react";
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

  const decodeHTML = (htmlString) => {
    const txt = document.createElement("textarea");
    txt.innerHTML = htmlString;
    return txt.value;
  };

  const currentScore = scores?.[participant?.id] ?? 0;

  // Shuffle answers with useMemo so it only happens once per question change
  const shuffledAnswers = useMemo(() => {
    if (!question?.answers) return [];
    // Create a shallow copy
    const answersCopy = [...question.answers];
    // Fisher-Yates shuffle
    for (let i = answersCopy.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [answersCopy[i], answersCopy[j]] = [answersCopy[j], answersCopy[i]];
    }
    return answersCopy;
  }, [question]);

  return (
    <div className="game-panel">
      {/* <button className="exit-button" onClick={onExit}>
        Exit
      </button> */}

      <ParticipantList
        participants={participants}
        scores={scores}
        currentParticipantId={participant?.id}
      />

      {question ? (
        <div className="question-block">
          <h2>{decodeHTML(question.question)}</h2>
          <div className="answers">
            {shuffledAnswers.map((answer) => {
            return (
              <button
                key={answer.id}
                className={`answer-button ${
                  correctAnswerId &&
                  selectedAnswerId === answer.id &&
                  !correctAnswerId.includes(answer.id)
                    ? "incorrect"
                    : correctAnswerId && correctAnswerId.includes(answer.id)
                    ? "correct"
                    : ""
                }`}
                disabled={selectedAnswerId !== null}
                onClick={() => handleAnswerClick(answer.id)}
              >
                {decodeHTML(answer.answer)}
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

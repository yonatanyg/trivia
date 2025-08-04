// AddQuestions.jsx
import { useState } from "react";
import axios from "axios";

import "./AddQuestions.css";

export default function AddQuestions() {
  const [question, setQuestion] = useState("");
  const [answers, setAnswers] = useState([{ answer: "", is_correct: false }]);
  const [correctIndex, setCorrectIndex] = useState(null);

  // Add new answer input
  const addAnswer = () => {
    setAnswers([...answers, { answer: "", is_correct: false }]);
  };

  // Remove last answer input
  const removeAnswer = () => {
    if (answers.length > 1) {
      setAnswers(answers.slice(0, -1));
    }
  };

  // Handle text change for each answer
  const handleAnswerChange = (index, value) => {
    const newAnswers = [...answers];
    newAnswers[index].answer = value;
    setAnswers(newAnswers);
  };

  // Handle radio selection
  const handleCorrectChange = (index) => {
    setCorrectIndex(index);
    const newAnswers = answers.map((ans, i) => ({
      ...ans,
      is_correct: i === index,
    }));
    setAnswers(newAnswers);
  };

  // Submit form
  const handleSubmit = async (e) => {
    e.preventDefault();

    const payload = {
      question,
      answers,
    };

    try {
      await axios.post("http://localhost:8000/questions/", payload);
      alert("Question added successfully!");
      setQuestion("");
      setAnswers([{ answer: "", is_correct: false }]);
      setCorrectIndex(null);
    } catch (error) {
      console.error(error);
      alert("Failed to add question.");
    }
  };

  return (
    <div className="add-question-container">
      <h2>Add New Question</h2>

      <form onSubmit={handleSubmit}>
        {/* Question input */}
        <div>
          <label>Question</label>
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            required
          />
        </div>

        {/* Answer inputs */}
        <div>
          <label>Answers</label>
          <div className="answers-list">
            {answers.map((ans, index) => (
              <div key={index} className="answer-item">
                <input
                  type="radio"
                  name="correctAnswer"
                  checked={correctIndex === index}
                  onChange={() => handleCorrectChange(index)}
                />
                <input
                  type="text"
                  value={ans.answer}
                  onChange={(e) => handleAnswerChange(index, e.target.value)}
                  required
                />
              </div>
            ))}
          </div>

          <div className="button-group">
            <button type="button" onClick={addAnswer}>
              +
            </button>
            <button type="button" onClick={removeAnswer}>
              –
            </button>
          </div>
        </div>

        {/* Submit */}
        <button type="submit" className="submit-button">
          Submit
        </button>
      </form>
    </div>
  );
}

// QuestionsList.jsx
import { useEffect, useState } from "react";
import axios from "axios";

export default function QuestionsList() {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchQuestions();
  }, []);

  const fetchQuestions = async () => {
    try {
      const res = await axios.get("http://localhost:8000/questions/");
      setQuestions(res.data);
    } catch (error) {
      console.error("Error fetching questions:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <p className="text-center">Loading questions...</p>;

  return (
    <div className="p-4 max-w-2xl mx-auto bg-white shadow rounded">
      <h2 className="text-xl font-bold mb-4">Questions List</h2>
      {questions.length === 0 ? (
        <p>No questions found. Add some!</p>
      ) : (
        <ul className="space-y-4">
          {questions.map((q) => (
            <li key={q.id} className="border p-3 rounded">
              <p className="font-semibold mb-2">
                Q{q.id}: {q.question}
              </p>
              <ul className="list-disc list-inside space-y-1">
                {q.answers.map((a) => (
                  <li
                    key={a.id}
                    className={
                      a.is_correct
                        ? "text-green-600 font-medium"
                        : "text-gray-700"
                    }
                  >
                    {a.answer} {a.is_correct && "✔"}
                  </li>
                ))}
              </ul>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

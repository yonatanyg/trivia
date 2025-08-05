import { Link } from "react-router-dom";
import AddQuestions from "./components/AdminComponents/AddQuestions";
import QuestionsList from "./components/AdminComponents/QuestionsList";

export default function AdminPage() {
  return (
    <div>
      <h2>Admin Panel</h2>

      {/* Add Question Form */}
      <div>
        <AddQuestions />
      </div>

      {/* Questions List */}
      <div>
        <QuestionsList />
      </div>

      <Link to="/">Back to Main</Link>
    </div>
  );
}

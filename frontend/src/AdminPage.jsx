import React, { useState, useEffect, useRef } from "react";
import { Link, useNavigate } from "react-router-dom";
import AddQuestions from "./components/AdminComponents/AddQuestions";
import QuestionsList from "./components/AdminComponents/QuestionsList";
import { api } from "./api"; // Import your axios instance

export default function AdminPage() {
  const [authorized, setAuthorized] = useState(false);
  const navigate = useNavigate();
  const promptRun = useRef(false);

  useEffect(() => {
    if (!authorized && !promptRun.current) {
      promptRun.current = true;
      const password = prompt("Enter admin password:");
      if (password === "ADMIN") {
        setAuthorized(true);
      } else {
        navigate("/", { replace: true });
      }
    }
  }, [authorized, navigate]);

  const handleSeedDB = async () => {
    try {
      const response = await api.post("/seed_db");
      if (response.status === 200) {
        alert("Database seeded successfully!");
      } else {
        alert("Failed to seed database.");
      }
    } catch (error) {
      alert("Error seeding database: " + error.message);
    }
  };

  const handleClearScoreboard = async () => {
    if (!window.confirm("Are you sure you want to clear the scoreboard? This action cannot be undone.")) {
      return;
    }
    try {
      const response = await api.delete("/scoreboard");
      if (response.status === 200 || response.status === 204) {
        alert("Scoreboard cleared successfully!");
      } else {
        alert("Failed to clear scoreboard.");
      }
    } catch (error) {
      alert("Error clearing scoreboard: " + error.message);
    }
  };

  if (!authorized) {
    return null;
  }

  return (
    <div>
      <h2>Admin Panel</h2>
      <button onClick={handleSeedDB} style={{ marginBottom: "1rem", marginRight: "1rem" }}>
        Seed DB
      </button>
      <button onClick={handleClearScoreboard} style={{ marginBottom: "1rem" }}>
        Clear Scoreboard
      </button>
      <AddQuestions />
      <QuestionsList />
      <Link to="/">Back to Main</Link>
    </div>
  );
}

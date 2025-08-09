import json
from database import get_db
from models import Question, Answer

def populate_db(json_path="questions.json"):
    db = next(get_db())

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        questions_data = data["questions"]  # <-- Access the list here

        for q_data in questions_data:
            question = Question(question=q_data["question"])
            for a_data in q_data["answers"]:
                answer = Answer(answer=a_data["answer"], is_correct=a_data["is_correct"])
                question.answers.append(answer)
            db.add(question)

        db.commit()
        print(f"✅ Inserted {len(questions_data)} questions into the database!")
    except Exception as e:
        db.rollback()
        print("❌ Error inserting data:", e)
    finally:
        db.close()

if __name__ == "__main__":
    populate_db()

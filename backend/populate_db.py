import json
from models import Question, Answer

def populate_db(db, json_path="questions.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    questions_data = data["questions"]

    for q_data in questions_data:
        exists = db.query(Question).filter(Question.question == q_data["question"]).first()
        if exists:
            continue

        question = Question(question=q_data["question"])
        for a_data in q_data["answers"]:
            answer = Answer(answer=a_data["answer"], is_correct=a_data["is_correct"])
            question.answers.append(answer)

        db.add(question)

    db.commit()

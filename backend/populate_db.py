import json
import logging
from models import Question, Answer

logger = logging.getLogger(__name__)

def populate_db(db, json_path="questions.json"):
    logger.info(f"Starting to populate the database from {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    questions_data = data["questions"]
    inserted_count = 0
    skipped_count = 0

    for q_data in questions_data:
        exists = db.query(Question).filter(Question.question == q_data["question"]).first()
        if exists:
            logger.warning(f"Skipping existing question: {q_data['question']}")
            skipped_count += 1
            continue

        question = Question(question=q_data["question"])
        for a_data in q_data["answers"]:
            answer = Answer(answer=a_data["answer"], is_correct=a_data["is_correct"])
            question.answers.append(answer)

        db.add(question)
        inserted_count += 1
        logger.info(f"Added question: {q_data['question']}")

    db.commit()
    logger.info(f"Database populated! Inserted: {inserted_count}, Skipped: {skipped_count}")

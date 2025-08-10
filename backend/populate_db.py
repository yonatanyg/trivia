import requests
import html
import logging
import time
from models import Question, Answer

logger = logging.getLogger(__name__)

CATEGORY_IDS = [9, 11, 12, 14, 15, 18, 19, 22, 26]

def get_category_name(category_id):
    url = "https://opentdb.com/api_category.php"
    response = requests.get(url)
    response.raise_for_status()
    categories = response.json()["trivia_categories"]
    for cat in categories:
        if cat["id"] == category_id:
            return cat["name"]
    return None

def fetch_questions_by_category(category_id, amount=50, retries=3):
    url = "https://opentdb.com/api.php"
    params = {
        "amount": amount,
        "category": category_id,
        "type": "multiple"
    }
    for attempt in range(retries):
        response = requests.get(url, params=params)
        if response.status_code == 429:
            wait = 2 ** attempt  # exponential backoff: 1, 2, 4 seconds
            logger.warning(f"Rate limited by API. Waiting {wait}s before retry #{attempt + 1}...")
            time.sleep(wait)
            continue
        response.raise_for_status()
        data = response.json()
        if data["response_code"] != 0:
            logger.warning(f"No results or error for category {category_id}")
            return []
        return data["results"]
    logger.error(f"Failed to fetch questions for category {category_id} after {retries} retries due to rate limiting")
    return []

def transform_questions(raw_questions, genre):
    questions = []
    for i, item in enumerate(raw_questions, start=1):
        question_text = html.unescape(item["question"])
        correct_answer = html.unescape(item["correct_answer"])
        incorrect_answers = [html.unescape(ans) for ans in item["incorrect_answers"]]

        answers = []
        answers.append({
            "answer": correct_answer,
            "is_correct": True
        })
        for ans in incorrect_answers:
            answers.append({
                "answer": ans,
                "is_correct": False
            })
        
        questions.append({
            "question": question_text,
            "genre": genre,
            "answers": answers
        })
    return questions

def populate_db(db, categories=CATEGORY_IDS, amount_per_category=50):
    logger.info(f"Starting DB population for categories {categories}")
    total_inserted = 0
    total_skipped = 0

    for cat_id in categories:
        genre = get_category_name(cat_id)
        logger.info(f"Fetching {amount_per_category} questions from category '{genre}' (ID {cat_id})")
        raw_questions = fetch_questions_by_category(cat_id, amount=amount_per_category)
        questions = transform_questions(raw_questions, genre)

        for q_data in questions:
            exists = db.query(Question).filter(Question.question == q_data["question"]).first()
            if exists:
                logger.warning(f"Skipping existing question: {q_data['question']}")
                total_skipped += 1
                continue

            question = Question(
                question=q_data["question"],
                genre=q_data.get("genre")
            )
            for a_data in q_data["answers"]:
                answer = Answer(answer=a_data["answer"], is_correct=a_data["is_correct"])
                question.answers.append(answer)

            db.add(question)
            total_inserted += 1
            logger.info(f"Added question: {q_data['question']}")

        # Be kind to the API - wait 2 seconds before next category
        time.sleep(2)

    db.commit()
    logger.info(f"DB population finished. Inserted: {total_inserted}, Skipped: {total_skipped}")

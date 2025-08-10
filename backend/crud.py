from sqlalchemy.orm import Session,joinedload
import models, schemas
import random, string

from sqlalchemy.exc import ProgrammingError
import logging
from sqlalchemy.sql.expression import func
from sqlalchemy import desc

# ------------------ Questions & Answers ------------------ #
def get_questions(db: Session):
    return db.query(models.Question).all()

def create_question(db: Session, question: schemas.QuestionCreate):
    db_question = models.Question(question=question.question)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    # Add answers
    for ans in question.answers:
        db_answer = models.Answer(
            answer=ans.answer,
            is_correct=ans.is_correct,
            question_id=db_question.id
        )
        db.add(db_answer)
    db.commit()

    db.refresh(db_question)
    return db_question

def get_random_question_with_answers(db: Session, genre: str = None):
    query = (
        db.query(models.Question)
        .options(joinedload(models.Question.answers))  # eager load answers
    )

    if genre:  # filter by genre if provided
        query = query.filter(models.Question.genre == genre)

    question = query.order_by(func.random()).first()
    return question

def get_genres(db: Session):
    try:
        genres = db.query(models.Question.genre).distinct().all()
        return [g[0] for g in genres if g[0] is not None]
    except ProgrammingError as e:
        logging.error(f"Database error fetching genres: {e}")
        # Return empty or fallback value so the app continues running
        return []

def get_amount_of_questions(db: Session, genre: str = None):
    query = db.query(func.count(models.Question.id))
    if genre:
        query = query.filter(models.Question.genre == genre)
    return query.scalar()  # returns the count as an integer

def update_scoreboard(db: Session, participants_score: dict[str, float]):
    """
    participants_score: dict mapping nickname (str) -> score (float)
    Updates the scoreboard table with given scores.
    Keeps only top 50 scores (removes lower ones).
    """
    # Upsert scores
    for nickname, score in participants_score.items():
        entry = db.query(models.Scoreboard).filter(models.Scoreboard.nickname == nickname).one_or_none()
        if entry:
            # Update score only if new score is higher
            if score > entry.score:
                entry.score = score
        else:
            entry = models.Scoreboard(nickname=nickname, score=score)
            db.add(entry)
    db.commit()

    # Delete entries beyond top 50
    top_50 = db.query(models.Scoreboard.nickname).order_by(desc(models.Scoreboard.score)).limit(50).all()
    top_50_nicknames = set(n[0] for n in top_50)

    # Delete entries NOT in top 50
    db.query(models.Scoreboard).filter(~models.Scoreboard.nickname.in_(top_50_nicknames)).delete(synchronize_session=False)
    db.commit()

def get_top_scoreboard(db: Session, amount: int = 10) -> dict[str, float]:
    """
    Returns a dict mapping nickname -> score for the top `amount` scores.
    """
    top_scores = db.query(models.Scoreboard).order_by(desc(models.Scoreboard.score)).limit(amount).all()
    return {entry.nickname: entry.score for entry in top_scores}

def delete_scores(db:Session):
    """ remove all rows of Scoreboard"""
   
    db.query(models.Scoreboard).delete()
    db.commit()

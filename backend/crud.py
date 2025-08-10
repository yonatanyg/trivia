from sqlalchemy.orm import Session,joinedload
import models, schemas
import random, string

from sqlalchemy.sql.expression import func

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
    genres = db.query(models.Question.genre).distinct().all()
    # genres is a list of single-element tuples, e.g. [('History',), ('Science',), ...]
    return [g[0] for g in genres if g[0] is not None]

def get_amount_of_questions(db: Session, genre: str = None):
    query = db.query(func.count(models.Question.id))
    if genre:
        query = query.filter(models.Question.genre == genre)
    return query.scalar()  # returns the count as an integer
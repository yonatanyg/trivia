from sqlalchemy.orm import Session
import models, schemas

def get_movies(db: Session):
    return db.query(models.Movie).all()

def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(name=movie.name, director=movie.director)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

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
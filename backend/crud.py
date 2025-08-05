from sqlalchemy.orm import Session
import models, schemas
import random, string


# ------------------ Movies ------------------ #
def get_movies(db: Session):
    return db.query(models.Movie).all()

def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(name=movie.name, director=movie.director)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


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


# ------------------ Rooms & Participants ------------------ #
def generate_room_code(length: int = 6):
    """Generate a random uppercase alphanumeric room code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def create_room(db: Session, room: schemas.RoomCreate = None):
    code = room.code if room and room.code else generate_room_code()

    # Ensure unique code
    while db.query(models.Room).filter(models.Room.code == code).first():
        code = generate_room_code()

    db_room = models.Room(code=code, state="waiting")
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def get_room_by_code(db: Session, code: str):
    return db.query(models.Room).filter(models.Room.code == code).first()

def get_rooms(db: Session):
    return db.query(models.Room).all()

def update_room_state(db: Session, code: str, state: str):
    db_room = get_room_by_code(db, code)
    if not db_room:
        return None
    db_room.state = state
    db.commit()
    db.refresh(db_room)
    return db_room

def delete_room(db: Session, code: str):
    db_room = get_room_by_code(db, code)
    if db_room:
        db.delete(db_room)
        db.commit()
    return db_room


# ------------------ Participants ------------------ #
def add_participant(db: Session, code: str, participant: schemas.ParticipantCreate):
    db_room = get_room_by_code(db, code)
    if not db_room:
        return None
    db_participant = models.Participant(name=participant.name, room_id=db_room.id)
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant

def get_participants(db: Session, code: str):
    db_room = get_room_by_code(db, code)
    if not db_room:
        return []
    return db_room.participants

def remove_participant(db: Session, participant_id: int):
    db_participant = db.query(models.Participant).filter(models.Participant.id == participant_id).first()
    if db_participant:
        db.delete(db_participant)
        db.commit()
    return db_participant

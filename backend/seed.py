from sqlalchemy.orm import Session
import models

def seed_data(db: Session):
    """Insert initial movies and questions with answers if tables are empty"""

    # Seed movies if empty
    if db.query(models.Movie).count() == 0:
        movies = [
            models.Movie(name="Inception", director="Christopher Nolan"),
            models.Movie(name="Pulp Fiction", director="Quentin Tarantino"),
            models.Movie(name="The Matrix", director="The Wachowskis"),
        ]
        db.add_all(movies)

    # Seed questions if empty
    if db.query(models.Question).count() == 0:
        q1 = models.Question(question="What is the capital of France?")
        q1.answers = [
            models.Answer(answer="Paris", is_correct=True),
            models.Answer(answer="London", is_correct=False),
            models.Answer(answer="Rome", is_correct=False),
        ]

        q2 = models.Question(question="Who wrote '1984'?")
        q2.answers = [
            models.Answer(answer="George Orwell", is_correct=True),
            models.Answer(answer="Aldous Huxley", is_correct=False),
            models.Answer(answer="Ray Bradbury", is_correct=False),
        ]

        q3 = models.Question(question="Which planet is known as the Red Planet?")
        q3.answers = [
            models.Answer(answer="Mars", is_correct=True),
            models.Answer(answer="Jupiter", is_correct=False),
            models.Answer(answer="Venus", is_correct=False),
        ]

        db.add_all([q1, q2, q3])

    db.commit()

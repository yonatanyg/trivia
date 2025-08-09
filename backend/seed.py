from sqlalchemy.orm import Session
from populate_db import populate_db
import models

def seed_data(db: Session):
    """Seed questions from JSON if questions table is empty"""

    if db.query(models.Question).count() == 0:
        try:
            populate_db(db)
        except Exception as e:
            print("Failed to seed questions:", e)

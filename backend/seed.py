from sqlalchemy.orm import Session
from populate_db import populate_db
import models
import logging

logger = logging.getLogger(__name__)

def seed_data(db: Session):
    """Clear all questions and seed from JSON, run once on startup"""
    try:
        # Delete all answers first (if cascading not set)
        deleted_answers = db.query(models.Answer).delete()
        logger.info(f"Deleted {deleted_answers} answers")

        # Delete all questions
        deleted_questions = db.query(models.Question).delete()
        logger.info(f"Deleted {deleted_questions} questions")

        db.commit()

        # Now populate fresh
        populate_db(db)
        logger.info("Seeded questions successfully")
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to seed questions: {e}")

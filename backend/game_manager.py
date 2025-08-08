import random
import asyncio
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from models import Question, Answer
import crud
import schemas
import utilities

logger = logging.getLogger(__name__)

def timestamp():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + " UTC"

class GameManager:
    def __init__(self, room, db: Session, num_rounds=5, timeout_seconds=20):
        self.room = room
        self.db = db
        self.num_rounds = num_rounds
        self.timeout_seconds = timeout_seconds
        self.questions_asked = set()

        self.current_answers = {}  # participant_id -> answer id
        self.scores = {}           # participant_id -> score

        self._answers_received_event = asyncio.Event()

    def receive_answer(self, participant_id, answer):
        logger.info(f"[{timestamp()}] Received answer from {participant_id}: {answer}")
        self.current_answers[participant_id] = answer
        if all(pid in self.current_answers for pid in self.room.participants.keys()):
            self._answers_received_event.set()

    def get_next_question(self):
        while True:
            question = crud.get_random_question_with_answers(self.db)
            if question is None:
                logger.warning(f"[{timestamp()}] No questions available in database.")
                return None
            if question.id not in self.questions_asked:
                self.questions_asked.add(question.id)
                logger.info(f"[{timestamp()}] Selected question ID {question.id}: {question.question}")
                return question
            logger.info(f"[{timestamp()}] Question ID {question.id} already asked. Picking another.")

    async def wait_for_answers_or_timeout(self):
        try:
            await asyncio.wait_for(self._answers_received_event.wait(), timeout=self.timeout_seconds)
        except asyncio.TimeoutError:
            logger.info(f"[{timestamp()}] Timeout reached while waiting for answers.")

    def compute_scores(self):
        winners = []
        if not hasattr(self, "current_question") or not self.current_question:
            logger.warning(f"[{timestamp()}] No current question to compute scores.")
            return winners

        correct_answer_ids = {ans.id for ans in self.current_question.answers if ans.is_correct}
        logger.info(f"[{timestamp()}] Correct answer IDs for question {self.current_question.id}: {correct_answer_ids}")

        for pid, answer_id in self.current_answers.items():
            if answer_id in correct_answer_ids:
                self.scores[pid] = self.scores.get(pid, 0) + 1
                logger.info(f"[{timestamp()}] Participant {pid} answered correctly. New score: {self.scores[pid]}")
            else:
                logger.info(f"[{timestamp()}] Participant {pid} answered incorrectly.")

        if self.current_answers:
            max_score = max(self.scores.get(pid, 0) for pid in self.current_answers)
            winners = [pid for pid in self.current_answers if self.scores.get(pid, 0) == max_score]
            logger.info(f"[{timestamp()}] Round winners: {winners}")
        else:
            logger.info(f"[{timestamp()}] No answers received this round.")

        return winners

    def get_overall_winner(self):
        if not self.scores:
            logger.info(f"[{timestamp()}] No scores to determine overall winner.")
            return None
        max_score = max(self.scores.values())
        winners = [pid for pid, score in self.scores.items() if score == max_score]
        logger.info(f"[{timestamp()}] Overall winners: {winners}")
        return winners if len(winners) > 1 else winners[0]

    async def run_game(self):
        logger.info(f"[{timestamp()}] Game started.")
        for round_num in range(self.num_rounds):
            logger.info(f"[{timestamp()}] --- Round {round_num + 1} ---")
            question = self.get_next_question()
            if question is None:
                logger.warning(f"[{timestamp()}] No more questions to ask. Ending game early.")
                break

            self.current_question = question
            self.current_answers = {}
            self._answers_received_event.clear()

            answers_data = [schemas.Answer.from_orm(ans) for ans in question.answers]
            question_data = schemas.Question(
                id=question.id,
                question=question.question,
                answers=answers_data
            ).dict()

            logger.info(f"[{timestamp()}] Broadcasting question {question.id} to room {self.room.code}")
            await self.room.broadcast({
                "event": "new_question",
                "question": question_data,
                "time": self.timeout_seconds
            })

            await self.wait_for_answers_or_timeout()

            winners = self.compute_scores()
            await self.room.broadcast({
                "event": "round_results",
                "winners": winners,
                "scores": self.scores,
                "correctAnswerId": utilities.correctAnswersId(self.current_question)
            })

            logger.info(f"[{timestamp()}] Scores after round {round_num + 1}: {self.scores}")
            await asyncio.sleep(3)

        overall_winner = self.get_overall_winner()
        logger.info(f"[{timestamp()}] Game over. Final winner(s): {overall_winner}")
        self.room.end_game()
        await self.room.broadcast({"event": "game_over", "winner": overall_winner})

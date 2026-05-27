from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db
from app.models.entities import Question, Submission
from app.schemas.question import QuestionRead
from app.schemas.submission import RecommendationRead, SubmissionCreate
from app.services.recommendations import create_submission_with_recommendation

router = APIRouter(prefix="/public", tags=["public"])


@router.get("/questions", response_model=list[QuestionRead])
def get_public_questions(db: Session = Depends(get_db)) -> list[Question]:
    query = (
        select(Question)
        .options(selectinload(Question.answer_options))
        .where(Question.is_active.is_(True))
        .order_by(Question.position, Question.id)
    )
    questions = db.execute(query).scalars().all()
    for question in questions:
        question.answer_options = [
            option for option in question.answer_options if option.is_active
        ]
    return list(questions)


@router.post("/submissions", response_model=RecommendationRead)
def submit_answers(payload: SubmissionCreate, db: Session = Depends(get_db)) -> RecommendationRead:
    submission = create_submission_with_recommendation(db, payload)
    submission = db.execute(
        select(Submission)
        .options(selectinload(Submission.recommended_package))
        .where(Submission.id == submission.id)
    ).scalar_one()
    return RecommendationRead(
        submission_id=submission.id,
        recommended_package=submission.recommended_package,
        total_score=submission.total_score,
    )

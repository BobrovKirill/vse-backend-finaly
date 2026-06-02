from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db
from app.models.entities import Choice, ChoicePackageRecommendation, Package, PackageService, Question
from app.schemas.choice import ChoiceCreate, RecommendationRead
from app.schemas.question import PublicQuestionRead
from app.services.public_questions_cache import cache_public_questions, get_cached_public_questions
from app.services.recommendations import create_choice_with_recommendation

router = APIRouter(prefix="/public", tags=["public"])


@router.get("/questions", response_model=list[PublicQuestionRead])
def get_public_questions(db: Session = Depends(get_db)) -> list[PublicQuestionRead]:
    cached_questions = get_cached_public_questions()
    if cached_questions is not None:
        return cached_questions

    query = (
        select(Question)
        .options(selectinload(Question.answers))
        .where(Question.is_active.is_(True))
        .order_by(Question.position, Question.id)
    )
    questions = db.execute(query).scalars().all()
    for question in questions:
        question.answers = [answer for answer in question.answers if answer.is_active]
    public_questions = [
        PublicQuestionRead.model_validate(question)
        for question in questions
    ]
    cache_public_questions(public_questions)
    return public_questions


@router.post("/choices", response_model=RecommendationRead)
def submit_answers(payload: ChoiceCreate, db: Session = Depends(get_db)) -> RecommendationRead:
    choice = create_choice_with_recommendation(db, payload)
    choice = db.execute(
        select(Choice)
        .options(
            selectinload(Choice.indicator_scores),
            selectinload(Choice.recommended_packages)
            .selectinload(ChoicePackageRecommendation.package)
            .selectinload(Package.services)
            .selectinload(PackageService.service),
        )
        .where(Choice.id == choice.id)
    ).scalar_one()
    return RecommendationRead(
        choice_id=choice.id,
        recommended_packages=choice.recommended_packages,
        total_score=choice.total_score,
        indicator_scores=choice.indicator_scores,
    )

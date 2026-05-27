from collections import defaultdict

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities import AnswerOption, Package, Question, QuestionType, Submission, SubmissionAnswer
from app.schemas.submission import SubmissionCreate


def create_submission_with_recommendation(db: Session, payload: SubmissionCreate) -> Submission:
    questions = _load_active_questions(db)
    options_by_id = _load_active_options(db)
    selected_rows: list[tuple[Question, AnswerOption]] = []

    for answer in payload.answers:
        question = questions.get(answer.question_id)
        if question is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Question {answer.question_id} is inactive or does not exist",
            )
        if question.question_type == QuestionType.single.value and len(answer.answer_option_ids) != 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Question {answer.question_id} accepts exactly one answer",
            )

        for option_id in answer.answer_option_ids:
            option = options_by_id.get(option_id)
            if option is None or option.question_id != question.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Answer option {option_id} does not belong to question {question.id}",
                )
            selected_rows.append((question, option))

    package_scores: dict[int, int] = defaultdict(int)
    total_score = 0
    for _, option in selected_rows:
        total_score += option.score
        if option.package_id is not None:
            package_scores[option.package_id] += option.score

    recommended_package_id = _select_best_package_id(db, package_scores)
    submission = Submission(
        contact_name=payload.contact_name,
        contact_phone=payload.contact_phone,
        recommended_package_id=recommended_package_id,
        total_score=total_score,
    )
    submission.answers = [
        SubmissionAnswer(question_id=question.id, answer_option_id=option.id)
        for question, option in selected_rows
    ]
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


def _load_active_questions(db: Session) -> dict[int, Question]:
    rows = db.execute(select(Question).where(Question.is_active.is_(True))).scalars().all()
    return {row.id: row for row in rows}


def _load_active_options(db: Session) -> dict[int, AnswerOption]:
    rows = db.execute(select(AnswerOption).where(AnswerOption.is_active.is_(True))).scalars().all()
    return {row.id: row for row in rows}


def _select_best_package_id(db: Session, package_scores: dict[int, int]) -> int | None:
    if not package_scores:
        return None

    active_packages = db.execute(
        select(Package).where(Package.id.in_(package_scores.keys()), Package.is_active.is_(True))
    ).scalars().all()
    active_ids = {package.id for package in active_packages}
    eligible_scores = {
        package_id: score
        for package_id, score in package_scores.items()
        if package_id in active_ids
    }
    if not eligible_scores:
        return None

    return max(eligible_scores.items(), key=lambda item: (item[1], -item[0]))[0]

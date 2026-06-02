from collections import defaultdict

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.entities import (
    Answer,
    Choice,
    ChoiceAnswer,
    ChoiceIndicatorScore,
    ChoicePackageRecommendation,
    Package,
    PackageRule,
    Question,
    QuestionType,
)
from app.schemas.choice import ChoiceCreate


def create_choice_with_recommendation(db: Session, payload: ChoiceCreate) -> Choice:
    questions = _load_active_questions(db)
    answers_by_id = _load_active_answers(db)
    selected_rows: list[tuple[Question, Answer]] = []

    for selected_answer in payload.answers:
        question = questions.get(selected_answer.question_id)
        if question is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Question {selected_answer.question_id} is inactive or does not exist",
            )
        if question.question_type == QuestionType.single.value and len(selected_answer.answer_ids) != 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Question {selected_answer.question_id} accepts exactly one answer",
            )

        for answer_id in selected_answer.answer_ids:
            answer = answers_by_id.get(answer_id)
            if answer is None or answer.question_id != question.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Answer {answer_id} does not belong to question {question.id}",
                )
            selected_rows.append((question, answer))

    indicator_scores: dict[int, int] = defaultdict(int)
    for _, answer in selected_rows:
        for effect in answer.effects:
            indicator_scores[effect.indicator_id] += effect.score

    choice = Choice(
        contact_name=payload.contact_name,
        contact_phone=payload.contact_phone,
    )
    choice.answers = [
        ChoiceAnswer(answer_id=answer.id)
        for _, answer in selected_rows
    ]
    choice.indicator_scores = [
        ChoiceIndicatorScore(indicator_id=indicator_id, score=score)
        for indicator_id, score in indicator_scores.items()
    ]
    choice.recommended_packages = [
        ChoicePackageRecommendation(
            package_id=package_id,
            rank=rank,
            matched_weight=matched_weight,
        )
        for rank, (package_id, matched_weight) in enumerate(
            _select_matching_packages(db, indicator_scores),
            start=1,
        )
    ]
    db.add(choice)
    db.commit()
    db.refresh(choice)
    return choice


def _load_active_questions(db: Session) -> dict[int, Question]:
    rows = db.execute(select(Question).where(Question.is_active.is_(True))).scalars().all()
    return {row.id: row for row in rows}


def _load_active_answers(db: Session) -> dict[int, Answer]:
    rows = db.execute(
        select(Answer)
        .options(selectinload(Answer.effects))
        .where(Answer.is_active.is_(True))
    ).scalars().all()
    return {row.id: row for row in rows}


def _select_matching_packages(db: Session, indicator_scores: dict[int, int]) -> list[tuple[int, int]]:
    if not indicator_scores:
        return []

    packages = db.execute(
        select(Package).where(Package.is_active.is_(True)).order_by(Package.id)
    ).scalars().all()
    rules = db.execute(select(PackageRule)).scalars().all()
    rules_by_package: dict[int, list[PackageRule]] = defaultdict(list)
    for rule in rules:
        rules_by_package[rule.package_id].append(rule)

    matched_packages: list[tuple[int, int]] = []
    for package in packages:
        package_rules = rules_by_package.get(package.id, [])
        if not package_rules:
            continue

        matched_weight = 0
        for rule in package_rules:
            score = indicator_scores.get(rule.indicator_id, 0)
            if score < rule.min_score:
                break
            if rule.max_score is not None and score > rule.max_score:
                break
            matched_weight += rule.weight
        else:
            matched_packages.append((package.id, matched_weight))

    return sorted(matched_packages, key=lambda item: (-item[1], item[0]))

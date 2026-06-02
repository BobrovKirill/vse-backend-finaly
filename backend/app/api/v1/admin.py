from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.api.v1.deps import get_current_admin
from app.core.database import get_db
from app.models.entities import (
    Answer,
    AnswerEffect,
    Choice,
    ChoicePackageRecommendation,
    HealthIndicator,
    Package,
    PackageRule,
    PackageService,
    Question,
    Service,
)
from app.schemas.choice import ChoiceRead
from app.schemas.indicator import (
    HealthIndicatorCreate,
    HealthIndicatorRead,
    HealthIndicatorUpdate,
    PackageRuleCreate,
    PackageRuleRead,
    PackageRuleUpdate,
)
from app.schemas.package import (
    PackageCreate,
    PackageRead,
    PackageServiceCreate,
    PackageServiceRead,
    PackageUpdate,
    ServiceCreate,
    ServiceRead,
    ServiceUpdate,
)
from app.schemas.question import (
    AnswerCreate,
    AnswerEffectCreate,
    AnswerEffectRead,
    AnswerEffectUpdate,
    AnswerRead,
    AnswerUpdate,
    QuestionCreate,
    QuestionRead,
    QuestionUpdate,
)
from app.services.public_questions_cache import invalidate_public_questions_cache

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_admin)],
)


@router.post("/packages", response_model=PackageRead, status_code=status.HTTP_201_CREATED)
def create_package(payload: PackageCreate, db: Session = Depends(get_db)) -> Package:
    package = Package(**_normalize_package_data(payload.model_dump()))
    db.add(package)
    db.commit()
    db.refresh(package)
    return package


@router.get("/packages", response_model=list[PackageRead])
def list_packages(db: Session = Depends(get_db)) -> list[Package]:
    return list(db.execute(_packages_query().order_by(Package.id)).scalars().all())


@router.get("/packages/{package_id}", response_model=PackageRead)
def get_package(package_id: int, db: Session = Depends(get_db)) -> Package:
    return _get_package_or_404(db, package_id)


@router.patch("/packages/{package_id}", response_model=PackageRead)
def update_package(package_id: int, payload: PackageUpdate, db: Session = Depends(get_db)) -> Package:
    package = _get_package_or_404(db, package_id)
    for field, value in _normalize_package_data(payload.model_dump(exclude_unset=True)).items():
        setattr(package, field, value)
    db.commit()
    db.refresh(package)
    return package


@router.delete("/packages/{package_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_package(package_id: int, db: Session = Depends(get_db)) -> Response:
    package = _get_package_or_404(db, package_id)
    db.delete(package)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/services", response_model=ServiceRead, status_code=status.HTTP_201_CREATED)
def create_service(payload: ServiceCreate, db: Session = Depends(get_db)) -> Service:
    service = Service(**payload.model_dump())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


@router.get("/services", response_model=list[ServiceRead])
def list_services(db: Session = Depends(get_db)) -> list[Service]:
    return list(db.execute(select(Service).order_by(Service.id)).scalars().all())


@router.patch("/services/{service_id}", response_model=ServiceRead)
def update_service(service_id: int, payload: ServiceUpdate, db: Session = Depends(get_db)) -> Service:
    service = _get_service_or_404(db, service_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(service, field, value)
    db.commit()
    db.refresh(service)
    return service


@router.delete("/services/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(service_id: int, db: Session = Depends(get_db)) -> Response:
    service = _get_service_or_404(db, service_id)
    db.delete(service)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/packages/{package_id}/services",
    response_model=PackageServiceRead,
    status_code=status.HTTP_201_CREATED,
)
def add_package_service(
    package_id: int,
    payload: PackageServiceCreate,
    db: Session = Depends(get_db),
) -> PackageService:
    _get_package_or_404(db, package_id)
    _get_service_or_404(db, payload.service_id)
    package_service = PackageService(package_id=package_id, **payload.model_dump())
    db.add(package_service)
    db.commit()
    db.refresh(package_service)
    return _get_package_service_or_404(db, package_service.id)


@router.delete("/packages-services/{package_service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_package_service(package_service_id: int, db: Session = Depends(get_db)) -> Response:
    package_service = _get_package_service_or_404(db, package_service_id)
    db.delete(package_service)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/indicators", response_model=HealthIndicatorRead, status_code=status.HTTP_201_CREATED)
def create_indicator(payload: HealthIndicatorCreate, db: Session = Depends(get_db)) -> HealthIndicator:
    indicator = HealthIndicator(**payload.model_dump())
    db.add(indicator)
    db.commit()
    db.refresh(indicator)
    return indicator


@router.get("/indicators", response_model=list[HealthIndicatorRead])
def list_indicators(db: Session = Depends(get_db)) -> list[HealthIndicator]:
    return list(db.execute(select(HealthIndicator).order_by(HealthIndicator.id)).scalars().all())


@router.patch("/indicators/{indicator_id}", response_model=HealthIndicatorRead)
def update_indicator(
    indicator_id: int,
    payload: HealthIndicatorUpdate,
    db: Session = Depends(get_db),
) -> HealthIndicator:
    indicator = _get_indicator_or_404(db, indicator_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(indicator, field, value)
    db.commit()
    db.refresh(indicator)
    return indicator


@router.post("/packages/{package_id}/rules", response_model=PackageRuleRead, status_code=status.HTTP_201_CREATED)
def create_package_rule(
    package_id: int,
    payload: PackageRuleCreate,
    db: Session = Depends(get_db),
) -> PackageRule:
    _get_package_or_404(db, package_id)
    _get_indicator_or_404(db, payload.indicator_id)
    rule = PackageRule(package_id=package_id, **payload.model_dump())
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return rule


@router.get("/packages/{package_id}/rules", response_model=list[PackageRuleRead])
def list_package_rules(package_id: int, db: Session = Depends(get_db)) -> list[PackageRule]:
    _get_package_or_404(db, package_id)
    query = select(PackageRule).where(PackageRule.package_id == package_id).order_by(PackageRule.id)
    return list(db.execute(query).scalars().all())


@router.patch("/package-rules/{rule_id}", response_model=PackageRuleRead)
def update_package_rule(
    rule_id: int,
    payload: PackageRuleUpdate,
    db: Session = Depends(get_db),
) -> PackageRule:
    rule = _get_package_rule_or_404(db, rule_id)
    data = payload.model_dump(exclude_unset=True)
    if data.get("indicator_id") is not None:
        _get_indicator_or_404(db, data["indicator_id"])
    for field, value in data.items():
        setattr(rule, field, value)
    db.commit()
    db.refresh(rule)
    return rule


@router.delete("/package-rules/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_package_rule(rule_id: int, db: Session = Depends(get_db)) -> Response:
    rule = _get_package_rule_or_404(db, rule_id)
    db.delete(rule)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/questions", response_model=QuestionRead, status_code=status.HTTP_201_CREATED)
def create_question(payload: QuestionCreate, db: Session = Depends(get_db)) -> Question:
    indicator_ids = [
        effect.indicator_id
        for answer in payload.answers
        for effect in answer.effects
    ]
    _validate_indicator_links(db, indicator_ids)
    question = Question(**payload.model_dump(exclude={"answers"}))
    question.answers = [
        Answer(
            **answer.model_dump(exclude={"effects"}),
            effects=[AnswerEffect(**effect.model_dump()) for effect in answer.effects],
        )
        for answer in payload.answers
    ]
    db.add(question)
    db.commit()
    db.refresh(question)
    invalidate_public_questions_cache()
    return _get_question_or_404(db, question.id)


@router.get("/questions", response_model=list[QuestionRead])
def list_questions(db: Session = Depends(get_db)) -> list[Question]:
    query = _questions_query().order_by(Question.position, Question.id)
    return list(db.execute(query).scalars().all())


@router.get("/questions/{question_id}", response_model=QuestionRead)
def get_question(question_id: int, db: Session = Depends(get_db)) -> Question:
    return _get_question_or_404(db, question_id)


@router.patch("/questions/{question_id}", response_model=QuestionRead)
def update_question(question_id: int, payload: QuestionUpdate, db: Session = Depends(get_db)) -> Question:
    question = _get_question_or_404(db, question_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(question, field, value)
    db.commit()
    invalidate_public_questions_cache()
    return _get_question_or_404(db, question.id)


@router.delete("/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(question_id: int, db: Session = Depends(get_db)) -> Response:
    question = _get_question_or_404(db, question_id)
    db.delete(question)
    db.commit()
    invalidate_public_questions_cache()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/questions/{question_id}/answers", response_model=AnswerRead, status_code=status.HTTP_201_CREATED)
def create_answer(question_id: int, payload: AnswerCreate, db: Session = Depends(get_db)) -> Answer:
    _get_question_or_404(db, question_id)
    _validate_indicator_links(db, [effect.indicator_id for effect in payload.effects])
    answer = Answer(
        question_id=question_id,
        **payload.model_dump(exclude={"effects"}),
        effects=[AnswerEffect(**effect.model_dump()) for effect in payload.effects],
    )
    db.add(answer)
    db.commit()
    db.refresh(answer)
    invalidate_public_questions_cache()
    return _get_answer_or_404(db, answer.id)


@router.patch("/answers/{answer_id}", response_model=AnswerRead)
def update_answer(answer_id: int, payload: AnswerUpdate, db: Session = Depends(get_db)) -> Answer:
    answer = _get_answer_or_404(db, answer_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(answer, field, value)
    db.commit()
    invalidate_public_questions_cache()
    return _get_answer_or_404(db, answer.id)


@router.delete("/answers/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(answer_id: int, db: Session = Depends(get_db)) -> Response:
    answer = _get_answer_or_404(db, answer_id)
    db.delete(answer)
    db.commit()
    invalidate_public_questions_cache()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/answers/{answer_id}/effects", response_model=AnswerEffectRead, status_code=status.HTTP_201_CREATED)
def create_answer_effect(
    answer_id: int,
    payload: AnswerEffectCreate,
    db: Session = Depends(get_db),
) -> AnswerEffect:
    _get_answer_or_404(db, answer_id)
    _get_indicator_or_404(db, payload.indicator_id)
    effect = AnswerEffect(answer_id=answer_id, **payload.model_dump())
    db.add(effect)
    db.commit()
    db.refresh(effect)
    return effect


@router.delete("/answer-effects/{effect_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer_effect(effect_id: int, db: Session = Depends(get_db)) -> Response:
    effect = _get_answer_effect_or_404(db, effect_id)
    db.delete(effect)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/answer-effects/{effect_id}", response_model=AnswerEffectRead)
def update_answer_effect(
    effect_id: int,
    payload: AnswerEffectUpdate,
    db: Session = Depends(get_db),
) -> AnswerEffect:
    effect = _get_answer_effect_or_404(db, effect_id)
    data = payload.model_dump(exclude_unset=True)
    if data.get("indicator_id") is not None:
        _get_indicator_or_404(db, data["indicator_id"])
    for field, value in data.items():
        setattr(effect, field, value)
    db.commit()
    db.refresh(effect)
    return effect


@router.get("/choices", response_model=list[ChoiceRead])
def list_choices(db: Session = Depends(get_db)) -> list[Choice]:
    query = (
        select(Choice)
        .options(
            selectinload(Choice.answers),
            selectinload(Choice.indicator_scores),
            selectinload(Choice.recommended_packages)
            .selectinload(ChoicePackageRecommendation.package)
            .selectinload(Package.services)
            .selectinload(PackageService.service),
        )
        .order_by(Choice.id.desc())
    )
    return list(db.execute(query).scalars().all())


def _questions_query():
    return select(Question).options(
        selectinload(Question.answers).selectinload(Answer.effects)
    )


def _get_package_or_404(db: Session, package_id: int) -> Package:
    package = db.execute(_packages_query().where(Package.id == package_id)).scalar_one_or_none()
    if package is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Package not found")
    return package


def _packages_query():
    return select(Package).options(
        selectinload(Package.services).selectinload(PackageService.service)
    )


def _get_service_or_404(db: Session, service_id: int) -> Service:
    service = db.get(Service, service_id)
    if service is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return service


def _get_package_service_or_404(db: Session, package_service_id: int) -> PackageService:
    query = (
        select(PackageService)
        .options(selectinload(PackageService.service))
        .where(PackageService.id == package_service_id)
    )
    package_service = db.execute(query).scalar_one_or_none()
    if package_service is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Package service not found")
    return package_service


def _get_indicator_or_404(db: Session, indicator_id: int) -> HealthIndicator:
    indicator = db.get(HealthIndicator, indicator_id)
    if indicator is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Health indicator not found")
    return indicator


def _get_package_rule_or_404(db: Session, rule_id: int) -> PackageRule:
    rule = db.get(PackageRule, rule_id)
    if rule is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Package rule not found")
    return rule


def _get_question_or_404(db: Session, question_id: int) -> Question:
    question = db.execute(_questions_query().where(Question.id == question_id)).scalar_one_or_none()
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    return question


def _get_answer_or_404(db: Session, answer_id: int) -> Answer:
    query = select(Answer).options(selectinload(Answer.effects)).where(Answer.id == answer_id)
    answer = db.execute(query).scalar_one_or_none()
    if answer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found")
    return answer


def _get_answer_effect_or_404(db: Session, effect_id: int) -> AnswerEffect:
    effect = db.get(AnswerEffect, effect_id)
    if effect is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer effect not found")
    return effect


def _validate_indicator_links(db: Session, indicator_ids: list[int]) -> None:
    ids = set(indicator_ids)
    if not ids:
        return
    count = len(db.execute(select(HealthIndicator.id).where(HealthIndicator.id.in_(ids))).scalars().all())
    if count != len(ids):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Linked health indicator does not exist")


def _normalize_package_data(data: dict) -> dict:
    if data.get("checkout_url") is not None:
        data["checkout_url"] = str(data["checkout_url"])
    return data

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db
from app.models.entities import AnswerOption, Package, Question, Submission
from app.api.v1.deps import get_current_admin
from app.schemas.package import PackageCreate, PackageRead, PackageUpdate
from app.schemas.question import AnswerOptionCreate, AnswerOptionRead, AnswerOptionUpdate, QuestionCreate, QuestionRead, QuestionUpdate
from app.schemas.submission import SubmissionRead

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_admin)],
)


@router.post("/packages", response_model=PackageRead, status_code=status.HTTP_201_CREATED)
def create_package(payload: PackageCreate, db: Session = Depends(get_db)) -> Package:
    package = Package(**payload.model_dump())
    db.add(package)
    db.commit()
    db.refresh(package)
    return package


@router.get("/packages", response_model=list[PackageRead])
def list_packages(db: Session = Depends(get_db)) -> list[Package]:
    return list(db.execute(select(Package).order_by(Package.id)).scalars().all())


@router.get("/packages/{package_id}", response_model=PackageRead)
def get_package(package_id: int, db: Session = Depends(get_db)) -> Package:
    return _get_package_or_404(db, package_id)


@router.patch("/packages/{package_id}", response_model=PackageRead)
def update_package(package_id: int, payload: PackageUpdate, db: Session = Depends(get_db)) -> Package:
    package = _get_package_or_404(db, package_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
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


@router.post("/questions", response_model=QuestionRead, status_code=status.HTTP_201_CREATED)
def create_question(payload: QuestionCreate, db: Session = Depends(get_db)) -> Question:
    _validate_package_links(db, [option.package_id for option in payload.answer_options])
    data = payload.model_dump(exclude={"answer_options"})
    question = Question(**data)
    question.answer_options = [AnswerOption(**option.model_dump()) for option in payload.answer_options]
    db.add(question)
    db.commit()
    db.refresh(question)
    return _get_question_or_404(db, question.id)


@router.get("/questions", response_model=list[QuestionRead])
def list_questions(db: Session = Depends(get_db)) -> list[Question]:
    query = select(Question).options(selectinload(Question.answer_options)).order_by(Question.position, Question.id)
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
    return _get_question_or_404(db, question.id)


@router.delete("/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(question_id: int, db: Session = Depends(get_db)) -> Response:
    question = _get_question_or_404(db, question_id)
    db.delete(question)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/questions/{question_id}/options", response_model=AnswerOptionRead, status_code=status.HTTP_201_CREATED)
def create_answer_option(question_id: int, payload: AnswerOptionCreate, db: Session = Depends(get_db)) -> AnswerOption:
    _get_question_or_404(db, question_id)
    _validate_package_links(db, [payload.package_id])
    option = AnswerOption(question_id=question_id, **payload.model_dump())
    db.add(option)
    db.commit()
    db.refresh(option)
    return option


@router.patch("/options/{option_id}", response_model=AnswerOptionRead)
def update_answer_option(option_id: int, payload: AnswerOptionUpdate, db: Session = Depends(get_db)) -> AnswerOption:
    option = _get_option_or_404(db, option_id)
    data = payload.model_dump(exclude_unset=True)
    _validate_package_links(db, [data.get("package_id")])
    for field, value in data.items():
        setattr(option, field, value)
    db.commit()
    db.refresh(option)
    return option


@router.delete("/options/{option_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer_option(option_id: int, db: Session = Depends(get_db)) -> Response:
    option = _get_option_or_404(db, option_id)
    db.delete(option)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/submissions", response_model=list[SubmissionRead])
def list_submissions(db: Session = Depends(get_db)) -> list[Submission]:
    query = (
        select(Submission)
        .options(selectinload(Submission.answers), selectinload(Submission.recommended_package))
        .order_by(Submission.id.desc())
    )
    return list(db.execute(query).scalars().all())


def _get_package_or_404(db: Session, package_id: int) -> Package:
    package = db.get(Package, package_id)
    if package is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Package not found")
    return package


def _get_question_or_404(db: Session, question_id: int) -> Question:
    query = select(Question).options(selectinload(Question.answer_options)).where(Question.id == question_id)
    question = db.execute(query).scalar_one_or_none()
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    return question


def _get_option_or_404(db: Session, option_id: int) -> AnswerOption:
    option = db.get(AnswerOption, option_id)
    if option is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer option not found")
    return option


def _validate_package_links(db: Session, package_ids: list[int | None]) -> None:
    ids = {package_id for package_id in package_ids if package_id is not None}
    if not ids:
        return
    count = len(db.execute(select(Package.id).where(Package.id.in_(ids))).scalars().all())
    if count != len(ids):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Linked package does not exist")

from pydantic import BaseModel, Field, model_validator

from app.models.entities import QuestionType


class AnswerOptionBase(BaseModel):
    text: str = Field(min_length=1)
    package_id: int | None = None
    score: int = Field(default=0, ge=0)
    position: int = Field(default=0, ge=0)
    is_active: bool = True


class AnswerOptionCreate(AnswerOptionBase):
    pass


class AnswerOptionUpdate(BaseModel):
    text: str | None = Field(default=None, min_length=1)
    package_id: int | None = None
    score: int | None = Field(default=None, ge=0)
    position: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class AnswerOptionRead(AnswerOptionBase):
    id: int
    question_id: int

    model_config = {"from_attributes": True}


class QuestionBase(BaseModel):
    text: str = Field(min_length=5)
    help_text: str | None = None
    question_type: QuestionType = QuestionType.single
    position: int = Field(default=0, ge=0)
    is_active: bool = True


class QuestionCreate(QuestionBase):
    answer_options: list[AnswerOptionCreate] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_options(self) -> "QuestionCreate":
        if len(self.answer_options) < 2:
            raise ValueError("question must contain at least two answer options")
        return self


class QuestionUpdate(BaseModel):
    text: str | None = Field(default=None, min_length=5)
    help_text: str | None = None
    question_type: QuestionType | None = None
    position: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class QuestionRead(QuestionBase):
    id: int
    answer_options: list[AnswerOptionRead] = []

    model_config = {"from_attributes": True}

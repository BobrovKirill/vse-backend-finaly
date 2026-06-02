from pydantic import BaseModel, Field, model_validator

from app.models.entities import QuestionType


class AnswerEffectBase(BaseModel):
    indicator_id: int
    score: int = Field(default=0, ge=0)


class AnswerEffectCreate(AnswerEffectBase):
    pass


class AnswerEffectUpdate(BaseModel):
    indicator_id: int | None = None
    score: int | None = Field(default=None, ge=0)


class AnswerEffectRead(AnswerEffectBase):
    id: int
    answer_id: int

    model_config = {"from_attributes": True}


class AnswerBase(BaseModel):
    text: str = Field(min_length=1)
    description: str | None = None
    position: int = Field(default=0, ge=0)
    is_active: bool = True


class AnswerCreate(AnswerBase):
    effects: list[AnswerEffectCreate] = Field(default_factory=list)


class AnswerUpdate(BaseModel):
    text: str | None = Field(default=None, min_length=1)
    description: str | None = None
    position: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class AnswerRead(AnswerBase):
    id: int
    question_id: int
    effects: list[AnswerEffectRead] = []

    model_config = {"from_attributes": True}


class QuestionBase(BaseModel):
    text: str = Field(min_length=5)
    help_text: str | None = None
    question_type: QuestionType = QuestionType.single
    position: int = Field(default=0, ge=0)
    is_active: bool = True


class QuestionCreate(QuestionBase):
    answers: list[AnswerCreate] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_answers(self) -> "QuestionCreate":
        if len(self.answers) < 2:
            raise ValueError("question must contain at least two answers")
        return self


class QuestionUpdate(BaseModel):
    text: str | None = Field(default=None, min_length=5)
    help_text: str | None = None
    question_type: QuestionType | None = None
    position: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class QuestionRead(QuestionBase):
    id: int
    answers: list[AnswerRead] = []

    model_config = {"from_attributes": True}


class PublicAnswerRead(AnswerBase):
    id: int
    question_id: int

    model_config = {"from_attributes": True}


class PublicQuestionRead(QuestionBase):
    id: int
    answers: list[PublicAnswerRead] = []

    model_config = {"from_attributes": True}

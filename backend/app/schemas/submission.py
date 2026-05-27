from pydantic import BaseModel, Field, model_validator

from app.schemas.package import PackageRead


class PublicAnswer(BaseModel):
    question_id: int
    answer_option_ids: list[int] = Field(min_length=1)


class SubmissionCreate(BaseModel):
    contact_name: str | None = Field(default=None, max_length=255)
    contact_phone: str | None = Field(default=None, max_length=64)
    answers: list[PublicAnswer] = Field(min_length=1)

    @model_validator(mode="after")
    def question_ids_must_be_unique(self) -> "SubmissionCreate":
        ids = [answer.question_id for answer in self.answers]
        if len(ids) != len(set(ids)):
            raise ValueError("each question can be submitted only once")
        return self


class SubmissionAnswerRead(BaseModel):
    question_id: int
    answer_option_id: int

    model_config = {"from_attributes": True}


class SubmissionRead(BaseModel):
    id: int
    contact_name: str | None
    contact_phone: str | None
    total_score: int
    recommended_package: PackageRead | None
    answers: list[SubmissionAnswerRead]

    model_config = {"from_attributes": True}


class RecommendationRead(BaseModel):
    submission_id: int
    recommended_package: PackageRead | None
    total_score: int

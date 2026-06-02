from pydantic import BaseModel, Field, model_validator

from app.schemas.package import PackageRead


class PublicAnswer(BaseModel):
    question_id: int
    answer_ids: list[int] = Field(min_length=1)


class ChoiceCreate(BaseModel):
    contact_name: str | None = Field(default=None, max_length=255)
    contact_phone: str | None = Field(default=None, max_length=64)
    answers: list[PublicAnswer] = Field(min_length=1)

    @model_validator(mode="after")
    def question_ids_must_be_unique(self) -> "ChoiceCreate":
        ids = [answer.question_id for answer in self.answers]
        if len(ids) != len(set(ids)):
            raise ValueError("each question can be submitted only once")
        return self


class ChoiceAnswerRead(BaseModel):
    answer_id: int

    model_config = {"from_attributes": True}


class ChoiceIndicatorScoreRead(BaseModel):
    indicator_id: int
    score: int

    model_config = {"from_attributes": True}


class ChoicePackageRecommendationRead(BaseModel):
    rank: int
    matched_weight: int
    package: PackageRead

    model_config = {"from_attributes": True}


class ChoiceRead(BaseModel):
    id: int
    contact_name: str | None
    contact_phone: str | None
    total_score: int
    recommended_packages: list[ChoicePackageRecommendationRead]
    answers: list[ChoiceAnswerRead]
    indicator_scores: list[ChoiceIndicatorScoreRead]

    model_config = {"from_attributes": True}


class RecommendationRead(BaseModel):
    choice_id: int
    recommended_packages: list[ChoicePackageRecommendationRead]
    total_score: int
    indicator_scores: list[ChoiceIndicatorScoreRead]

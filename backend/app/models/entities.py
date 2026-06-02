from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class QuestionType(str, Enum):
    single = "single"
    multiple = "multiple"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class HealthIndicator(Base):
    __tablename__ = "health_indicators"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    answer_effects: Mapped[list["AnswerEffect"]] = relationship(back_populates="indicator")
    package_rules: Mapped[list["PackageRule"]] = relationship(back_populates="indicator")
    choice_scores: Mapped[list["ChoiceIndicatorScore"]] = relationship(back_populates="indicator")


class Package(Base):
    __tablename__ = "packages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    checkout_url: Mapped[str | None] = mapped_column(String(2048))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    rules: Mapped[list["PackageRule"]] = relationship(
        back_populates="package",
        cascade="all, delete-orphan",
    )
    services: Mapped[list["PackageService"]] = relationship(
        back_populates="package",
        cascade="all, delete-orphan",
        order_by="PackageService.position",
    )
    recommendations: Mapped[list["ChoicePackageRecommendation"]] = relationship(
        back_populates="package",
    )


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    help_text: Mapped[str | None] = mapped_column(Text)
    question_type: Mapped[QuestionType] = mapped_column(String(20), default=QuestionType.single.value)
    position: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    answers: Mapped[list["Answer"]] = relationship(
        back_populates="question",
        cascade="all, delete-orphan",
        order_by="Answer.position",
    )


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    position: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    question: Mapped[Question] = relationship(back_populates="answers")
    effects: Mapped[list["AnswerEffect"]] = relationship(
        back_populates="answer",
        cascade="all, delete-orphan",
    )
    choice_answers: Mapped[list["ChoiceAnswer"]] = relationship(back_populates="answer")


class AnswerEffect(Base):
    __tablename__ = "answer_effects"
    __table_args__ = (UniqueConstraint("answer_id", "indicator_id"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    answer_id: Mapped[int] = mapped_column(ForeignKey("answers.id", ondelete="CASCADE"), nullable=False)
    indicator_id: Mapped[int] = mapped_column(ForeignKey("health_indicators.id"), nullable=False)
    score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    answer: Mapped[Answer] = relationship(back_populates="effects")
    indicator: Mapped[HealthIndicator] = relationship(back_populates="answer_effects")


class PackageRule(Base):
    __tablename__ = "package_rules"
    __table_args__ = (UniqueConstraint("package_id", "indicator_id"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    package_id: Mapped[int] = mapped_column(ForeignKey("packages.id", ondelete="CASCADE"), nullable=False)
    indicator_id: Mapped[int] = mapped_column(ForeignKey("health_indicators.id"), nullable=False)
    min_score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_score: Mapped[int | None] = mapped_column(Integer)
    weight: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    package: Mapped[Package] = relationship(back_populates="rules")
    indicator: Mapped[HealthIndicator] = relationship(back_populates="package_rules")


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[float | None] = mapped_column(Numeric(10, 2))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    packages: Mapped[list["PackageService"]] = relationship(
        back_populates="service",
    )


class PackageService(Base):
    __tablename__ = "packages_services"
    __table_args__ = (UniqueConstraint("package_id", "service_id"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    package_id: Mapped[int] = mapped_column(ForeignKey("packages.id", ondelete="CASCADE"), nullable=False)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), nullable=False)
    position: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    package: Mapped[Package] = relationship(back_populates="services")
    service: Mapped[Service] = relationship(back_populates="packages")


class Choice(Base):
    __tablename__ = "choices"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    contact_name: Mapped[str | None] = mapped_column(String(255))
    contact_phone: Mapped[str | None] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    answers: Mapped[list["ChoiceAnswer"]] = relationship(
        back_populates="choice",
        cascade="all, delete-orphan",
    )
    indicator_scores: Mapped[list["ChoiceIndicatorScore"]] = relationship(
        back_populates="choice",
        cascade="all, delete-orphan",
    )
    recommended_packages: Mapped[list["ChoicePackageRecommendation"]] = relationship(
        back_populates="choice",
        cascade="all, delete-orphan",
        order_by="ChoicePackageRecommendation.rank",
    )

    @property
    def total_score(self) -> int:
        return sum(item.score for item in self.indicator_scores)


class ChoiceAnswer(Base):
    __tablename__ = "choices_answers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    choice_id: Mapped[int] = mapped_column(ForeignKey("choices.id", ondelete="CASCADE"), nullable=False)
    answer_id: Mapped[int] = mapped_column(ForeignKey("answers.id"), nullable=False)

    choice: Mapped[Choice] = relationship(back_populates="answers")
    answer: Mapped[Answer] = relationship(back_populates="choice_answers")


class ChoiceIndicatorScore(Base):
    __tablename__ = "choices_indicator_scores"
    __table_args__ = (UniqueConstraint("choice_id", "indicator_id"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    choice_id: Mapped[int] = mapped_column(ForeignKey("choices.id", ondelete="CASCADE"), nullable=False)
    indicator_id: Mapped[int] = mapped_column(ForeignKey("health_indicators.id"), nullable=False)
    score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    choice: Mapped[Choice] = relationship(back_populates="indicator_scores")
    indicator: Mapped[HealthIndicator] = relationship(back_populates="choice_scores")


class ChoicePackageRecommendation(Base):
    __tablename__ = "choices_package_recommendations"
    __table_args__ = (
        UniqueConstraint("choice_id", "package_id"),
        UniqueConstraint("choice_id", "rank"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    choice_id: Mapped[int] = mapped_column(ForeignKey("choices.id", ondelete="CASCADE"), nullable=False)
    package_id: Mapped[int] = mapped_column(ForeignKey("packages.id"), nullable=False)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    matched_weight: Mapped[int] = mapped_column(Integer, nullable=False)

    choice: Mapped[Choice] = relationship(back_populates="recommended_packages")
    package: Mapped[Package] = relationship(back_populates="recommendations")

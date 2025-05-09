from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlmodel import JSON, Column, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.models import User  # noqa: F401
    from app.models.sel_skill import SelSkill  # noqa: F401


class SelQuizBase(SQLModel):
    question: str | None = Field(
        default=None,
        max_length=255,
        title="Question",
        description="Question of the story",
    )
    options: list[str] | None = Field(
        default=None,
        title="Options",
        description="List of options for the question",
        sa_column=Column(JSON),
    )
    answer: str | None = Field(
        default=None,
        title="Answer",
        description="Correct answer to the question",
    )
    explanation: str | None = Field(
        default=None,
        title="Explanation",
        description="Explanation of the correct answer",
    )
    skill_id: int | None = Field(foreign_key="sel_skill.id")
    created_by_id: int | None = Field(
        foreign_key="user.id",
        title="Created By",
        description="User who created the warm-up",
    )


class SelQuizCreate(SelQuizBase):
    pass


class SelQuiz(SelQuizBase, table=True):
    __tablename__ = "sel_quiz"
    id: int | None = Field(default=None, primary_key=True)
    created_date: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    modified_date: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": datetime.now(timezone.utc)},
    )
    is_active: bool = Field(default=True)
    is_deleted: bool = Field(default=False)
    skill: Optional["SelSkill"] = Relationship(back_populates="quizs")
    created_by: Optional["User"] = Relationship(back_populates="quizs")


class SelQuizPublic(SelQuizBase):
    id: int
    created_date: datetime
    modified_date: datetime
    is_active: bool
    is_deleted: bool


class SelQuizUpdate(SelQuizBase):
    pass

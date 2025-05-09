from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlmodel import JSON, Column, Field, Relationship, SQLModel

# from app.models import SelActivity, SelQuiz, SelStory, SelWarmUp

if TYPE_CHECKING:
    from app.models.models import User  # noqa: F401
    from app.models.sel_activity import SelActivity  # noqa: F401
    from app.models.sel_quiz import SelQuiz  # noqa: F401
    from app.models.sel_story import SelStory  # noqa: F401
    from app.models.sel_warmup import SelWarmUp  # noqa: F401


class SelSkillBase(SQLModel):
    name: str | None = Field(
        default=None,
        max_length=255,
        title="Name",
        description="Name of the skill",
    )
    description: str | None = Field(
        default=None,
        max_length=255,
        title="Description",
        description="Description of the skill",
    )
    examples: list[str] | None = Field(
        default=None,
        title="Examples",
        description="Examples of the skill",
        sa_column=Column(JSON),
    )


class SelSkillCreate(SelSkillBase):
    pass


class SelSkill(SelSkillBase, table=True):
    __tablename__ = "sel_skill"
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
    warmups: list["SelWarmUp"] = Relationship(back_populates="skill")
    quizs: list["SelQuiz"] = Relationship(back_populates="skill")
    activities: list["SelActivity"] = Relationship(back_populates="skill")
    stories: list["SelStory"] = Relationship(back_populates="skill")


class SelSkillPublic(SelSkillBase):
    id: int
    created_date: datetime
    modified_date: datetime
    is_active: bool
    is_deleted: bool


class SelSkillUpdate(SelSkillBase):
    pass

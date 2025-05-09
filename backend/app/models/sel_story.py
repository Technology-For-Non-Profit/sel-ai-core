from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.models import User  # noqa: F401
    from app.models.sel_skill import SelSkill  # noqa: F401


class SelStoryBase(SQLModel):
    title: str | None = Field(
        default=None,
        max_length=255,
        title="Title",
        description="Title of the story",
    )
    overview: str | None = Field(
        default=None,
        max_length=255,
        title="Overview",
        description="Overview of the story",
    )
    detailed_story: str | None = Field(
        default=None,
        title="Detailed Story",
        description="Detailed story details",
    )
    skill_id: int | None = Field(foreign_key="sel_skill.id")
    created_by_id: int | None = Field(
        foreign_key="user.id",
        title="Created By",
        description="User who created the warm-up",
    )


class SelStoryCreate(SelStoryBase):
    pass


class SelStory(SelStoryBase, table=True):
    __tablename__ = "sel_story"
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
    skill: Optional["SelSkill"] = Relationship(back_populates="stories")
    created_by: Optional["User"] = Relationship(back_populates="stories")


class SelStoryPublic(SelStoryBase):
    id: int
    created_date: datetime
    modified_date: datetime
    is_active: bool
    is_deleted: bool


class SelStoryUpdate(SelStoryBase):
    pass

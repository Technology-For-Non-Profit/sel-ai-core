from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlmodel import JSON, Column, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.models import User  # noqa: F401
    from app.models.sel_skill import SelSkill  # noqa: F401


class SelActivityBase(SQLModel):
    name: str | None = Field(
        default=None,
        max_length=255,
        title="Name",
        description="Name of the activity",
    )
    description: str | None = Field(
        default=None,
        max_length=255,
        title="Description",
        description="Description of the activity",
    )
    detailed_activity: list[str] | None = Field(
        default=None,
        title="Detailed Activity",
        description="Detailed activities for the warm-up",
        sa_column=Column(JSON),
    )
    skill_id: int | None = Field(foreign_key="sel_skill.id")
    created_by_id: int | None = Field(
        foreign_key="user.id",
        title="Created By",
        description="User who created the warm-up",
    )


class SelActivityCreate(SelActivityBase):
    pass


class SelActivity(SelActivityBase, table=True):
    __tablename__ = "sel_activity"
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
    skill: Optional["SelSkill"] = Relationship(back_populates="activities")
    created_by: Optional["User"] = Relationship(back_populates="activities")


class SelActivityPublic(SelActivityBase):
    id: int
    created_date: datetime
    modified_date: datetime
    is_active: bool
    is_deleted: bool


class SelActivityUpdate(SelActivityBase):
    pass

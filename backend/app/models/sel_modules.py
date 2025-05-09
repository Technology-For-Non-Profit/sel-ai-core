from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class SelModulesBase(SQLModel):
    name: str | None = Field(
        default=None,
        max_length=255,
        title="Name",
        description="Name of the module",
    )
    description: str | None = Field(
        default=None,
        title="Description",
        description="Description of the module",
    )


class SelModulesCreate(SelModulesBase):
    pass


class SelModules(SelModulesBase, table=True):
    __tablename__ = "sel_modules"
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


class SelModulesPublic(SelModulesBase):
    id: int
    created_date: datetime
    modified_date: datetime
    is_active: bool
    is_deleted: bool


class SelModulesUpdate(SelModulesBase):
    pass

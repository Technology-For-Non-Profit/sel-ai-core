from fastapi import APIRouter, HTTPException
from sqlmodel import not_, select

from app.api.deps import SessionDep
from app.models import (
    SelActivity,
    SelActivityCreate,
    SelActivityPublic,
    SelActivityUpdate,
)

router = APIRouter(prefix="/skill-activity", tags=["skill-activity"])


# Create a Skill
@router.post(
    "/",
    response_model=SelActivityPublic,
    # dependencies=[Depends(permission_dependency("create_location"))],
)
def create_activity(
    *,
    sel_activity_create: SelActivityCreate,
    session: SessionDep,
) -> SelActivityPublic:
    """
    Create a new skill.
    """
    sel_activity = SelActivity.model_validate(sel_activity_create)
    session.add(sel_activity)
    session.commit()
    session.refresh(sel_activity)
    return sel_activity


# Get all Skills
@router.get(
    "/",
    response_model=list[SelActivityPublic],
    # dependencies=[Depends(permission_dependency("read_location"))],
)
def get_all_skills(
    *,
    session: SessionDep,
    skill_id: int | None = None,
) -> list[SelActivityPublic]:
    """
    Get all skills.
    """
    query = select(SelActivity).where(not_(SelActivity.is_deleted))

    if skill_id is not None:
        query = query.where(SelActivity.skill_id == skill_id)
    sel_activities = session.exec(query).all()
    return sel_activities


# Get a Skill by ID
@router.get(
    "/{sel_activity_id}",
    response_model=SelActivityPublic,
    # dependencies=[Depends(permission_dependency("read_location"))],
)
def get_skill_by_id(
    *,
    sel_activity_id: int,
    session: SessionDep,
) -> SelActivityPublic:
    """
    Get a skill by ID.
    """
    sel_activity = session.get(SelActivity, sel_activity_id)
    if not sel_activity:
        raise HTTPException(status_code=404, detail="Skill not found")
    return sel_activity


# Update a Skill
@router.put(
    "/{sel_activity_id}",
    response_model=SelActivityPublic,
    # dependencies=[Depends(permission_dependency("update_location"))],
)
def update_skill(
    *,
    sel_activity_id: int,
    sel_activity_update: SelActivityUpdate,
    session: SessionDep,
) -> SelActivityPublic:
    """
    Update a skill.
    """
    sel_activity = session.get(SelActivity, sel_activity_id)
    if not sel_activity or sel_activity.is_deleted is True:
        raise HTTPException(status_code=404, detail="Skill not found")
    sel_activity_data = SelActivity.model_validate(sel_activity_update)
    sel_activity_data.id = sel_activity.id
    session.add(sel_activity_data)
    session.commit()
    session.refresh(sel_activity_data)
    return sel_activity_data

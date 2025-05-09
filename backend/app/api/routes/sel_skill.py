from fastapi import APIRouter, HTTPException
from sqlmodel import not_, select

from app.api.deps import SessionDep
from app.models import SelSkill, SelSkillCreate, SelSkillPublic

router = APIRouter(prefix="/skill", tags=["skill"])


# Create a Skill
@router.post(
    "/",
    response_model=SelSkillPublic,
    # dependencies=[Depends(permission_dependency("create_location"))],
)
def create_block(
    *,
    sel_skill_create: SelSkillCreate,
    session: SessionDep,
) -> SelSkillPublic:
    """
    Create a new skill.
    """
    sel_skill = SelSkill.model_validate(sel_skill_create)
    session.add(sel_skill)
    session.commit()
    session.refresh(sel_skill)
    return sel_skill


# Get all Skills
@router.get(
    "/",
    response_model=list[SelSkillPublic],
    # dependencies=[Depends(permission_dependency("read_location"))],
)
def get_all_skills(
    *,
    session: SessionDep,
) -> list[SelSkillPublic]:
    """
    Get all skills.
    """
    sel_skills = session.exec(select(SelSkill).where(not_(SelSkill.is_deleted))).all()
    return sel_skills


# Get a Skill by ID
@router.get(
    "/{sel_skill_id}",
    response_model=SelSkillPublic,
    # dependencies=[Depends(permission_dependency("read_location"))],
)
def get_skill_by_id(
    *,
    sel_skill_id: int,
    session: SessionDep,
) -> SelSkillPublic:
    """
    Get a skill by ID.
    """
    sel_skill = session.get(SelSkill, sel_skill_id)
    if not sel_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return sel_skill


# Update a Skill
@router.put(
    "/{sel_skill_id}",
    response_model=SelSkillPublic,
    # dependencies=[Depends(permission_dependency("update_location"))],
)
def update_skill(
    *,
    sel_skill_id: int,
    sel_skill_update: SelSkillCreate,
    session: SessionDep,
) -> SelSkillPublic:
    """
    Update a skill.
    """
    sel_skill = session.get(SelSkill, sel_skill_id)
    if not sel_skill or sel_skill.is_deleted is True:
        raise HTTPException(status_code=404, detail="Skill not found")
    sel_skill_data = SelSkill.model_validate(sel_skill_update)
    sel_skill_data.id = sel_skill.id
    session.add(sel_skill_data)
    session.commit()
    session.refresh(sel_skill_data)
    return sel_skill_data

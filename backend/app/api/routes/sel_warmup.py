from fastapi import APIRouter, HTTPException
from sqlmodel import not_, select

from app.api.deps import SessionDep
from app.models import SelWarmUp, SelWarmUpCreate, SelWarmUpPublic, SelWarmUpUpdate

router = APIRouter(prefix="/skill-warmup", tags=["skill-warmup"])


# Create a Skill
@router.post(
    "/",
    response_model=SelWarmUpPublic,
    # dependencies=[Depends(permission_dependency("create_location"))],
)
def create_warmup(
    *,
    sel_warmup_create: SelWarmUpCreate,
    session: SessionDep,
) -> SelWarmUpPublic:
    """
    Create a new warmup.
    """
    sel_warmup = SelWarmUp.model_validate(sel_warmup_create)
    session.add(sel_warmup)
    session.commit()
    session.refresh(sel_warmup)
    return sel_warmup


# Get all Skills
@router.get(
    "/",
    response_model=list[SelWarmUpPublic],
    # dependencies=[Depends(permission_dependency("read_location"))],
)
def get_all_skills(
    *,
    session: SessionDep,
    skill_id: int | None = None,
) -> list[SelWarmUpPublic]:
    """
    Get all skills.
    """
    query = select(SelWarmUp).where(not_(SelWarmUp.is_deleted))

    if skill_id is not None:
        query = query.where(SelWarmUp.skill_id == skill_id)

    sel_warmups = session.exec(query).all()
    return sel_warmups


# Get Warmup Module by ID
@router.get(
    "/{sel_skill_id}",
    response_model=SelWarmUpPublic,
    # dependencies=[Depends(permission_dependency("read_location"))],
)
def get_skill_by_id(
    *,
    sel_warmup_id: int,
    session: SessionDep,
) -> SelWarmUpPublic:
    """
    Get a warmup by ID.
    """
    sel_warmup = session.get(SelWarmUp, sel_warmup_id)
    if not sel_warmup:
        raise HTTPException(status_code=404, detail="Warmup not found")
    return sel_warmup


# Update a Skill
@router.put(
    "/{sel_warmup_id}",
    response_model=SelWarmUpPublic,
    # dependencies=[Depends(permission_dependency("update_location"))],
)
def update_skill(
    *,
    sel_warmup_id: int,
    sel_skill_update: SelWarmUpUpdate,
    session: SessionDep,
) -> SelWarmUpPublic:
    """
    Update a skill.
    """
    sel_warmup = session.get(SelWarmUp, sel_warmup_id)
    if not sel_warmup or sel_warmup.is_deleted is True:
        raise HTTPException(status_code=404, detail="Warmup not found")
    sel_warmup_data = SelWarmUp.model_validate(sel_skill_update)
    sel_warmup_data.id = sel_warmup.id
    session.add(sel_warmup_data)
    session.commit()
    session.refresh(sel_warmup_data)
    return sel_warmup_data

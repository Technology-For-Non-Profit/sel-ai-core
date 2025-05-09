from fastapi import APIRouter, HTTPException
from sqlmodel import not_, select

from app.api.deps import SessionDep
from app.models import SelStory, SelStoryCreate, SelStoryPublic, SelStoryUpdate

router = APIRouter(prefix="/skill-story", tags=["skill-story"])


# Create a Skill
@router.post(
    "/",
    response_model=SelStoryPublic,
    # dependencies=[Depends(permission_dependency("create_location"))],
)
def create_activity(
    *,
    sel_quiz_create: SelStoryCreate,
    session: SessionDep,
) -> SelStoryPublic:
    """
    Create a new skill.
    """
    sel_story = SelStory.model_validate(sel_quiz_create)
    session.add(sel_story)
    session.commit()
    session.refresh(sel_story)
    return sel_story


# Get all Skills
@router.get(
    "/",
    response_model=list[SelStoryPublic],
    # dependencies=[Depends(permission_dependency("read_location"))],
)
def get_all_skills(
    *,
    session: SessionDep,
) -> list[SelStoryPublic]:
    """
    Get all skills.
    """
    sel_stories = session.exec(select(SelStory).where(not_(SelStory.is_deleted))).all()
    return sel_stories


# Get a Skill by ID
@router.get(
    "/{sel_quiz_id}",
    response_model=SelStoryPublic,
    # dependencies=[Depends(permission_dependency("read_location"))],
)
def get_skill_by_id(
    *,
    sel_quiz_id: int,
    session: SessionDep,
) -> SelStoryPublic:
    """
    Get a skill by ID.
    """
    sel_story = session.get(SelStory, sel_quiz_id)
    if not sel_story:
        raise HTTPException(status_code=404, detail="Skill not found")
    return sel_story


# Update a Skill
@router.put(
    "/{sel_quiz_id}",
    response_model=SelStoryPublic,
    # dependencies=[Depends(permission_dependency("update_location"))],
)
def update_skill(
    *,
    sel_quiz_id: int,
    sel_quiz_update: SelStoryUpdate,
    session: SessionDep,
) -> SelStoryPublic:
    """
    Update a skill.
    """
    sel_story = session.get(SelStory, sel_quiz_id)
    if not sel_story or sel_story.is_deleted is True:
        raise HTTPException(status_code=404, detail="Skill not found")
    sel_story_data = SelStory.model_validate(sel_quiz_update)
    sel_story_data.id = sel_story.id
    session.add(sel_story_data)
    session.commit()
    session.refresh(sel_story_data)
    return sel_story_data

from fastapi import APIRouter, HTTPException
from sqlmodel import not_, select

from app.api.deps import SessionDep
from app.models import SelQuiz, SelQuizCreate, SelQuizPublic, SelQuizUpdate

router = APIRouter(prefix="/skill-quiz", tags=["skill-quiz"])


# Create a Quiz
@router.post(
    "/",
    response_model=SelQuizPublic,
    # dependencies=[Depends(permission_dependency("create_location"))],
)
def create_activity(
    *,
    sel_quiz_create: SelQuizCreate,
    session: SessionDep,
) -> SelQuizPublic:
    """
    Create a new quiz.
    """
    sel_quiz = SelQuiz.model_validate(sel_quiz_create)
    session.add(sel_quiz)
    session.commit()
    session.refresh(sel_quiz)
    return sel_quiz


# Get all Quizzes  # Updated comment
@router.get(
    "/",
    response_model=list[SelQuizPublic],
    # dependencies=[Depends(permission_dependency("read_location"))],
)
def get_all_quizzes(
    *,
    session: SessionDep,
) -> list[SelQuizPublic]:
    """
    Get all quizzes.
    """
    sel_quizzes = session.exec(select(SelQuiz).where(not_(SelQuiz.is_deleted))).all()
    return sel_quizzes


# Get a Quiz by ID
@router.get(
    "/{sel_quiz_id}",
    response_model=SelQuizPublic,
    # dependencies=[Depends(permission_dependency("read_location"))],
)
def get_quiz_by_id(
    *,
    sel_quiz_id: int,
    session: SessionDep,
) -> SelQuizPublic:
    """
    Get a quiz by ID.
    """
    sel_quiz = session.get(SelQuiz, sel_quiz_id)
    if not sel_quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return sel_quiz


# Update a Quiz
@router.put(
    "/{sel_quiz_id}",
    response_model=SelQuizPublic,
    # dependencies=[Depends(permission_dependency("update_location"))],
)
def update_quiz(
    *,
    sel_quiz_id: int,
    sel_quiz_update: SelQuizUpdate,
    session: SessionDep,
) -> SelQuizPublic:
    """
    Update a quiz.
    """
    sel_quiz = session.get(SelQuiz, sel_quiz_id)
    if not sel_quiz or sel_quiz.is_deleted is True:
        raise HTTPException(status_code=404, detail="Quiz not found")
    sel_quiz_data = SelQuiz.model_validate(sel_quiz_update)
    sel_quiz_data.id = sel_quiz.id
    session.add(sel_quiz_data)
    session.commit()
    session.refresh(sel_quiz_data)
    return sel_quiz_data

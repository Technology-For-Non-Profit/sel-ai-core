import os
from typing import Any

from app.models.models import User
from app.models.sel_activity import SelActivity
from app.models.sel_quiz import SelQuiz
from app.models.sel_story import SelStory
from dotenv import load_dotenv
from fastapi import APIRouter, Body, HTTPException, Query

from app.api.deps import CurrentUser, SessionDep, get_llm_response
from app.core.config import extract_json_from_llm_output
from app.models.sel_skill import SelSkill
from app.models.sel_warmup import SelWarmUp
from sqlmodel import select

router = APIRouter(prefix="/llm", tags=["sel-llm"])

# api_key = settings.GEMINI_API_KEY
# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment variables
api_key = os.getenv("GEMINI_API_KEY")


# Get Response for warmup
@router.post(
    "/warmup",
    response_model=None,
    # dependencies=[Depends(permission_dependency("read_location"))],
)
def get_ai_warmup(
    session: SessionDep,
    skill_id: int = Query(None),
    age: str = Body(8),
    state: str = Body("Uttar Pradesh"),
    language: str = Body("Hindi"),
    response_amount: int = Body(3),
) -> Any:
    """
    Get response for warmup.
    """

    current_user = session.exec(
        select(User).where(User.email == "admin@example.com")
    ).first()
    print("Current user ID:", current_user)

    skill_obj = session.get(SelSkill, skill_id)  # `skill` is the ID
    if not skill_obj:
        raise HTTPException(status_code=404, detail="Skill not found")

    skill_name = skill_obj.name
    skill_description = skill_obj.description

    # fmt: off
    prompt = f"I am a Social and Emotional Learning (SEL) facilitator. I am conducting a session on the skill of {skill_name}. This skill is described as {skill_description}. The age group for the session are children of age {age}. They are from the state of {state} in India. Kindly help me with creative ideas to start the session. It can involve interacting with the students and asking them questions to warmup the session. Respond only with the JSON array, and do not wrap it in markdown-style code block like ```json. Example : [{{'idea': 'Sharing a Feeling Face Story', 'purpose': 'To gently introduce the concept of recognizing emotions in others. By sharing a simple story about a time they saw someone showing a particular emotion (happy, sad, surprised), they start thinking about outward expressions of feelings without directly focusing on empathy yet. This can make them comfortable sharing and listening.', 'reflective_questions': ['Think about a time you saw someone look really happy. What do you think made them feel that way?', 'Can you remember a time someone looked a little sad? What might have happened?', 'Have you ever seen someone look surprised? What could have caused that surprise?']}}, {{...}}] The response should be in the language {language}. Kindly provide {response_amount} such responses."
    # fmt: on
    result = get_llm_response(prompt=prompt)

    result = extract_json_from_llm_output(result)

    print("Current user:", current_user.id)

    warmup_list = []
    for current_result in result:
        # Create a new SelWarmUpPublic instance
        warmup = SelWarmUp(
            skill_id=skill_id,
            created_by_id=current_user.id,
            idea=current_result["idea"],
            purpose=current_result["purpose"],
            reflective_questions=current_result["reflective_questions"],
        )
        # Add the new instance to the warmup list
        warmup_list.append(warmup)
    session.add_all(warmup_list)
    session.commit()

    print(f"LLM response: {result}")

    return result


# Get Response for warmup
@router.post(
    "/quiz",
    response_model=None,
    # dependencies=[Depends(permission_dependency("read_location"))],
)
def get_ai_quiz(
    session: SessionDep,
    skill_id: int = Query(None),
    age: str = Body(8),
    state: str = Body("Uttar Pradesh"),
    language: str = Body("Hindi"),
    response_amount: int = Body(3),
) -> Any:
    """
    Get response for warmup.
    """
    skill_obj = session.get(SelSkill, skill_id)  # `skill` is the ID
    if not skill_obj:
        raise HTTPException(status_code=404, detail="Skill not found")

    current_user = session.exec(
        select(User).where(User.email == "admin@example.com")
    ).first()

    skill_name = skill_obj.name
    skill_description = skill_obj.description

    # fmt: off
    prompt = f"I am a Social and Emotional Learning (SEL) facilitator. I am conducting a session on the skill of {skill_name}. This skill is described as {skill_description}. The age group for the session are children of age {age}. They are from the state of {state} in India. To make the students understand the skill better, I want to conduct a quiz in the classroom. Kindly suggest some interesting quiz questions. Respond only with the JSON array, and do not wrap it in markdown-style code block like ```json. Example : [{{'question': 'Which of the following best shows critical thinking?', 'options': ['Memorising facts for a test','Accepting everything your friend says','Asking questions to understand better','Repeating what the teacher said'], 'answer': 2, 'explanation': 'Critical thinking involves asking questions and analyzing information rather than just accepting it at face value.'}}, {{...}}]. In the example, the answer should point to the index of the array of the right answer. The response should be in the language {language}. Kindly provide {response_amount} such responses."

    result = get_llm_response(prompt=prompt)
    # fmt: on
    result = get_llm_response(prompt=prompt)

    result = extract_json_from_llm_output(result)

    quiz_list = []
    for current_result in result:
        # Create a new SelQuizPublic instance
        quiz = SelQuiz(
            skill_id=skill_id,
            created_by_id=current_user.id,
            question=current_result["question"],
            options=current_result["options"],
            answer=current_result["answer"],
            explanation=current_result["explanation"],
        )
        # Add the new instance to the quiz list
        quiz_list.append(quiz)
    session.add_all(quiz_list)
    session.commit()

    print(f"LLM response: {result}")

    return result


# Get Response for activity
@router.post(
    "/activity",
    response_model=None,
    # dependencies=[Depends(permission_dependency("read_location"))],
)
def get_ai_activity(
    session: SessionDep,
    skill_id: int = Query(None),
    age: str = Body(8),
    state: str = Body("Uttar Pradesh"),
    language: str = Body("Hindi"),
    response_amount: int = Body(3),
) -> Any:
    """
    Get response for warmup.
    """
    skill_obj = session.get(SelSkill, skill_id)  # `skill` is the ID
    if not skill_obj:
        raise HTTPException(status_code=404, detail="Skill not found")

    current_user = session.exec(
        select(User).where(User.email == "admin@example.com")
    ).first()

    skill_name = skill_obj.name
    skill_description = skill_obj.description

    # fmt: off
    prompt = f"I am a Social and Emotional Learning (SEL) facilitator. I am conducting a session on the skill of {skill_name}. This skill is described as {skill_description}. The age group for the session are children of age {age}. They are from the state of {state} in India. Kindly suggest me some interesting interactive activities which I can conduct in the classroom so that students will have fun and also learn about the skill. Respond only with the JSON array, and do not wrap it in markdown-style code block like ```json. Example: [{{'name': 'Identify Five Red Flags in the Text', 'description': 'Read the story and identify five red flags that indicate a lack of empathy.', 'detailed_activity': ['<div style=\\'background-color:#FFF3E0; border:2px solid #FB8C00; border-radius:10px; padding:15px;\\'>Step 1: Read the short story provided by the teacher.</div>', '<div style=\\'background-color:#FFE0B2; border:2px solid #F57C00; border-radius:10px; padding:15px;\\'>Step 2: Highlight or note down any actions or behaviors that seem unfair or unkind.</div>', '<div style=\\'background-color:#FFCC80; border:2px solid #EF6C00; border-radius:10px; padding:15px;\\'>Step 3: Discuss in pairs why these actions could be red flags for empathy.</div>', '<div style=\\'background-color:#FFB74D; border:2px solid #E65100; border-radius:10px; padding:15px;\\'>Step 4: Share your five red flags with the class.</div>', '<div style=\\'background-color:#FFA726; border:2px solid #D84315; border-radius:10px; padding:15px;\\'>Step 5: Reflect on what could have been done differently to show empathy.</div>']}},...] If you observe the shared example, in the JSON response for interactive activity, the field 'detailed_activity' is an array. Here, each element of the array is one step in that activity. The response should be in the language {language}. Kindly provide {response_amount} such responses."
                   # fmt: on
    result = get_llm_response(prompt=prompt)

    result = extract_json_from_llm_output(result)

    activity_list = []
    for current_result in result:
        # Create a new SelActivityPublic instance
        activity = SelActivity(
            skill_id=skill_id,
            created_by_id=current_user.id,
            name=current_result["name"],
            description=current_result["description"],
            detailed_activity=current_result["detailed_activity"],
        )
        # Add the new instance to the activity list
        activity_list.append(activity)
    session.add_all(activity_list)
    session.commit()

    print(f"LLM response: {result}")

    return result


# Get Response for story
@router.post(
    "/story",
    response_model=None,
    # dependencies=[Depends(permission_dependency("read_location"))],
)
def get_ai_story(
    session: SessionDep,
    skill_id: int = Query(None),
    age: str = Body(8),
    state: str = Body("Uttar Pradesh"),
    language: str = Body("Hindi"),
    response_amount: int = Body(2),
) -> Any:
    """
    Get response for story.
    """
    skill_obj = session.get(SelSkill, skill_id)  # `skill` is the ID
    if not skill_obj:
        raise HTTPException(status_code=404, detail="Skill not found")

    skill_name = skill_obj.name
    skill_description = skill_obj.description

    current_user = session.exec(
        select(User).where(User.email == "admin@example.com")
    ).first()

    # fmt: off
    prompt = f"""I am a Social and Emotional Learning (SEL) facilitator. I am conducting a session on the skill of {skill_name}. This skill is described as '{skill_description}'. The age group for the session are children of age {age}. They are from the state of '{state}' in India. I want to come up with an interesting story to make the students learn and reflect on the skill. Suggest me some stories which I can read aloud and discuss in the class.Keep the detailed story colorful and large for student to read. Respond only with the JSON array, and do not wrap it in markdown-style code block like ```json. Example [{{"title": "सोनू की पतंग", "overview": "यह कहानी एक छोटे बच्चे सोनू की है, जो अपनी पतंग के साथ आसमान में उड़ने का सपना देखता है।", "detailed_story": "<div style=\'border: 2px dashed #FF69B4; padding: 20px; color: #2E8B57; font-family: \'Comic Sans MS\'; background-color: #F0F8FF;\'>सोनू हर साल पतंगबाजी प्रतियोगिता में भाग लेता था, लेकिन इस बार उसका पतंग उड़ाना कुछ खास था। उसके पतंग की डोर जब आसमान में लहराई, तो वह खुशी से झूम उठा।</div>"}}]. The response should be in the language '{language }'. Kindly provide {response_amount} such responses."""

     # fmt: on
    result = get_llm_response(prompt=prompt)

    result = extract_json_from_llm_output(result)

    print("Result of story-->", result)

    story_list = []
    for current_result in result:
        # Create a new SelStory instance
        story = SelStory(
            skill_id=skill_id,
            created_by_id=current_user.id,
            title=current_result["title"],
            overview=current_result["overview"],
            detailed_story=current_result["detailed_story"],
        )
        # Add the new instance to the story list
        story_list.append(story)
    session.add_all(story_list)
    session.commit()

    print(f"LLM response: {result}")

    return result

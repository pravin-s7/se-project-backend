from models.model import FlashCard, FlashCardUpdate, SuccessCreateResponse, SuccessDeleteResponse
from fastapi import APIRouter, Security
from models.model import User
from utils.response import objectEntity, objectsEntity
from database.db import db
from typing import Annotated, List
from utils.security import get_current_active_user
from utils.validation import AlreadyExistsError, NotExistsError, NotFoundError
from bson import ObjectId
from ai.run_model import search_generate_flashcard


flashcard = APIRouter(prefix="/flashcard", tags=["Flash cards"])


@flashcard.post("/generate")
async def generate_flashcard(
    flashcard_input: FlashCard,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
) -> FlashCard:
    find = db.flashcard.find(filter={"course_id": flashcard_input.course_id})
    if not find:
        raise NotFoundError("Could not find the course")

    _in = db.flashcard.insert_one(
        {
            "user_email_id": current_user.email,
            "course_id": flashcard_input.course_id,
            "week": flashcard_input.week,
            "title": flashcard_input.title,
            "content": search_generate_flashcard(
                flashcard_input.course_id, flashcard_input.week, flashcard_input.title
            ),
        }
    )

    if _in.acknowledged:
        find = db.flashcard.find_one(
            filter={"_id": ObjectId(_in.inserted_id)}
        )
        
        return objectEntity(find)
    else:
        raise AlreadyExistsError()


@flashcard.post("/create")
async def create_flashcard(
    flashcard_input: FlashCard,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
) -> SuccessCreateResponse:
    _in = db.flashcard.insert_one(
        {
            "user_email_id": current_user.email,
            "course_id": flashcard_input.course_id,
            "week": flashcard_input.week,
            "title": flashcard_input.title,
            "content": flashcard_input.content,
        }
    )

    if _in.acknowledged:
        return {"message": "success", "db_entry_id": str(_in.inserted_id)}
    else:
        raise AlreadyExistsError()


@flashcard.get("/get/course/{course_id}")
async def get_c_flash_card(
    course_id: str,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
) -> List[FlashCard]:
    find = db.flashcard.find(
        filter={"course_id": course_id, "user_email_id": current_user.email}
    )
    if find:
        return objectsEntity(find)
    raise NotExistsError()


@flashcard.get("/get/course/{course_id}/week/{week_id}")
async def get_flash_card(
    course_id: str,
    week_id: int,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
) -> List[FlashCard]:
    find = db.flashcard.find(
        filter={
            "course_id": course_id,
            "user_email_id": current_user.email,
            "week": week_id,
        }
    )
    if find:
        return objectsEntity(find)
    raise NotExistsError()


@flashcard.put("/update/{flashcard_id}")
async def update_flash_card(
    flashcard_id: str,
    flashcard_input: FlashCardUpdate,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
) -> SuccessCreateResponse:
    find = db.flashcard.find_one(
        filter={"_id": ObjectId(flashcard_id), "user_email_id": current_user.email}
    )
    if not find:
        raise NotExistsError()

    update = {}
    if flashcard_input.title:
        update["title"] = flashcard_input.title
    if flashcard_input.content:
        update["content"] = flashcard_input.content

    updated = db.flashcard.update_one({"_id": ObjectId(flashcard_id)}, {"$set": update})
    return {"message": "success", "db_entry_id": flashcard_id}


@flashcard.delete("/delete/{flashcard_id}")
async def delete_flash_card(
    flashcard_id: str,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
)-> SuccessDeleteResponse:
    filter = {"_id": ObjectId(flashcard_id), "user_email_id": current_user.email}
    find = db.flashcard.find_one(
        filter=filter
    )
    if not find:
        raise NotFoundError()
    
    db.flashcard.delete_one(filter)

    return {'message': 'success'}
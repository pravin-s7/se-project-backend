from fastapi import APIRouter, Security, Path
from models.user import User
from utils.response import objectEntity, objectsEntity

from database.db import db
from models.flashcard import FlashCard, FlashCardUpdate
from typing import Annotated
from utils.security import get_current_active_user
from utils.validation import AlreadyExistsError, NotExistsError, NotFoundError
from ai.colab_request import search_generate_flashcard

from bson import ObjectId

fc = APIRouter(prefix="/flash_card", tags=["Flash Card"])

@fc.post('/create')
async def create_flash_card(
    flash_card: FlashCard,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])]
):
    flash_card.user_id = current_user.user_id

    # check whether the user has enrolled in that course or not
    if flash_card.course_id not in current_user.courses:
        raise ValueError("User has not enrolled in this courses")
    
    fashcard_in = db.flashcard.insert_one(dict(flash_card))
    return {"message": "success", "db_entry_id": str(fashcard_in.inserted_id)}

@fc.get('/get/{card_id}')
async def get_flash_card(
    flash_card_id: str,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])]
) -> FlashCard:
    card = db.flashcard.find_one({"_id": ObjectId(flash_card_id)})
    if card is None:
        raise NotExistsError()
    return FlashCard(**card)

@fc.put('/update/{card_id}')
async def update_flash_card(
    flash_card_id: str,
    flash_card : FlashCardUpdate,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])]
):
    try:
        db.flashcard.find_one_and_update({"_id": ObjectId(flash_card_id)}, {"$set": dict(flash_card)})
    except:
        raise NotExistsError()
    return {"msg": "FlashCard Updated successfully"}

    
@fc.delete('/delete/{card_id}')
async def delete_flash_card(
    flash_card_id: str,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])]
):
    try:
        db.flashcard.find_one_and_delete({"_id": ObjectId(flash_card_id)})
    except:
        raise NotExistsError()
    return {"msg": "FlashCard deleted successfully"}


@fc.post("/generate")
async def generate_flashcard(
    flashcard_input: FlashCard,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
) -> FlashCard:
    find = db.course.find(filter={"course_id": flashcard_input.course_id})
    if not find:
        raise NotFoundError("Could not find the course")

    _in = db.flashcard.insert_one(
        {
            "user_email_id": current_user.user_id,
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

    
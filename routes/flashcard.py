from fastapi import APIRouter, Security, Path, HTTPException
from models.user import User
from utils.response import objectEntity, objectsEntity, responses

from database.db import db
from models.flashcard import FlashCard, FlashCardUpdate
from typing import Annotated
from utils.security import get_current_active_user
from utils.validation import AlreadyExistsError, NotExistsError, NotFoundError
from ai.colab_request import search_generate_flashcard

from bson import ObjectId

fc = APIRouter(prefix="/flash_card", tags=["Flashcard"])


@fc.post("/create", status_code=201, responses=responses)
async def create_flash_card(
    flash_card: FlashCard,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
):
    flash_card.user_id = current_user.user_id

    # check whether the user has enrolled in that course or not
    if flash_card.course_id not in current_user.courses:
        raise HTTPException(404, "User has not enrolled in this courses")

    fashcard_in = db.flashcard.insert_one(dict(flash_card))
    return {"message": "success", "db_entry_id": str(fashcard_in.inserted_id)}


# @fc.get("/get/{flash_card_id}", responses=responses)
@fc.get("/getall", responses=responses)
async def get_flash_cards(
    # flash_card_id: str,
    # current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
)   :
    try:
        flashcards = db.flashcard.find()
        
        # Convert cursor to a list and convert ObjectId to string
        flashcards_list = []
        for card in flashcards:
            card['_id'] = str(card['_id'])  # Convert ObjectId to string
            flashcards_list.append(card)
        
        # If no flashcards found, raise an error
        if not flashcards_list:
            raise NotExistsError()

        # Return the list of flashcards
        return flashcards_list
    except Exception as e:
        raise HTTPException(500, str(e))
    # except:
    #     raise HTTPException(422, "Invalid ID")
    # if card is None:
    #     raise NotExistsError()
    # return FlashCard(**card)


@fc.put("/update/{flash_card_id}", status_code=202, responses=responses)
async def update_flash_card(
    flash_card_id: str,
    flash_card: FlashCardUpdate,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
):
    try:
        find = db.flashcard.find_one({"_id": ObjectId(flash_card_id)})
    except:
        raise HTTPException(422, "Invalid ID")
    if not find:
        raise NotExistsError()
    try:
        db.flashcard.find_one_and_update(
            {"_id": ObjectId(flash_card_id)}, {"$set": dict(flash_card)}
        )
    except:
        raise NotExistsError()
    return {"message": "FlashCard Updated successfully"}


@fc.delete("/delete/{flash_card_id}", responses=responses)
async def delete_flash_card(
    flash_card_id: str,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
):
    try:
        card = db.flashcard.find_one({"_id": ObjectId(flash_card_id)})
    except:
        raise HTTPException(422, "Invalid ID")
    if not card:
        raise NotExistsError()
    try:
        db.flashcard.find_one_and_delete({"_id": ObjectId(flash_card_id)})
    except:
        raise NotExistsError()
    return {"message": "FlashCard deleted successfully"}


@fc.post("/generate", responses=responses)
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
        find = db.flashcard.find_one(filter={"_id": ObjectId(_in.inserted_id)})

        return objectEntity(find)
    else:
        raise AlreadyExistsError()

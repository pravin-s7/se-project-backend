from fastapi import APIRouter, Security, HTTPException
from models.user import User
from utils.response import objectEntity, objectsEntity, responses

from database.db import db
from typing import Annotated

from utils.security import get_current_active_user
from models.model import SuccessCreateResponse
from models.course import Notes, NotesUpdate
from utils.validation import AlreadyExistsError, NotExistsError
from bson import ObjectId

notes = APIRouter(prefix="/notes", tags=["Notes"])


@notes.post("/create", status_code=201, responses=responses)
async def create_notes(
    notes_input: Notes,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
) -> SuccessCreateResponse:
    course = db.course.find_one(filter={"course_id": notes_input.course_id})
    if not course:
        raise NotExistsError()
    material_in = db.notes.insert_one(dict(notes_input))

    if material_in.acknowledged:
        return {"message": "success", "db_entry_id": str(material_in.inserted_id)}
    else:
        raise AlreadyExistsError()


@notes.get("/get/{course_id}", responses=responses)
async def get_notes(
    course_id: str,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
):
    course = db.course.find_one(filter={"course_id": course_id})
    if not course:
        raise NotExistsError()
    find = db.notes.find(filter={"course_id": course_id})
    return objectsEntity(find)


@notes.put(
    "/update/{notes_id}", status_code=202, responses=responses
)
async def update_notes(
    notes_id: str,
    notes_input: NotesUpdate,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
):
    try:
        find = db.notes.find_one(filter={"_id": ObjectId(notes_id)})
    except:
        raise HTTPException(422, "Invalid ID")
    if not find:
        raise NotExistsError()

    updated = db.notes.update_one(
        {"_id": ObjectId(notes_id)}, {"$set": dict(notes_input)}
    )
    return {"message": "success", "db_entry_id": notes_id}


@notes.delete("/delete/{notes_id}", responses=responses)
async def delete_notes(
    notes_id: str,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
):
    try:
        find = db.notes.find_one(filter={"_id": ObjectId(notes_id)})
    except:
        raise HTTPException(422, "Invalid ID")
    if not find:
        raise NotExistsError()

    deleted = db.notes.delete_one({"_id": ObjectId(notes_id)})
    print(deleted)
    return {"msg": "Notes Deleted"}
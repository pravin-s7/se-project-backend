from fastapi import APIRouter, Security
from models.model import User
from utils.response import objectEntity, objectsEntity

from database.db import db
from typing import Annotated

from utils.security import get_current_active_user
from models.model import Course, SuccessCreateResponse
from utils.validation import AlreadyExistsError, NotExistsError

course = APIRouter(prefix="/course", tags=["Course"])


@course.post(
    "/create",
)
async def create_course(
    course_input: Course,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
) -> SuccessCreateResponse:
    find = db.course.find_one(filter={"course_id": course_input.course_id})
    if find:
        raise AlreadyExistsError("Duplicated Course ID")
    course_in = db.course.insert_one(
        {
            "course_id": course_input.course_id,
            "course_name": course_input.course_name,
        }
    )
    if course_in.acknowledged:
        return {"message": "success", "db_entry_id": str(course_in.inserted_id)}
    else:
        raise AlreadyExistsError()


@course.get("/get/{course_id}")
async def get_course(
    course_id: str,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
):
    find = db.course.find_one(filter={"course_id": course_id})
    if find:
        return objectEntity(find)
    raise NotExistsError()


@course.put("/update/{course_id}")
async def update_course(
    course_id: str,
    course_input: Course,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
):
    find = db.course.find_one(filter={"course_id": course_id})
    if not find:
        return NotExistsError()

    update = {}
    if course_input.course_name:
        update["course_name"] = course_input.course_name

    updated = db.course.update_one({"course_id": course_id}, update)
    print(updated)
    return {"message": "success", "db_entry_id": str(updated.inserted_id)}

from fastapi import APIRouter, Security
from models.user import User
from utils.response import objectEntity, objectsEntity, responses

from database.db import db
from typing import Annotated

from utils.security import get_current_active_user
from models.model import SuccessCreateResponse
from models.course import Course, CourseMaterial, CourseMaterialUpdate
from utils.validation import AlreadyExistsError, NotExistsError
from bson import ObjectId

course_material = APIRouter(prefix="/course_material", tags=["Course Material"])


@course_material.post(
    "/create", status_code=201, responses=responses
)
async def create_course_material(
    course_material_input: CourseMaterial,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
) -> SuccessCreateResponse:

    material_in = db.course_material.insert_one(dict(course_material_input))

    if material_in.acknowledged:
        return {"msg": "success", "db_entry_id": str(material_in.inserted_id)}
    else:
        raise AlreadyExistsError()


@course_material.get("/get/{course_id}", responses=responses)
async def get_course_material(
    course_id: str,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
):
    find = db.course_material.find(filter={"course_id": course_id})
    return objectsEntity(find)


@course_material.put("/update/{course_material_id}", status_code=202, responses=responses)
async def update_course_material(
    course_material_id: str,
    course_material_input: CourseMaterialUpdate,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
):
    find = db.course_material.find_one(filter={"_id": ObjectId(course_material_id)})
    if not find:
        raise NotExistsError()

    updated = db.course_material.update_one(
        {"_id": ObjectId(course_material_id)}, {"$set": dict(course_material_input)}
    )
    return {"msg": "success", "db_entry_id": course_material_id}

@course_material.delete("/delete/{course_material_id}", responses=responses)
async def delete_course_material(
    course_material_id: str,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
):
    find = db.course_material.find_one(filter={"_id": ObjectId(course_material_id)})
    if not find:
        raise NotExistsError()

    deleted = db.course_material.delete_one({'_id': ObjectId(course_material_id)})
    print(deleted)
    return {"msg": "Course Material Deleted"}




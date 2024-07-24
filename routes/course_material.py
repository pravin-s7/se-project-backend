from fastapi import APIRouter, Security
from models.model import User
from utils.response import objectEntity, objectsEntity

from database.db import db
from typing import Annotated

from utils.security import get_current_active_user
from models.model import CourseMaterial, SuccessCreateResponse, CourseMaterialUpdate
from utils.validation import AlreadyExistsError, NotExistsError
from ai.chroma_vector import insertIntoEmbeddings
from bson import ObjectId

course_material = APIRouter(prefix="/course_material", tags=["Course Material"])


@course_material.post(
    "/create",
)
async def create_course_material(
    course_material_input: CourseMaterial,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
) -> SuccessCreateResponse:

    material_in = db.course_material.insert_one(
        {
            "course_id": course_material_input.course_id,
            "material_type": course_material_input.material_type,
            "url": course_material_input.url,
            "content": course_material_input.content,
            "week": course_material_input.week,
        }
    )

    # print(course_material_input.content)
    if course_material_input.material_type == "notes":
        insertIntoEmbeddings(
            course_material_input.course_id,
            course_material_input.week,
            course_material_input.content,
        )

    if material_in.acknowledged:
        return {"message": "success", "db_entry_id": str(material_in.inserted_id)}
    else:
        raise AlreadyExistsError()


@course_material.get("/get/{course_id}")
async def get_course_material(
    course_id: str,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
):
    find = db.course_material.find(filter={"course_id": course_id})
    if find:
        return objectsEntity(find)
    raise NotExistsError()


@course_material.put("/update/{course_material_id}")
async def update_course_material(
    course_material_id: str,
    course_material_input: CourseMaterialUpdate,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
):
    find = db.course_material.find_one(filter={"_id": ObjectId(course_material_id)})
    if not find:
        raise NotExistsError()

    update = {}
    if course_material_input.material_type:
        update["material_type"] = course_material_input.material_type
    if course_material_input.url:
        update["url"] = course_material_input.url
    if course_material_input.content:
        update["content"] = course_material_input.content
    if course_material_input.week:
        update["week"] = course_material_input.week

    updated = db.course_material.update_one(
        {"_id": ObjectId(course_material_id)}, {"$set": update}
    )
    return {"message": "success", "db_entry_id": course_material_id}

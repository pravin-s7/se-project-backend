from fastapi import APIRouter, Security, Depends, HTTPException, Query
from models.user import User
from utils.response import objectEntity, objectsEntity, convert_to_serializable

from database.db import db
from database.pipeline import get_course_pipeline, get_course_pipeline_week
from typing import Annotated

from utils.security import get_current_active_user
from models.model import SuccessCreateResponse
from models.course import Course
from models.assignment import AssignmentType
from utils.validation import AlreadyExistsError, NotExistsError

course = APIRouter(prefix="/course", tags=["Course"])


@course.post("/create")
async def create_course(
    course_input: Course,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
) -> SuccessCreateResponse:
    find = db.course.find_one(filter={"course_id": course_input.course_id})
    if find:
        raise AlreadyExistsError("Duplicated Course ID")
    course_in = db.course.insert_one(dict(course_input))
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

    updated = db.course.update_one({"course_id": course_id}, {"$set": update})
    print(updated)
    return {"message": "success", "db_updated_id": str(updated.upserted_id)}

# get all course_material by passing course_id respectice to the weeks
@course.get("/course_material/{course_id}")
async def get_course_materials(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
    course_id: str
):
    find = db.course.find_one(filter={"course_id": course_id})
    if not find:
        return NotExistsError()
    c_materials = db.course_material.find({"course_id": course_id})
    return objectsEntity(c_materials)


# get all assignment by passinig course_id, assignment_type, week
@course.get("/get_contents")
async def get_course_contents(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
    course_id: str
):
    find = db.course.find_one(filter={"course_id": course_id})
    if not find:
        return NotExistsError()
    
    pipeline = get_course_pipeline(course_id=course_id)
    results = db.course.aggregate(pipeline)
    return [convert_to_serializable(result) for result in results]


@course.get("/get_week_content")
async def get_course_week_contents(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
    course_id: str = Query,
    week: int = Query(le=12, ge=1)
):
    course = db.course.find_one({"course_id": course_id})
    if not course:
        raise NotExistsError()
    
    pipeline = get_course_pipeline_week(course_id=course_id, week=week)
    results = db.course.aggregate(pipeline)
    return [convert_to_serializable(result) for result in results]

@course.get('/get_assignment')
async def get_course_week_assignment(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
    course_id: str = Query,
    week: int = Query(le=12, ge=1),
    assgn_type: AssignmentType = Query(description="the type of the assignment")
):
    course = db.course.find_one({"course_id": course_id})
    if not course:
        raise NotExistsError()
    collection = db.assignment if assgn_type in ["AQ", "PA", "GrPA"] else db.coding_assignment

    results = collection.find({"course_id": course_id, "week": week, "assgn_type": assgn_type})

    return [convert_to_serializable(result) for result in results]
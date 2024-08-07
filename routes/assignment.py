from fastapi import APIRouter, Security, HTTPException
from models.user import User
from utils.response import objectEntity, objectsEntity, responses
from bson import ObjectId
from database.db import db
from typing import Annotated, List

from utils.security import get_current_active_user
from models.assignment import Assignment, AssignmentUpdate, ProgrammingAssignment
from utils.validation import AlreadyExistsError, NotExistsError

assgn = APIRouter(prefix="/assignment", tags=["Assignment"])

@assgn.post('/create', status_code=201, responses=responses)
async def create_question(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
    assignment: Assignment
):
    assignment_in = db.assignment.insert_one(dict(assignment))
    if assignment_in.acknowledged:
        return {"message": "success", "db_entry_id": str(assignment_in.inserted_id)}
    raise AlreadyExistsError()

@assgn.post('/create_many_questions', status_code=201, responses=responses)
async def create_many_questions(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
    assignments: List[Assignment]
):
    assignments_dicts = [dict(assignment) for assignment in assignments]

    result = db.assignment.insert_many(assignments_dicts)
    
    if result.acknowledged:
        return {"message": "success", "db_entry_ids": [str(id) for id in result.inserted_ids]}
    raise HTTPException(status_code=500, detail="An error occurred while inserting the assignments.")

@assgn.get('/get/{assgn_id}', responses=responses)
async def get_question(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
    assgn_id: str
):
    try: 
        ObjectId(assgn_id)
    except:
        raise HTTPException(status_code=422, detail="Invalid assignment id")
    assgn = db.assignment.find_one({"_id": ObjectId(assgn_id)})
    if not assgn:
        raise NotExistsError()
    return objectEntity(assgn)

@assgn.put('/update/{assgn_id}', status_code=202, responses=responses)
async def update_question(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
    assgn_id: str,
    assgn: AssignmentUpdate
):
    try: 
        ObjectId(assgn_id)
    except:
        raise HTTPException(status_code=422, detail="Invalid assignment id")
    assgn = db.assignment.find_one_and_update({"_id": ObjectId(assgn_id)}, {"$set": dict(assgn)})
    if not assgn:
        raise NotExistsError()
    return {"msg": "Assigment Updated"}

@assgn.delete('/delete/{assgn_id}', responses=responses)
async def delete_question(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
    assgn_id: str
):
    try: 
        ObjectId(assgn_id)
    except:
        raise HTTPException(status_code=422, detail="Invalid assignment id")
    assgn = db.assignment.delete_one({"_id": ObjectId(assgn_id)})
    if assgn.acknowledged:
        return {"msg": "Deleted Successfully"}
    raise NotExistsError()
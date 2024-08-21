from fastapi import APIRouter, Depends, Security, HTTPException, Path, Query
from typing import Annotated, List
from utils.security import get_current_active_user
from models.user import User
from models.assignment import AssignmentSubmissionForm, LastSubmission, AssignmentType
from models.model import GenerateResponse, AIQuery
from utils.response import objectsEntity, objectEntity, responses
from utils.validation import NotFoundError, NotExistsError
from bson import ObjectId
from ai.gemini import search_generate, generate
from datetime import datetime

from database.db import db

user=APIRouter(prefix='/user', tags=["User"])

@user.get('/me', responses=responses)
async def get_current_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@user.get("/get/course/{course_id}", responses=responses)
async def get_flash_card_course_filter(
    course_id: str,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
):
    find = db.course.find_one(filter={"course_id": course_id})
    if not find:
        raise NotFoundError("Could not find the course")
    
    f_cards = db.flashcard.find(
        filter={"course_id": course_id, "user_id": current_user.user_id}
    )
    
    return objectsEntity(f_cards)

@user.get("/get/course/{course_id}/week/{week_id}")
async def get_flash_card_course_and_week_filter(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
    course_id: str,
    week_id: int = Path(..., title="Week ID", ge=1, le=12)
):
    find = db.flashcard.find(
        filter={
            "course_id": course_id,
            "user_email_id": current_user.email,
            "week": week_id,
        }
    )
    return objectsEntity(find)


@user.get('/flashcards', responses=responses)
async def get_all_flashcards(current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])]):
    flash_cards = db.flashcard.find({"user_id": current_user.user_id})
    arr = objectsEntity(flash_cards)
    arr.reverse()
    return arr

@user.post('/search_generate')
async def search_and_generate_response(query: GenerateResponse):
    find = db.course.find(filter={"course_id": query.course_id})
    if not find:
        raise NotFoundError("Could not find the course")
    return {'response': search_generate(query.course_id, query.week, query.query)}

@user.post('/generate')
async def generate_response(query: AIQuery, current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])]):
    return {'response': generate(query.query)}

@user.post('/register_course', include_in_schema=False)
async def register_courses(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
    courses: List[str]
):
    print(courses)
    for c_id in courses:
        course = db.course.find_one({"course_id": c_id})
        if course is None:
            raise ValueError("Invalid Course_ID")
        
    register = db.user.update_one({"user_id": current_user.user_id}, {"$set": {"courses": courses}})

    if register.acknowledged:
       return {"msg": "Courses have been registered successfully"}
    
    raise HTTPException(status_code=500, detail="Something went wrong")


# Submitting the assignment answers by users

from utils.grading import *

@user.post('/submit_answers', responses=responses)
async def submit_answers(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
    submissions: List[AssignmentSubmissionForm]
):
    try:
        assignment_id = dict(submissions[0])['assgn_id']
        assignment = db.assignment.find_one({"_id": ObjectId(assignment_id)})
        coding_assignment = db.coding_assignment.find_one({"_id": ObjectId(assignment_id)})

        assgn = assignment if assignment else coding_assignment

        submission_dicts = [
            {
                **submission.dict(),               
                "assgn_id": ObjectId(submission.assgn_id),
                "user_id": current_user.user_id  
            }
            
            for submission in  submissions
        ]

        db.last_submission.update_one({ 
            "user_id": current_user.user_id,
            "course_id": assgn["course_id"],
            "week": assgn["week"],
            "assgn_type": assgn["assgn_type"]}, { "$set": {
                                        "user_id": current_user.user_id,
                                        "course_id": assgn["course_id"],
                                        "week": assgn["week"],
                                        "assgn_type": assgn["assgn_type"],
                                        "last_submission": datetime.now() }
        }, upsert=True)

        for submission in submission_dicts:
            db.submission.update_one(
                { "assgn_id": ObjectId(submission["assgn_id"]),
                "user_id": current_user.user_id }, 
                { "$set": submission }, 
                upsert=True
                )
            

        return {"message": "Assignment_submitted", "submission_time": datetime.now()}
    except:   
        raise HTTPException(status_code=500, detail="An error occurred while submitting the answers.")
   

@user.get('/get_marks', responses=responses)
async def submit_answers(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
    course_id: str
):
    user_marks = objectsEntity(db.marks.find({"course_id": course_id}).sort("week", 1))
    # Returuns the mark week_wise
    return user_marks

@user.get('/last_submission', responses=responses)
async def last_submission_time(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
    course_id: str,
    week: int = Query(le=12, ge=1),
    assgn_type: AssignmentType = Query(description="the type of the assignment")
):
    course = db.course.find_one({"course_id": course_id})
    if not course:
        raise NotExistsError()
    
    last_submission_time = db.last_submission.find({
        "user_id": current_user.user_id,
        "course_id": course_id,
        "assgn_type": assgn_type,
        "week": week
    })

    return objectsEntity(last_submission_time)
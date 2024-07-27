from fastapi import APIRouter, Depends, Security, HTTPException, Path
from typing import Annotated, List
from utils.security import get_current_active_user
from models.user import User
from models.assignment import AssignmentSubmissionForm
from utils.response import objectEntity, objectsEntity
from bson import ObjectId

from database.db import db

user=APIRouter(prefix='/user', tags=["User"])

@user.get('/all_users')
async def all_user():
    users = db.user.find()
    return objectsEntity(users)

@user.get('/me')
async def get_current_user(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@user.get("/get/course/{course_id}")
async def get_flash_card_course_filter(
    course_id: str,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
):
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


@user.get('/flashcards')
async def get_all_flashcards(current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])]):
    flash_cards = db.flashcard.find({"user_id": current_user.user_id}, {"title": 1, "content": 1})
    return objectsEntity(flash_cards)

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

@user.post('/submit_answer')
async def submit_answers(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
    submissions: List[AssignmentSubmissionForm]
):
    submission_dicts = [
        {
            **submission.dict(),               
            "assgn_id": ObjectId(submission.assgn_id),
            "user_id": current_user.user_id  
        }
        
        for submission in  submissions
    ]

    submit = db.submission.insert_many(submission_dicts)
    if submit.acknowledged:
        return {"message": "success", "db_entry_ids": [str(id) for id in submit.inserted_ids]}
    raise HTTPException(status_code=500, detail="An error occurred while submitting the answers.")
   

# Evaluate the assignment and store the marks consecutively for each week and assignment type
# As a background task with crontab


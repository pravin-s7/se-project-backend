from pydantic import BaseModel, Field, model_validator
from database.db import db
from typing import Optional
from utils.security import get_current_active_user

class FlashCard(BaseModel):
    user_id: Optional[str] = None
    course_id: str
    week: int = Field(ge=0, le=12)
    title: str
    content: str | None

    @model_validator(mode='before')
    def validate_user_and_course(cls, values):
        course_id = values.get('course_id')
        course = db.course.find_one({"course_id": course_id})
        if course is None:
            raise ValueError("Invalid Course_ID")
        return values


class FlashCardUpdate(BaseModel):
    week: int | None = Field(ge=1, le=12)
    title: str | None
    content: str | None
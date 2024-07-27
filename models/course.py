from pydantic import BaseModel, field_validator, HttpUrl, Field
from enum import Enum
from database.db import db

class MaterialType(str, Enum):
    video_url = "video_URL"
    file_url = "file_URL"
    pdf = "pdf"
    transcript = "transcript"
    notes = "notes"
    slides = "slides"


class CourseMaterial(BaseModel):
    course_id: str  # like CS01
    material_type: MaterialType
    url: str | None = None
    content: str | None = None
    week: int = Field(ge=0, le=12)

    @field_validator('url')
    def validate_url_format(cls, url):
        try:
            HttpUrl(url)
        except:
            raise ValueError("Invalid URL")
        return url
    
    @field_validator('course_id')
    def validate_course_id(cls, c_id):
        course = db.course.find_one({"course_id": c_id})
        if course is None:
            raise ValueError("Invalid Course_ID")
        return c_id

            
class CourseMaterialUpdate(BaseModel):
    material_type: MaterialType 
    url: str | None 
    content: str | None 
    week: int = Field(ge=0, le=12)

    @field_validator('url')
    def validate_url_format(cls, url):
        try:
            HttpUrl(url)
        except:
            raise ValueError("Invalid URL")
        return url

class Course(BaseModel):
    course_id: str
    course_name: str
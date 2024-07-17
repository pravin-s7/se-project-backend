from pydantic import BaseModel, validate_email, field_validator, EmailStr, Field, HttpUrl
from typing import List, Union, Optional
from enum import Enum
from datetime import datetime

class Role(str, Enum):
    student = "student"
    admin = "admin"
    user = "user"

class User(BaseModel):
    email : EmailStr
    name: str | None = None
    disabled: Optional[bool] = False 
    roles: List[Role]
    courses: Optional[List[str]] | None = [] # validate later

    @field_validator('email')
    def validate_email_format(cls, email):
        if not validate_email(email):
            raise ValueError('Invalid email format')
        return email    

class Semester(str, Enum):
    summer = "summer"
    winter = "winter"

class Courses(BaseModel):
    course_id: str
    course_name: str
    semester: List[Semester]
    year: int = Field(ge=2000)

class MaterialType(str, Enum):
    video_url = "video_URL"
    file_url = "file_URL"
    pdf = "pdf"
    transcript = "transcript"
    notes = "notes"
    slides = "slides"

class Week(str, Enum):
    W1 = "W1"
    W2 = "W2"
    W3 = "W3"
    W4 = "W4"
    W5 = "W5"
    W6 = "W6"
    W7 = "W7"
    W8 = "W8"
    W9 = "W9"
    W10 = "W10"
    W11 = "W11"
    W12 = "W12"

class CourseMaterial(BaseModel):
    course_id: str = Field(min_length=24, max_length=24)
    material_type: MaterialType
    url: HttpUrl
    content: str | None = None
    week: Week

class QuestionType(str, Enum):
    MSQ = "MSQ"
    MCQ = "MCQ"
    Numeric = "Numeric"
    String = "String"
    Float = "Float"

class AssignmentType(str, Enum):
    AQ = "AQ"
    PA = "PA"
    GA = "GA"
    PPA = "PPA"
    GrPA = "GrPA"

class Assignment(BaseModel):
    question: str
    q_type: QuestionType
    options: List[Union[int, str, float]]
    answers: List[Union[int, str, float]]
    assgn_type: AssignmentType
    course_id: str = Field(min_length=24, max_length=24)
    week: Week
    deadline: datetime = Field(..., description="Deadline in ISO format")

class CodeLanguage(str, Enum):
    python = "python"
    sql = "sql"
    java = "java"
    js = "js"

class ProgrammingAssignment(BaseModel):
    question: str
    language: CodeLanguage
    public_tc_input: List[Union[int, str, float, tuple, dict]]
    public_tc_output: List[Union[int, str, float, tuple, dict]]
    private_tc_input: List[Union[int, str, float, tuple, dict]]
    private_tc_output: List[Union[int, str, float, tuple, dict]]
    assgn_type: AssignmentType
    course_id: str = Field(min_length=24, max_length=24)
    week: Week
    deadline: datetime = Field(description="Deadline in ISO format")

class Submission(BaseModel):
    assgn_id: str = Field(min_length=24, max_length=24)
    user_id: str = Field(min_length=24, max_length=24)
    answer: list

class Marks(BaseModel):
    user_id: str = Field(min_length=24, max_length=24)
    assgn_id: str = Field(min_length=24, max_length=24)
    marks: int = Field(ge=0, le=100)


class FlashCards(BaseModel):
    user_id: str = Field(min_length=24, max_length=24)
    course_id: str = Field(min_length=24, max_length=24)
    title: str
    content: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str 
    scopes: list[str] = []

class LoginForm(BaseModel):
    email : str
    password: str
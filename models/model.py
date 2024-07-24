from pydantic import (
    BaseModel,
    validate_email,
    field_validator,
    EmailStr,
    Field,
    HttpUrl,
)
from typing import List, Union, Optional
from enum import Enum
from datetime import datetime


class Role(str, Enum):
    student = "student"
    admin = "admin"
    user = "user"


class User(BaseModel):
    email: EmailStr
    name: str | None = None
    disabled: Optional[bool] = False
    roles: List[Role]
    courses: Optional[List[str]] | None = []  # validate later

    @field_validator("email")
    def validate_email_format(cls, email):
        if not validate_email(email):
            raise ValueError("Invalid email format")
        return email


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
    url: Optional[HttpUrl] | None = None
    content: str | None = None
    week: int = Field(ge=0, le=12)


class CourseMaterialUpdate(BaseModel):
    material_type: MaterialType | None = None
    url: Optional[HttpUrl] | None = None
    content: str | None = None
    week: int | None = Field(ge=0, le=12)


class Course(BaseModel):
    course_id: str
    course_name: str


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
    week: int = Field(ge=0, le=12)
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
    week: int = Field(ge=0, le=12)
    deadline: datetime = Field(description="Deadline in ISO format")


class Submission(BaseModel):
    assgn_id: str = Field(min_length=24, max_length=24)
    user_id: str = Field(min_length=24, max_length=24)
    answer: list


class Marks(BaseModel):
    user_id: str = Field(min_length=24, max_length=24)
    assgn_id: str = Field(min_length=24, max_length=24)
    marks: int = Field(ge=0, le=100)


class FlashCard(BaseModel):
    course_id: str # like CS01
    week: int = Field(ge=0, le=12)
    title: str
    content: str | None

class FlashCardUpdate(BaseModel):
    title: str | None
    content: str | None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str
    scopes: list[str] = []


class LoginForm(BaseModel):
    email: str
    password: str


class SuccessCreateResponse(BaseModel):
    message: str
    db_entry_id: str = Field(min_length=24, max_length=24)

class SuccessDeleteResponse(BaseModel):
    message: str

class CodingAssignment(BaseModel):
    id: int
    question: str
    function: str
    explanation: str
    examples: List[dict]
    testCases: List[dict]
    deadline: datetime = Field(..., description="Deadline in ISO format")

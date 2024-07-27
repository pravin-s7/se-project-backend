from pydantic import BaseModel, field_validator, Field, model_validator
from enum import Enum
from typing import Optional, List, Union, Dict
from bson import ObjectId
from datetime import datetime
from database.db import db

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
    course_id: str
    week: int = Field(ge=0, le=12)
    deadline: datetime = Field(..., description="Deadline in ISO format")

    @field_validator('course_id')
    def validate_course_id(cls, c_id):
        course = db.course.find_one({"course_id": c_id})
        if course is None:
            raise ValueError("Invalid Course_ID")
        return c_id
    
    @field_validator('assgn_type')
    def validate_assgn_type(cls, assgn_type):
        if assgn_type not in ["AQ", "PA", "GA"]:
            raise ValueError("Invalid Assignment Type")
        return assgn_type
    
class CodeLanguage(str, Enum):
    python = "python"
    sql = "sql"
    java = "java"
    js = "js"


class ProgrammingAssignment(BaseModel):
    question: str
    language: CodeLanguage
    public_testcase: List[dict]
    private_testcase: List[dict]
    assgn_type: AssignmentType
    course_id: str
    week: int = Field(ge=0, le=12)
    deadline: datetime = Field(description="Deadline in ISO format")

    @model_validator(mode='before')
    def validate_testcases(cls, values):
        public_tc = values.get('public_testcase')
        private_tc = values.get('private_testcase')
        
        # Validate each test case
        for tc in public_tc + private_tc:
            if not isinstance(tc, dict):
                raise ValueError("Each test case should be a dictionary")
            elif set(tc.keys()) != {'input', 'output'}:
                raise ValueError("Each test case should only have 'input' and 'output' keys")
            elif not isinstance(tc['input'], list) or not isinstance(tc['output'], list):
                raise ValueError("Both 'input' and 'output' should be lists")
        return values

    @field_validator('course_id')
    def validate_course_id(cls, c_id):
        course = db.course.find_one({"course_id": c_id})
        if course is None:
            raise ValueError("Invalid Course_ID")
        return c_id
    
    @field_validator('assgn_type')
    def validate_assgn_type(cls, assgn_type):
        if assgn_type not in ["PPA", "GrPA"]:
            raise ValueError("Invalid Assignment Type")
        return assgn_type


class ProgrammingAssignmentUpdate(BaseModel):
    question: Optional[str] 
    language: Optional[CodeLanguage]
    public_testcase: Optional[List[dict]] 
    private_testcase: Optional[List[dict]] 
    assgn_type: Optional[AssignmentType] 
    week: Optional[int] = Field(ge=0, le=12)
    deadline: Optional[datetime] = Field(description="Deadline in ISO format")

    @model_validator(mode='before')
    def validate_testcases(cls, values):
        public_tc = values.get('public_testcase')
        private_tc = values.get('private_testcase')
        
        if (public_tc!=None) or (private_tc!=None):
            # Validate each test case
            for tc in public_tc + private_tc:
                if not isinstance(tc, dict):
                    raise ValueError("Each test case should be a dictionary")
                elif set(tc.keys()) != {'input', 'output'}:
                    raise ValueError("Each test case should only have 'input' and 'output' keys")
                elif not isinstance(tc['input'], list) or not isinstance(tc['output'], list):
                    raise ValueError("Both 'input' and 'output' should be lists")
        return values
    
    @field_validator('assgn_type')
    def validate_assgn_type(cls, assgn_type):
        if assgn_type not in ["PPA", "GrPA"]:
            raise ValueError("Invalid Assignment Type")
        return assgn_type

class AssignmentSubmissionForm(BaseModel):
    assgn_id: str = Field(min_length=24, max_length=24)
    user_id: Optional[str] = None
    answer: list

    @field_validator('assgn_id')
    def validate_assgn_id(cls, assgn_id):
        assgn = db.assignment.find_one({"_id": ObjectId(assgn_id)})
        coding_assgn = db.coding_assignment.find_one({"_id": ObjectId(assgn_id)})
        if (assgn is None) and (coding_assgn is None):
            raise ValueError("Invalid Assignment_ID")
        return assgn_id
    
    @field_validator('user_id')
    def validate_user_id(cls, user_id):
        user = db.user.find_one({"user_id": user_id})
        if user is None:
            raise ValueError("Invalid User_ID")
        return user_id


class Marks(BaseModel):
    user_id: str
    assgn_id: str = Field(min_length=24, max_length=24)
    marks: int = Field(ge=0, le=100)

    @field_validator('assgn_id')
    def validate_assgn_id(cls, assgn_id):
        assgn = db.assignment.find_one({"assgn_id": assgn_id})
        if assgn is None:
            raise ValueError("Invalid Assignment_ID")
        return assgn_id
    
    @field_validator('user_id')
    def validate_user_id(cls, user_id):
        user = db.user.find_one({"user_id": user_id})
        if user is None:
            raise ValueError("Invalid User_ID")
        return user_id

class AssignmentUpdate(BaseModel):
    question: Optional[str]
    q_type: Optional[QuestionType]
    options: Optional[List[Union[int, str, float]]]
    answers: Optional[List[Union[int, str, float]]]
    assgn_type: Optional[AssignmentType]
    week: Optional[int] = Field(ge=0, le=12)
    deadline: Optional[datetime] = Field(description="Deadline in ISO format")
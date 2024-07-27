from pydantic import (
    BaseModel,
    validate_email,
    field_validator,
    EmailStr,
)

from uuid import UUID

from typing import List, Optional
from enum import Enum

class Role(str, Enum):
    student = "student"
    admin = "admin"
    user = "user"


class User(BaseModel):
    user_id: str
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
    
    @field_validator("user_id")
    def validate_user_id(cls, user_id):
        try:
            UUID(user_id)
        except:
            raise ValueError("Invalid User_ID")
        return user_id
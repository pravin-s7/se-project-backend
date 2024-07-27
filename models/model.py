from pydantic import BaseModel, Field
class GenerateResponse(BaseModel):
    query: str
    course_id: str
    week: int = Field(ge=0, le=12)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str
    scopes: list[str] = []

class SuccessCreateResponse(BaseModel):
    message: str
    db_entry_id: str = Field(min_length=24, max_length=24)

class SuccessDeleteResponse(BaseModel):
    message: str
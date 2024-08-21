from fastapi import APIRouter, Security, Depends, HTTPException
from typing import Annotated
from models.user import User
from utils.response import objectEntity, objectsEntity, convert_to_serializable, responses

from database.db import db

from utils.security import get_current_active_user

genai = APIRouter(prefix="/gen_ai", tags=["Gen-AI"])


@genai.post('/summarize', responses=responses)
async def summarize(current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])]):
    return ""

@genai.post('/hints', responses=responses)
async def provide_hints(current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])]):
    return ""

@genai.post('/generate', responses=responses)
async def generate_responses( current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])]):
    return ""

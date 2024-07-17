from fastapi import APIRouter
from models.model import User
from utils.response import objectEntity, objectsEntity

from database.db import db

user=APIRouter(prefix='/user', tags=["User"])

@user.get('/all_users')
async def all_user():
    users = db.user.find()
    return objectsEntity(users)
    return "Returning all users from this endpoint"
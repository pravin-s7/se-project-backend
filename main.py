from fastapi import FastAPI, Security
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes.user import user
from routes.course import course
from routes.course_material import course_material
from routes.flashcard import flashcard
from utils.security import auth
from utils.response import responses
from utils.extra import tags_metadata


from models.model import User
from typing import Annotated
from utils.security import get_current_active_user


app = FastAPI(
    title="Study Buddy",
    summary="Description of the app", 
    description="Description from the description",
    version="1.0.0",
    openapi_tags=tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows these methods
    allow_headers=["*"],  # Allows all headers
)

# Adding a router
app.include_router(user)
app.include_router(auth)
app.include_router(course)
app.include_router(course_material)
app.include_router(flashcard)
# Mounting Static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Favicon of the app
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

# endpoint
@app.get('/', description="Home page", tags=["Home"], responses=responses)
async def home():
    return "Hello from Home page"

@app.get("/test")
async def read_users_me(user: User):
    return ""

@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
):
    return current_user


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app="main:app", host='0.0.0.0', port=8000, reload=True)
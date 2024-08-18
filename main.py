from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes.user import user
from routes.course import course
from routes.course_material import course_material
from routes.coding_assignments import coding_assignment
from routes.flashcard import fc
from routes.assignment import assgn
from routes.gen_ai import genai
from utils.security import auth
from utils.response import responses
from utils.extra import tags_metadata, description
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

app = FastAPI(
    title="Team-22 Learning Management Portal API",
    description=description,
    version="1.0.0",
    openapi_tags=tags_metadata,
    servers=[{"url": "http://127.0.0.1:8000", "description": "Local development server"}]
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
app.include_router(fc)
app.include_router(genai)
app.include_router(assgn)
app.include_router(coding_assignment)

# Mounting Static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Defining template directory
templates = Jinja2Templates(directory="templates")

# Favicon of the app
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

scheduler = AsyncIOScheduler()

from utils.grading import grade_assignment

@app.on_event("startup")
async def startup_event():
    print("App Started")
    scheduler.add_job(grade_assignment, IntervalTrigger(days=1))
    scheduler.start()
    return {"message": "Scheduler started!"}

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app="main:app", host='0.0.0.0', port=8000, reload=True)
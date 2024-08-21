from fastapi import FastAPI, BackgroundTasks, WebSocket
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes.user import user
from routes.course import course
from routes.notes import notes
from routes.course_material import course_material
from routes.coding_assignments import coding_assignment
from routes.flashcard import fc
from routes.summarize import summarizer
from routes.assignment import assgn
from routes.question_answer import question_answer
from routes.generate_assignment_questions import assignment_question_answer

from utils.security import auth
from utils.response import responses
from utils.extra import tags_metadata
from utils.grading import grade_assignment
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import asyncio
from asyncio import sleep
from ai.gemini import generate_chunks
from threading import Thread
from ai.format_query import format_query



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
app.include_router(fc)
app.include_router(question_answer)
app.include_router(assignment_question_answer)
app.include_router(summarizer)
app.include_router(assgn)
app.include_router(coding_assignment)
app.include_router(notes)

async def send_res(websocket: WebSocket, streamer):
    last_send = 0
    while True:
        await sleep(0.5)
        s = len(streamer.queue)
        if s>last_send:
            await websocket.send_text(streamer.queue[last_send: s])
        elif not streamer.has_next:
            print(streamer.queue)
            await websocket.close()
            break
        last_send = s

@app.websocket("/generate")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    request = await websocket.receive_json()
    if request.get('query') is None:
        websocket.close()
        return
    await generate_chunks(request.get('query'), websocket)
    await websocket.close()

@app.websocket("/search_generate")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    request = await websocket.receive_json()
    if request.get('query') is None or request.get('course_id') is None or request.get('week') is None:
        websocket.close()
        return
    
    query = format_query(request.get('query'), request.get('week'), request.get('course_id'))
    await generate_chunks(query, websocket)
    await websocket.close()

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

scheduler = AsyncIOScheduler()


@app.on_event("startup")
async def startup_event():
    print("App Started")
    scheduler.add_job(grade_assignment, IntervalTrigger(minutes=1))
    scheduler.start()
    return {"message": "Scheduler started!"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app="main:app", host='0.0.0.0', port=8000, reload=True)

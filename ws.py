from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from ai.gpt_2 import tok, model
from ai.streamer import TextStreamer
from asyncio import sleep
from threading import Thread
import uvicorn
app = FastAPI()
import asyncio

async def send_res(websocket: WebSocket, streamer):
    last_send = 0
    while True:
        await sleep(1)
        s = len(streamer.queue)
        if s>last_send:
            await websocket.send_text(streamer.queue[last_send: s])
        elif not streamer.has_next:
            return
        last_send = s


@app.websocket("/generate")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    request = await websocket.receive_json()
    if request.get('query') is None:
        await websocket.close()
        return
    inputs = tok([request['query']], return_tensors="pt")
    streamer = TextStreamer(tok, websocket)
    generation_kwargs = dict(**inputs, streamer=streamer, do_sample=True, temperature=0.1, repetition_penalty=1.1, max_new_tokens=200)
    thread = Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()
    # 
    await send_res(websocket, streamer)
    await websocket.close()

@app.websocket("/search_generate")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    request = await websocket.receive_json()
    if request.get('query') is None or request.get('course_id') is None or request.get('week') is None:
        await websocket.close()
        return
    
    inputs = tok([request['query']], return_tensors="pt")
    streamer = TextStreamer(tok, websocket)
    generation_kwargs = dict(**inputs, streamer=streamer, do_sample=True, temperature=0.1, repetition_penalty=1.1, max_new_tokens=200)
    thread = Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()
    thread_2 = Thread(target=send_res, kwargs={'websocket': websocket, 'streamer': streamer})
    thread_2.start()
    thread_2.join()
    
    
if __name__ == '__main__':
    uvicorn.run(app="ws:app", host='0.0.0.0', port=8000)
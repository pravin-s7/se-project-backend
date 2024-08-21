from fastapi import APIRouter, Body
from utils.response import responses
from ai.summary import TextSummarizer

summarizer = APIRouter(tags=["Summarize"])

@summarizer.post("/summarize", status_code=201,  responses=responses)
async def summarize_text(
    text: str = Body(..., embed=True)
):
    text_summarizer = TextSummarizer()
    summary = text_summarizer.invoke_chain(text)
    return summary
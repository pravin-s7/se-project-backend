from fastapi import APIRouter, Body
from utils.response import responses
from ai.question_answer import QuestionAnswerGenerator

question_answer = APIRouter(tags=["Question Answer Generator"])

# notes
@question_answer.post("/generate_questions", status_code=201,  responses=responses)
async def question_gen(
    text: str = Body(..., embed=True)
):
    question_answer_gen = QuestionAnswerGenerator()
    question = question_answer_gen.invoke_chain(text)
    return question
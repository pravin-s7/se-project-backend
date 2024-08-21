from fastapi import APIRouter, Body
from utils.response import responses
from ai.question_answer import SimilarQuestionAnswerGenerator

assignment_question_answer = APIRouter(tags=["Assignment Question Answer Generator"])

# question & answer

@assignment_question_answer.post("/generate_assignment_questions", status_code=201,  responses=responses)
async def question_gen(
    text: str = Body(..., embed=True)
):
    question_answer_gen = SimilarQuestionAnswerGenerator()
    question = question_answer_gen.invoke_chain(text)
    return question
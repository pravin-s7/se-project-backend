import json
from langchain.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import List

import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_AI_KEY')

class QuestionAnswerSchema(BaseModel):
    question: str = Field(description="Generated Question")
    option1: str = Field(description="Option 1")
    option2: str = Field(description="Option 2")
    option3: str = Field(description="Option 3")
    option4: str = Field(description="Option 4")
    correct_option: str = Field(description="Correct Option")

class QuestionsSchema(BaseModel):
    questions: List[QuestionAnswerSchema]

class QuestionAnswerGenerator():
    def __init__(self) -> None:
        self.parser = PydanticOutputParser(pydantic_object=QuestionsSchema)
        self.model = ChatGoogleGenerativeAI(model='gemini-1.5-flash', google_api_key=GOOGLE_API_KEY)
        self.template = """
    You are a MCQ generator. Generate 2 MCQ questions using the provided text.

    TEXT: {text}

    {format_instructions}
"""

    def get_chain(self):
        format_instructions = self.parser.get_format_instructions()

        prompt = PromptTemplate(
            template=self.template,
            input_variables=["text"],
            partial_variables={"format_instructions": format_instructions}
        )
        chain = prompt | self.model | self.parser
        return chain
    
    def invoke_chain(self, text):
        chain = self.get_chain()
        summary = chain.invoke({
            "text": f"{text}"
        })
        return json.loads(summary.json())


class SimilarQuestionAnswerGenerator():
    def __init__(self) -> None:
        self.parser = PydanticOutputParser(pydantic_object=QuestionsSchema)
        self.model = ChatGoogleGenerativeAI(model='gemini-1.5-flash', google_api_key=GOOGLE_API_KEY)
        self.template = """
    You are a MCQ generator
    Generate 3 multiple-choice questions based on the following text. 
    Ensure that the questions are of similar difficulty and style to the provided questions. 
    Give different questions and answers which are similar to the provided questions.
    Each question should have one correct answer and three distractors.

    TEXT: {text}

    {format_instructions}
"""

    def get_chain(self):
        format_instructions = self.parser.get_format_instructions()

        prompt = PromptTemplate(
            template=self.template,
            input_variables=["text"],
            partial_variables={"format_instructions": format_instructions}
        )
        chain = prompt | self.model | self.parser
        return chain
    
    def invoke_chain(self, text):
        chain = self.get_chain()
        summary = chain.invoke({
            "text": f"{text}"
        })
        return json.loads(summary.json())
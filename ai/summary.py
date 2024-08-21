import json
from langchain.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field

import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_AI_KEY')

class SummarySchema(BaseModel):
    summary: str = Field(description="Summary of the provided text")

class TextSummarizer():
    def __init__(self) -> None:
        self.parser = PydanticOutputParser(pydantic_object=SummarySchema)
        self.model = ChatGoogleGenerativeAI(model='gemini-1.5-flash', google_api_key=GOOGLE_API_KEY)
        self.template = """
    You are a text summarizer. Generate the summary of the text given below.

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

import google.generativeai as genai
import os
from dotenv import load_dotenv
from fastapi import WebSocket
from ai.format_query import format_query, format_query_flashcard

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_AI_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

'''
models/gemini-1.5-flash ['generateContent', 'countTokens']

for m in genai.list_models():  
  print(m.name, m.supported_generation_methods)
'''

model = genai.GenerativeModel('gemini-1.5-flash')

def generate(prompt):
  response = model.generate_content(prompt) 
  return response.text.replace("answer:", "")

async def generate_chunks(prompt, websocket: WebSocket):
  response = model.generate_content(prompt, stream= True)
  for chunk in response:
    await websocket.send_text(chunk.text)
  return response.text

def search_generate(course_id, week_lte, query):
  query = format_query(query, week_lte, course_id)
  return generate(query)

def search_generate_flashcard(course_id, week_lte, query):
  query = format_query_flashcard(query, week_lte, course_id)
  return generate(query)
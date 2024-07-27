import google.generativeai as genai
import os
from dotenv import load_dotenv

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
  return response.text
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_AI_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

'''
models/chat-bison-001 ['generateMessage', 'countMessageTokens']
models/text-bison-001 ['generateText', 'countTextTokens', 'createTunedTextModel']
models/embedding-gecko-001 ['embedText', 'countTextTokens']
models/gemini-1.0-pro ['generateContent', 'countTokens']
models/gemini-1.0-pro-001 ['generateContent', 'countTokens', 'createTunedModel']
models/gemini-1.0-pro-latest ['generateContent', 'countTokens']
models/gemini-1.0-pro-vision-latest ['generateContent', 'countTokens']
models/gemini-1.5-flash ['generateContent', 'countTokens']
models/gemini-1.5-flash-001 ['generateContent', 'countTokens', 'createCachedContent']
models/gemini-1.5-flash-latest ['generateContent', 'countTokens']
models/gemini-1.5-pro ['generateContent', 'countTokens']
models/gemini-1.5-pro-001 ['generateContent', 'countTokens', 'createCachedContent']
models/gemini-1.5-pro-latest ['generateContent', 'countTokens']
models/gemini-pro ['generateContent', 'countTokens']
models/gemini-pro-vision ['generateContent', 'countTokens']
models/embedding-001 ['embedContent']
models/text-embedding-004 ['embedContent']
models/aqa ['generateAnswer']

for m in genai.list_models():  
  print(m.name, m.supported_generation_methods)
'''

model = genai.GenerativeModel('gemini-1.5-flash')


def generate(prompt):
  response = model.generate_content(prompt) 
  return response.text

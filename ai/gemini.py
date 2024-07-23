import textwrap

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

model = genai.GenerativeModel('models/aqa')

prompt = '''n<|system|>
Answer the question based on your knowledge. Use the following context to help:
[Document(page_content='Definition 3.43 Active Clause Coverage (ACC): For each p ∈ P and eac major clause ci ∈ C p , choose minor clauses c j , j \\x08= i so that ci determines p.'), Document(page_content='Criterion 3.16 Correlated Active Clause Coverage (CACC): For each p ∈  and each major clause ci ∈ C p , choose minor clauses c j , j \\x08= i so that ci determine p. T R has two requirements for each ci : ci evaluates to true and ci evaluates to false.'), Document(page_content='Active clause coverage requires that each clause c in a predicate p evaluates t true and false and determines the value of p. The first version in Chapter 3, genera active clause coverage allows the values for other clauses in p to have differen values when c is true and c is false. It is simple to show that mutation subsume general active clause coverage; in fact, we already have.'), Document(page_content='In terms of criteria, we develop the notion of active clause coverage in a general way first with the definition below and then refine out the ambiguities in th definition to arrive at the resulting formal coverage criteria.')]
<|user|>
What is active clause coverage?
<|assistant|>
'''

content = '''
You are a summarizer, that summarize the documents, Summarize the following
So, most often classes and objects arise in the context of what are called abstract data types. 
So, we have data types as we know, in Python, we have lists, we have dictionaries. And when 
we have a data type, we have certain permitted operations on these. For a list, for example, 
you can append to it, or you can combine two lists using plus you can concatenate them, with 
a dictionary, you can create a new entry with the key, you can update it, and so on.
You can get X, extract all the keys of a dictionary, extract all the values and so on. Now, 
sometimes we need to create our own data type. And this data type will typically have two 
parts; it will have some information that is stored in it. But there may also be some discipline 
or some required way of controlling access to this information. 
So, a typical example that most people use for this is a stack. So, what is a stack? A stack is 
what you think in English, it is just a pile of things come one on top of the other. Now, if I 
have a stack of books, for example, in a table, what can I do? I can add one more to the top of 
the stack. So, this is what is called in stack terminal, you push, or I can take the top most 
book of the stack, and this is called a pop.
Now, I cannot take out this book, until I take out the box on top of it. Otherwise, things will 
fall down haphazardly. So, the idea of a stack is that I have a sequence of values. So, x1, x2 
up to say some xn, and when I push I add a value on the end, and when I pop, I can only take 
out the last value. Now I may represent this information as a list. 

'''

response = model.generate_content(content) 

print(response.text)

for chunk in response:
  print(chunk.text)
  print("_"*80)
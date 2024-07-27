from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers import pipeline, BitsAndBytesConfig
from langchain.chains import LLMChain
import torch

collection_name = "CourseMaterialRAG"

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory="../chroma_db", embedding_function=embeddings)
db._client.heartbeat()
def vectorSearch(course_id, week_lte, query):
    res = db.similarity_search(
        query=query,
        k=5,
        filter={"$and": [{"course_id": course_id}, {"week": {"$lte": week_lte}}]},
    )

    return res

model_name = 'HuggingFaceH4/zephyr-7b-beta'
bnb_config = BitsAndBytesConfig(
 load_in_4bit=True,
 bnb_4bit_use_double_quant=True,
 bnb_4bit_quant_type="nf4",
 bnb_4bit_compute_dtype=torch.bfloat16
)
model = AutoModelForCausalLM.from_pretrained(model_name, quantization_config=bnb_config)
tokenizer = AutoTokenizer.from_pretrained(model_name)

text_generation_pipeline = pipeline(
    model=model,
    tokenizer=tokenizer,
    task="text-generation",
    temperature=0.2,
    repetition_penalty=1.1,
    return_full_text=True,
    max_new_tokens=400,
)

llm = HuggingFacePipeline(pipeline=text_generation_pipeline)

def generate(prompt):
  res = llm.invoke(prompt)
  index = res.find('<|assistant|>')
  if index!= -1:
    return res[index+14:].strip()
  return res

def search_generate(course_id, week_lte, query):
    docs = vectorSearch(course_id, week_lte, query)
    print('Found Context')
    model_query = '''
<|system|>
Answer the question based on your knowledge. Please follow the following rules:
1. If you don't find something in context, don't try to make up an answer.
2. If you find the answer, write the answer in a concise way with five sentences maximum.
<|question|>
    
    '''
    model_query += query + '\n <|context|>\n'
    for doc in docs:
        model_query += doc.page_content + '\n'

    model_query += '\n <|assistant|> \n'

    print('Generating Response')
    res = generate(model_query) # local langchain OR gemini OR colab

    return res

def search_generate_flashcard(course_id, week_lte, query):
    docs = vectorSearch(course_id, week_lte, query)
    print('Found Context')
    model_query = '''
<|system|>
Generate Flashcard from the following use the context to help. Please follow the following rules:
1. If you don't find something in context, don't try to make up an answer.
2. If you find the answer, write the answer in a concise way with two sentences maximum.

<|query|>
    '''
    model_query += query + '\n <|context|>\n'
    for doc in docs:
        model_query += doc.page_content + '\n'

    model_query += '\n <|assistant|> \n'

    print('Generating Response')
    res = generate(model_query) # local langchain OR gemini OR colab

    return res





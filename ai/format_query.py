from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
collection_name = "CourseMaterialRAG"

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory="../chroma_db", embedding_function=embeddings)
def vectorSearch(course_id, week_lte, query):
    res = db.similarity_search(
        query=query,
        k=5,
        filter={"$and": [{"course_id": course_id}, {"week": {"$lte": week_lte}}]},
    )

    return res

def format_query(query, week, course_id):
    docs = vectorSearch(course_id, week, query)
    model_query = '''
<|system|>
Answer the question based on your knowledge. Please follow the following rules:
1. If you are not able to relate something in context with respect to query. Return Ask question related to course
2. If you relate something in the context, write the answer in a concise way. Format: Answer
<|question|>
    
    '''
    model_query += query + '\n <|context|>\n'
    for doc in docs:
        model_query += doc.page_content + '\n'

    model_query += '\n <|assistant|> \n'

    print(f'Found {len(docs)} context docs')
    return model_query


def format_query_flashcard(query, week, course_id):
    docs = vectorSearch(course_id, week, query)
    model_query = '''
<|system|>
Generate Flashcard from the following use the context to help. Please follow the following rules:
1. If you don't find something in context, don't try to make up an answer. Return Ask question related to course.
2. If you find the answer, write the answer in a concise way with two sentences maximum.
3. Only give the answer for Back of the flashcard, no other entities. Format: Answer
<|query|>
    '''
    model_query += query + '\n <|context|>\n'
    for doc in docs:
        model_query += doc.page_content + '\n'

    model_query += '\n <|assistant|> \n'

    print(f'Found {len(docs)} context docs')
    return model_query

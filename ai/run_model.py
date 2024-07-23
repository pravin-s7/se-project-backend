from chroma_vector import vectorSearch
from colab_request import generate

def search_generate(course_id, week_lte, query):
    docs = vectorSearch(course_id, week_lte, query)

    model_query = '''
<|system|>
Answer the question based on your knowledge. Use the following context to help:
Use the following pieces of context to answer the question at the end. Please follow the following rules:
1. If you don't find the answer in context, don't try to make up an answer. Just say "I can't find the answer".
2. If you find the answer, write the answer in a concise way with five sentences maximum.

<|question|>

    '''
    model_query += query + '\n <|context|>\n'
    for doc in docs:
        model_query += doc.page_content + '\n'

    model_query += '\n <|assistant|> \n'

    res = generate(model_query)
    
    return res


print(search_generate('CS01', 2, 'What is stack'))
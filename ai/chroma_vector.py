from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

collection_name = "CourseMaterialRAG"
# embeddings_model_name = 'BAAI/bge-base-en-v1.5'
# embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
db._client.heartbeat()


def insertIntoEmbeddings(course_id, week, content):
    metadata = {"course_id": course_id, "week": week}
    splitted = splitter(content)
    metadatas = [metadata for doc in splitted]
    db.add_texts(texts=splitted, metadatas=metadatas)


def splitter(content):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    return text_splitter.split_text(content)


def vectorSearch(course_id, week_lte, query):
    db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    res = db.similarity_search(
        query=query,
        k=5,
        filter={"$and": [{"course_id": course_id}, {"week": {"$lte": week_lte}}]},
    )

    return res


# splitter(content)
# insertIntoEmbeddings("CS02", 2, content=content)
# vectorSearch("CS01", 0, "What is stack")

from langchain_community.embeddings import LocalAIEmbeddings
from langchain_community.llms import Ollama
from slugify import slugify

EMBEDDING_MODEL = "text-embedding-ada-002"
LLM_MODEL = "mixtral:8x7b-instruct-v0.1-q5_K_M"


def get_embeddings():
    return LocalAIEmbeddings(
        openai_api_base="http://localhost:8080",
        model=EMBEDDING_MODEL,
    )


def get_collection_name(problem_name):
    collection_name = slugify(problem_name, separator="_")
    if collection_name[0].isdigit():
        collection_name = f"_{collection_name}"
    return collection_name


def get_llm():
    return Ollama(
        model=LLM_MODEL,
    )


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

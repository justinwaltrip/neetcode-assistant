from langchain_community.embeddings import LocalAIEmbeddings
from slugify import slugify


def get_embeddings():
    return LocalAIEmbeddings(
        openai_api_base="http://localhost:8080", model="text-embedding-ada-002"
    )


def get_collection_name(problem_name):
    collection_name = slugify(problem_name, separator="_")
    if collection_name[0].isdigit():
        collection_name = f"_{collection_name}"
    return collection_name

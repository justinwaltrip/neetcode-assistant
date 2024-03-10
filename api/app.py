import json
import os
import sys

from fastapi import FastAPI
from langchain_community.vectorstores import Milvus
from pydantic import BaseModel

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils import get_collection_name, get_embeddings

PROBLEMS_PATH = "data/processed/index.json"

with open(PROBLEMS_PATH, "r") as f:
    problems = json.load(f)

embeddings = get_embeddings()

app = FastAPI()


@app.get("/")
def get_root():
    """Return API status.

    Returns:
        dict: API status.
    """
    return {"status": "initialized"}


class RetrieveRequest(BaseModel):
    problem_name: str
    query: str


@app.post("/retrieve")
def post_retrieve(body: RetrieveRequest):
    """Retrieve relevant documents for a given query."""
    # get problem (if exists)
    try:
        problem = next(
            problem for problem in problems if problem["name"] == body.problem_name
        )
    except StopIteration:
        return {"error": "problem not found"}

    # check if problem is indexed
    if not problem.get("indexed", False):
        return {"error": "problem not indexed"}

    # connect to vector database
    vector_db = Milvus(
        embeddings,
        collection_name=get_collection_name(body.problem_name),
    )

    return vector_db.similarity_search(
        body.query,
    )

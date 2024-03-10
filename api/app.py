import json
import os
import sys
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_community.vectorstores import Milvus
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from utils import format_docs, get_collection_name, get_embeddings, get_llm

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


class ChatRequest(BaseModel):
    problem_name: str
    query: str
    streaming: Optional[bool] = False


@app.post("/chat")
async def post_chat(body: ChatRequest):
    """Chat with the bot."""
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

    template = """You are helping someone with a LeetCode problem.
    I will give you the problem description, some relevant sections of the solution transcript, and the problem solution.
    Use this information to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Keep your answer concise.
    Format your answer using markdown.

    Here is the problem description:
    <description>
    {description}
    </description> 

    Here are some relevant sections of the solution transcript (hidden from the user):
    <transcript>
    {context}
    </transcript>

    Here is the solution (hidden from the user):
    <solution>
    {solution}
    </solution>

    The user does have access to the problem description, but not the solution transcript or the solution.
    You can use the solution transcript and solution to help answer the user's question, but don't refer to them directly.
    Your goal is to help the user get to the solution, not to give them the solution directly.
    Give the user a helpful hint or a nudge in the right direction, but don't give them the answer directly.

    Question: {question}

    Helpful Answer:"""
    prompt = PromptTemplate.from_template(
        template,
        partial_variables={
            "description": problem["description"],
            "solution": problem["solution"],
        },
    )

    # initialize RAG chain
    rag_chain = (
        {
            "context": vector_db.as_retriever() | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | get_llm()
        | StrOutputParser()
    )

    if body.streaming:
        # create a response iterator
        def stream_response():
            for chunk in rag_chain.stream(body.query):
                yield chunk

        return StreamingResponse(stream_response(), media_type="text/plain")
    else:
        return rag_chain.invoke(body.query).strip()

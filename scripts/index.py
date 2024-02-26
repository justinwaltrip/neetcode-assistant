"""Index text for retrieval.

1. Split long transcript into smaller chunks.

    Since we don't have punctuation in the transcript, we can split by word with a fixed length and overlap.

2. Embed chunks for semantic search.
3. Load chunks into vector database.
"""
import json

from langchain.indexes import SQLRecordManager, index
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Milvus
from slugify import slugify
from tqdm import tqdm

PROBLEMS_PATH = "data/raw/problems.json"
TRANSCRIPTS_DIR = "data/processed/transcripts"
MODEL = "mixtral:8x7b-instruct-v0.1-q5_K_M"
INDEX_PATH = "data/processed/index.json"

with open(PROBLEMS_PATH, "r") as f:
    problems = json.load(f)

# create text splitter
text_splitter = CharacterTextSplitter(
    separator=" ",
    chunk_size=500,
    chunk_overlap=100,  # 20% overlap
    is_separator_regex=False,
)

# get embeddings from Ollama
embeddings = OllamaEmbeddings(model=MODEL)

for problem in tqdm(problems):
    try:
        video_link = problem["video_link"]
        id = video_link.split("=")[-1]
        transcript_path = f"{TRANSCRIPTS_DIR}/{id}.en.txt"
        transcript = open(transcript_path, "r").read()
        problem_name = problem["name"]

        # connect to vector database
        vector_db = Milvus(
            embeddings,
            collection_name=slugify(problem_name, separator="_"),
        )

        # initialize record manager
        record_manager = SQLRecordManager(
            namespace=f"milvus/{problem_name}",
            db_url="sqlite:///record_manager_cache.sql",
        )
        record_manager.create_schema()

        # split transcript into chunks
        metadata = {"source": problem_name}
        documents = text_splitter.create_documents(
            [transcript],
            metadatas=[metadata],
        )

        # index chunks
        index(
            docs_source=documents,
            record_manager=record_manager,
            vector_store=vector_db,
            cleanup="full",
            source_id_key="source",
        )
        problem["indexed"] = True

    except Exception as e:
        print(f"Error processing {problem['name']}: {e}")
        problem["indexed"] = False

# save problems with indexed flag
with open(INDEX_PATH, "w") as f:
    json.dump(problems, f, indent=4)

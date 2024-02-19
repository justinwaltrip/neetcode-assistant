"""Index text for retrieval.

1. Split long transcript into smaller chunks.

    Since we don't have punctuation in the transcript, we can split by word with a fixed length and overlap.

2. Embed chunks for semantic search.
3. Load chunks into vector database.
"""
import json
from tqdm import tqdm
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Milvus
from langchain_community.embeddings import OllamaEmbeddings
from langchain.indexes import SQLRecordManager, index

PROBLEMS_PATH = "data/raw/problems.json"
TRANSCRIPTS_DIR = "data/processed/transcripts"
MODEL = "mixtral:8x7b-instruct-v0.1-q5_K_M"
COLLECTION_NAME = "transcripts"

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

# connect to vector database
vector_db = Milvus(
    embeddings,
    collection_name=COLLECTION_NAME,
)

# initialize record manager
record_manager = SQLRecordManager(
    namespace=f"milvus/{COLLECTION_NAME}",
    db_url="sqlite:///record_manager_cache.sql",
)
record_manager.create_schema()

transcripts = []
metadatas = []

for problem in problems:
    try:
        video_link = problem["video_link"]
        id = video_link.split("=")[-1]
        transcript_path = f"{TRANSCRIPTS_DIR}/{id}.en.txt"
        transcripts.append(open(transcript_path, "r").read())
        metadatas.append({"source": problem["name"]})
    except Exception as e:
        print(f"Error processing {problem['name']}: {e}")

# split transcript into chunks
documents = text_splitter.create_documents(
    transcripts,
    metadatas=metadatas,
)

# get batches of 100 documents
batches = [documents[i : i + 100] for i in range(0, len(documents), 100)]

for batch in tqdm(batches):
    # index chunks
    index(
        docs_source=batch,
        record_manager=record_manager,
        vector_store=vector_db,
        cleanup="full",
        source_id_key="source",
    )

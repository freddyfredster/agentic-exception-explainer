import os
import glob
from typing import List, Dict

import chromadb
from chromadb.config import Settings
from openai import OpenAI

from .config import RAW_DATA_DIR, VECTORSTORE_DIR, OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def load_text_files() -> List[Dict]:
    """Load all .txt files from data/raw/notes and data/raw/emails."""
    docs = []
    for folder in ["notes", "emails"]:
        pattern = os.path.join(RAW_DATA_DIR, folder, "**", "*.txt")
        for path in glob.glob(pattern, recursive=True):
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            docs.append(
                {
                    "id": os.path.relpath(path, RAW_DATA_DIR),
                    "text": text,
                    "source_type": folder,
                }
            )
    return docs


def chunk_text(text: str, max_chars: int = 800) -> List[str]:
    """Very simple character-based chunking."""
    return [text[i : i + max_chars] for i in range(0, len(text), max_chars)]


def embed_texts(texts: List[str]):
    """Create embeddings for a list of texts."""
    resp = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts,
    )
    return [d.embedding for d in resp.data]


def build_doc_vectorstore():
    """Create/reset the Chroma collection and add all document chunks."""
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)

    chroma_client = chromadb.PersistentClient(
        path=VECTORSTORE_DIR,
        settings=Settings(allow_reset=True),
    )

    # Start clean each time for this demo
    try:
        chroma_client.delete_collection("docs")
    except Exception:
        pass

    collection = chroma_client.create_collection("docs")

    docs = load_text_files()
    ids, texts, metas = [], [], []

    for doc in docs:
        chunks = chunk_text(doc["text"])
        for idx, chunk in enumerate(chunks):
            ids.append(f"{doc['id']}::chunk-{idx}")
            texts.append(chunk)
            metas.append(
                {
                    "file_id": doc["id"],
                    "source_type": doc["source_type"],
                }
            )

    embeddings = embed_texts(texts)

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metas,
    )

    print(f"Ingested {len(texts)} chunks from {len(docs)} files into vector store.")


if __name__ == "__main__":
    build_doc_vectorstore()

from app.services.vector_store import VectorStore


if __name__ == "__main__":
    store = VectorStore()
    store.ingest("data/kb_docs")
    print("Knowledge base ingested")

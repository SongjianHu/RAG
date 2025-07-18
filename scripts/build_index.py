import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.retrieval.vector_retriever import build_faiss_index

if __name__ == "__main__":
    chunk_dir = "data/processed/chunks"
    index_out_path = "data/vector_stores/faiss_index/chunks.index"
    meta_out_path = "data/vector_stores/metadata/chunks_metadata.json"
    build_faiss_index(chunk_dir, index_out_path, meta_out_path) 
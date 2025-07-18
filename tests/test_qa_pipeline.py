import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.generation.qa_pipeline import rag_qa

def test_rag_qa():
    answer = rag_qa(
        question="3D编程模型创新设计专项赛的竞赛时间",
        index_path="data/vector_stores/faiss_index/chunks.index",
        meta_path="data/vector_stores/metadata/chunks_metadata.json",
        chunk_dir="data/processed/chunks",
        top_k=3
    )
    print("RAG答案：", answer)

if __name__ == "__main__":
    test_rag_qa() 
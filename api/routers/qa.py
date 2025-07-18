from fastapi import APIRouter
from pydantic import BaseModel
from src.generation.qa_pipeline import rag_qa

class QARequest(BaseModel):
    question: str
    top_k: int = 5
    rerank: bool = True
    use_llm_compress: bool = False

class QAResponse(BaseModel):
    answer: str

router = APIRouter()

@router.post("/answer", response_model=QAResponse)
def answer(req: QARequest):
    index_path = "data/vector_stores/faiss_index/chunks.index"
    meta_path = "data/vector_stores/metadata/chunks_metadata.json"
    chunk_dir = "data/processed/chunks"
    answer = rag_qa(
        question=req.question,
        index_path=index_path,
        meta_path=meta_path,
        chunk_dir=chunk_dir,
        top_k=req.top_k,
        rerank=req.rerank,
        use_llm_compress=req.use_llm_compress
    )
    return QAResponse(answer=answer) 
from sentence_transformers import CrossEncoder

def rerank(query, candidates, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2", top_k=5):
    """
    candidates: List[dict]，每个dict包含'text'和'metadata'字段
    返回重排序后的top_k结果
    """
    model = CrossEncoder(model_name)
    pairs = [(query, c["metadata"].get("text", "")) for c in candidates]
    scores = model.predict(pairs)
    for c, s in zip(candidates, scores):
        c["rerank_score"] = float(s)
    results = sorted(candidates, key=lambda x: x["rerank_score"], reverse=True)[:top_k]
    return results 
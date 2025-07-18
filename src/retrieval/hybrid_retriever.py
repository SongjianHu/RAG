from src.retrieval.vector_retriever import search_faiss
from src.retrieval.keyword_retriever import keyword_retrieve
from src.retrieval.reranker import rerank

def hybrid_retrieve(query, index_path, meta_path, chunk_dir, model_name="moka-ai/m3e-base", top_k=5, alpha=0.7, rerank_enable=False, rerank_model="cross-encoder/ms-marco-MiniLM-L-6-v2"):
    """
    混合检索：向量检索和关键词检索加权融合，alpha为向量检索权重
    rerank_enable: 是否启用重排序
    """
    vec_results = search_faiss(query, index_path, meta_path, model_name, top_k=top_k*2)
    kw_results = keyword_retrieve(query, chunk_dir, top_k=top_k*2)
    # 合并去重
    merged = {}
    for r in vec_results:
        key = str(r["metadata"])
        merged[key] = {"score": r["score"] * alpha, "metadata": r["metadata"]}
    for r in kw_results:
        key = str(r["metadata"])
        if key in merged:
            merged[key]["score"] += r["score"] * (1 - alpha)
        else:
            merged[key] = {"score": r["score"] * (1 - alpha), "metadata": r["metadata"]}
    # 按融合分数排序
    results = sorted(merged.values(), key=lambda x: x["score"], reverse=True)[:top_k*2]
    # 可选重排序
    if rerank_enable:
        # 需要将chunk文本补充到metadata中
        for r in results:
            if "text" not in r["metadata"]:
                r["metadata"]["text"] = r["metadata"].get("text", "")
        results = rerank(query, results, model_name=rerank_model, top_k=top_k)
    else:
        results = results[:top_k]
    return results 
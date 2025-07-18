import os
import json
from pathlib import Path
from tqdm import tqdm
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

def load_chunks(chunk_dir):
    chunks = []
    metadatas = []
    for chunk_file in Path(chunk_dir).glob("*.json"):
        with open(chunk_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            chunks.append(data["text"])
            metadatas.append(data["metadata"])
    return chunks, metadatas

def build_faiss_index(chunk_dir, index_out_path, meta_out_path, model_name="moka-ai/m3e-base", batch_size=64):
    model = SentenceTransformer(model_name)
    chunks, metadatas = load_chunks(chunk_dir)
    embeddings = []
    for i in tqdm(range(0, len(chunks), batch_size), desc="Embedding chunks"):
        batch = chunks[i:i+batch_size]
        emb = model.encode(batch, show_progress_bar=False, normalize_embeddings=True)
        embeddings.append(emb)
    embeddings = np.vstack(embeddings)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    faiss.write_index(index, index_out_path)
    # 保存元数据
    with open(meta_out_path, "w", encoding="utf-8") as f:
        json.dump(metadatas, f, ensure_ascii=False, indent=2)
    print(f"Faiss索引已保存到: {index_out_path}")
    print(f"元数据已保存到: {meta_out_path}")

def load_faiss_index(index_path):
    return faiss.read_index(index_path)

def load_metadata(meta_path):
    with open(meta_path, "r", encoding="utf-8") as f:
        return json.load(f)

def search_faiss(query, index_path, meta_path, model_name="moka-ai/m3e-base", top_k=5):
    """
    输入query，返回top_k个最相似chunk及其元数据
    """
    model = SentenceTransformer(model_name)
    index = load_faiss_index(index_path)
    metadatas = load_metadata(meta_path)
    query_emb = model.encode([query], normalize_embeddings=True)
    query_emb = np.array(query_emb).astype('float32')
    if query_emb.ndim == 1:
        query_emb = query_emb.reshape(1, -1)
    D, I = index.search(query_emb, top_k)
    results = []
    for idx, score in zip(I[0], D[0]):
        if idx < len(metadatas):
            results.append({
                "score": float(score),
                "metadata": metadatas[idx]
            })
    return results 
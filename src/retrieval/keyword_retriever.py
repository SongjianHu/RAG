import os
import json
from pathlib import Path
from collections import defaultdict
from tqdm import tqdm

def load_chunks(chunk_dir):
    chunks = []
    metadatas = []
    for chunk_file in Path(chunk_dir).glob("*.json"):
        with open(chunk_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            chunks.append(data["text"])
            metadatas.append(data["metadata"])
    return chunks, metadatas

def keyword_retrieve(query, chunk_dir, top_k=5):
    """
    简单基于关键词的召回，按命中关键词数排序
    """
    chunks, metadatas = load_chunks(chunk_dir)
    query_keywords = set(query.split())
    scored = []
    for i, chunk in enumerate(chunks):
        score = sum(1 for kw in query_keywords if kw in chunk)
        if score > 0:
            scored.append((score, i))
    scored.sort(reverse=True)
    results = []
    for score, idx in scored[:top_k]:
        results.append({
            "score": float(score),
            "metadata": metadatas[idx]
        })
    return results 
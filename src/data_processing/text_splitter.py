import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
import json

def split_text_file(text_path, out_dir, chunk_size=500, chunk_overlap=50):
    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read()
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_text(text)
    meta = {"source": str(text_path)}
    os.makedirs(out_dir, exist_ok=True)
    for i, chunk in enumerate(chunks):
        chunk_file = Path(out_dir) / f"{Path(text_path).stem}_chunk_{i}.json"
        with open(chunk_file, "w", encoding="utf-8") as f:
            json.dump({"text": chunk, "metadata": meta}, f, ensure_ascii=False, indent=2)

def batch_split_texts(text_dir, out_dir):
    for text_file in Path(text_dir).glob("*.txt"):
        split_text_file(text_file, out_dir) 
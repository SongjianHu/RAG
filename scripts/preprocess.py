import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.data_processing.pdf_processor import batch_pdf_to_text
from src.data_processing.text_splitter import batch_split_texts
from src.data_processing.structured_extractor import batch_extract_structured

if __name__ == "__main__":
    # 1. PDF转文本
    pdf_dirs = [
        "data/raw/manuals",
        "data/raw/changes_and_addition",
        "data/raw/test"
    ]
    text_out_dir = "data/processed/texts"
    for pdf_dir in pdf_dirs:
        batch_pdf_to_text(pdf_dir, text_out_dir)

    # 2. 文本分割
    chunk_out_dir = "data/processed/chunks"
    batch_split_texts(text_out_dir, chunk_out_dir)

    # 3. 结构化信息抽取
    structured_out_dir = "data/processed/structured"
    batch_extract_structured(text_out_dir, structured_out_dir)
    print("数据预处理与结构化信息抽取完成！") 
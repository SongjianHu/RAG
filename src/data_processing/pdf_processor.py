import os
from pathlib import Path
from PyPDF2 import PdfReader

def pdf_to_text(pdf_path, out_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)

def batch_pdf_to_text(pdf_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for pdf_file in Path(pdf_dir).glob("*.pdf"):
        out_file = Path(out_dir) / (pdf_file.stem + ".txt")
        pdf_to_text(pdf_file, out_file) 
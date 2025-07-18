import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import gradio as gr
from src.generation.qa_pipeline import rag_qa

print("Gradio脚本启动")
def qa_fn(question):
    print("收到问题：", question)
    answer = rag_qa(
        question=question,
        index_path="data/vector_stores/faiss_index/chunks.index",
        meta_path="data/vector_stores/metadata/chunks_metadata.json",
        chunk_dir="data/processed/chunks",
        top_k=5,
        rerank=True,
        use_llm_compress=False
    )
    return answer

def qa_fn(question):
    import os
    print("Gradio收到问题：", question)
    print("Gradio进程环境变量DEEPSEEK_API_KEY:", os.getenv("DEEPSEEK_API_KEY"))
    answer = rag_qa(
        question=question,
        index_path="data/vector_stores/faiss_index/chunks.index",
        meta_path="data/vector_stores/metadata/chunks_metadata.json",
        chunk_dir="data/processed/chunks",
        top_k=5,
        rerank=True,
        use_llm_compress=False
    )
    print("Gradio返回答案：", answer)
    return answer

iface = gr.Interface(
    fn=qa_fn,
    inputs=gr.Textbox(lines=2, label="请输入你的竞赛问题"),
    outputs=gr.Textbox(lines=8, label="答案"),
    title="RAG竞赛问答机器人",
    description="输入你的竞赛相关问题，机器人将基于手册内容为你解答。"
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)
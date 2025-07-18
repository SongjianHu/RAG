import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.retrieval.hybrid_retriever import hybrid_retrieve
from src.retrieval.compressor import simple_concat, llm_summarize
from src.generation.prompt_templates import build_qa_prompt
from src.generation.llm_client import DeepSeekLLMClient


def rag_qa(
    question: str,
    index_path: str,
    meta_path: str,
    chunk_dir: str,
    llm_api_key: str = none,#replace to your own deepseek api key
    top_k: int = 5,
    alpha: float = 0.7,
    rerank: bool = True,
    use_llm_compress: bool = False,
    max_tokens: int = 512
) -> str:
    """
    RAG主流程：混合检索->压缩/摘要->Prompt->LLM生成答案
    """
    # 1. 检索
    results = hybrid_retrieve(
        question, index_path, meta_path, chunk_dir,
        top_k=top_k, alpha=alpha, rerank_enable=rerank
    )
    # 2. 内容压缩/摘要
    if use_llm_compress:
        llm_client = DeepSeekLLMClient(api_key=llm_api_key)
        context = llm_summarize(results, question, llm_client, max_tokens=1024)
    else:
        context = simple_concat(results, max_tokens=1500)
    # 3. 构建Prompt
    prompt = build_qa_prompt(question, context)
    # 4. LLM生成答案
    llm_client = DeepSeekLLMClient(api_key=llm_api_key)
    answer = llm_client.generate(prompt, max_tokens=max_tokens)
    return answer 

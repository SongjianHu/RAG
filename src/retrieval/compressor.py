from typing import List, Dict, Literal

# 简单拼接压缩

def simple_concat(chunks: List[Dict], max_tokens: int = 1500) -> str:
    """
    将检索到的chunk文本简单拼接，截断到max_tokens长度
    """
    texts = [c["metadata"].get("text", "") for c in chunks]
    concat = "\n".join(texts)
    # 简单按字符数截断（可按token数优化）
    return concat[:max_tokens * 2]

# LLM摘要压缩（需外部LLM客户端支持）
def llm_summarize(chunks: List[Dict], question: str, llm_client, max_tokens: int = 512) -> str:
    """
    用LLM对检索到的chunks做摘要压缩
    llm_client需有generate(prompt, max_tokens)方法
    """
    context = simple_concat(chunks, max_tokens=2000)
    prompt = f"请根据以下内容，简明整理出与问题相关的关键信息：\n问题：{question}\n内容：{context}\n摘要："
    summary = llm_client.generate(prompt, max_tokens=max_tokens)
    return summary 
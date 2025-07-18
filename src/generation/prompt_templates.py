def build_qa_prompt(question: str, context: str) -> str:
    """
    构建RAG问答Prompt，适配竞赛手册场景
    """
    prompt = f"""
你是一名竞赛助手，请根据给定的竞赛手册内容，准确、简明地回答用户问题。

【竞赛手册内容】
{context}

【用户问题】
{question}

【要求】
- 只基于手册内容作答，不要编造。
- 如内容不足，请回复“手册中未找到相关信息”。
- 答案尽量结构化、条理清晰。

【答案】
"""
    return prompt 
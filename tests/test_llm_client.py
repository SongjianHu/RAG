import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.generation.llm_client import DeepSeekLLMClient

def test_deepseek_llm():
    # 推荐用环境变量传递API Key
    api_key = "sk-7c68bde882bb4c0096149cf85e9b92a4"
    if not api_key:
        print("请先设置DEEPSEEK_API_KEY环境变量！")
        return
    llm = DeepSeekLLMClient(api_key=api_key)
    prompt = "你好，介绍一下你自己。"
    response = llm.generate(prompt, max_tokens=64)
    print("模型响应：", response)

if __name__ == "__main__":
    test_deepseek_llm() 
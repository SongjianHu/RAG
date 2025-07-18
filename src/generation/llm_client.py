import os
from openai import OpenAI

class DeepSeekLLMClient:
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.base_url = base_url or "https://api.deepseek.com"
        print("DeepSeekLLMClient实际用的Key:", self.api_key)
        print("base_url:", self.base_url)
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.2, model: str = "deepseek-chat") -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "你是一名竞赛助手，请根据检索内容准确回答用户问题。"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            stream=False
        )
        return response.choices[0].message.content or ""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.gradio_app import qa_fn

def test_gradio_qa_fn():
    question = "你知道‘未来校园’智能应用专项赛的开赛时间么"
    answer = qa_fn(question)
    print(f"问题: {question}\n答案: {answer}")

if __name__ == "__main__":
    test_gradio_qa_fn() 
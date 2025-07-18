import os
import re
import json
from pathlib import Path

def extract_structured_info(text):
    info = {}
    # 抽取时间（示例：2024年6月1日-6月3日 或 2024年6月1日）
    time_match = re.search(r"(20\d{2}年[\d月日\-至到\s]+)", text)
    if time_match:
        info["time"] = time_match.group(1).strip()
    # 抽取主办方
    org_match = re.search(r"(主办单位|主办方)[：: ]*(.*?)(。|\n)", text)
    if org_match:
        info["organizer"] = org_match.group(2).strip()
    # 抽取竞赛名称
    name_match = re.search(r"([“\"]?)([\u4e00-\u9fa5A-Za-z0-9（）\(\)]+?专项赛|竞赛通知|挑战赛|杯)[”\"]?", text)
    if name_match:
        info["competition_name"] = name_match.group(0).strip()
    # 可继续添加更多字段
    return info

def batch_extract_structured(text_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for text_file in Path(text_dir).glob("*.txt"):
        with open(text_file, "r", encoding="utf-8") as f:
            text = f.read()
        info = extract_structured_info(text)
        out_file = Path(out_dir) / (text_file.stem + ".json")
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(info, f, ensure_ascii=False, indent=2) 
import os
import re


def get_addition_data(title: str, index: int) -> list:
    path = f"data/{title}/{index}"
    files = []

    if os.path.exists(path):
        for root, _, filenames in os.walk(path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                files.append(file_path)
    return files


def clear_answer(line: str) -> str:
    answer = "".join(re.findall(r"\b\w+\b", line)).lower()
    return answer

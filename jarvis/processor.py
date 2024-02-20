import json
import os
from functools import partial
from .prompts import ExtractInsights

base_dir = partial(os.path.join, os.path.dirname(__file__), "..", "data")
raw_dir = partial(base_dir, "raw")
processed_dir = partial(base_dir, "processed")


def append_to_file(name, data, title, url, author):
    path = processed_dir(name)
    data = [{"content": row, "title": title, "url": url, "author": author}
            for row in data]
    if os.path.exists(path):
        with open(path, "r") as f:
            old_data = json.load(f)
            data = old_data + data

    with open(path, "w") as f:
        json.dump(data, f, indent=4, sort_keys=True, default=str)


def process_file(file_path):
    with open(file_path, "r") as f:
        data = f.read()
    out = ""
    for chunk in ExtractInsights(article=data):
        out += chunk
        print(chunk, end="")

    data = json.loads(out)

    append_to_file("macro.json", data["macro"],
                   data["title"], data["url"], data["author"])
    for code, obj in data["stocks"].items():
        positives = data["stocks"][code]["positives"]
        append_to_file(f"{code}-positives.json", positives,
                       data["title"], data["url"], data["author"])
        negatives = data["stocks"][code]["negatives"]
        append_to_file(f"{code}-negatives.json", negatives,
                       data["title"], data["url"], data["author"])

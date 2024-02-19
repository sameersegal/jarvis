import json
import os
from functools import partial
from .prompts import ExtractInsights

base_dir = partial(os.path.join, os.path.dirname(__file__), "..", "data")
raw_dir = partial(base_dir, "raw")
processed_dir = partial(base_dir, "processed")


def append_to_file(name, data):
    path = processed_dir(name)
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

    append_to_file("macro.json", data["macro"])
    for code, obj in data["stocks"].items():
        positives = data["stocks"][code]["positives"]
        append_to_file(f"{code}-positives.json", positives)
        negatives = data["stocks"][code]["negatives"]
        append_to_file(f"{code}-negatives.json", negatives)

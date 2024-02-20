import json
from functools import partial
import os
from .llm import completion
from .prompts import QnAPrompt

processed_dir = partial(os.path.join, os.path.dirname(
    __file__), "..", "data", "processed")


def answer(question, history = []):
    with open(processed_dir("macro.json"), "r") as f:
        macro = json.loads(f.read())

    with open(processed_dir("NVDA-positives.json"), "r") as f:
        positives = json.loads(f.read())

    with open(processed_dir("NVDA-negatives.json"), "r") as f:
        negatives = json.loads(f.read())

    for chunk in QnAPrompt(macro=macro, positives=positives, negatives=negatives, question=question, history=history):
        yield chunk

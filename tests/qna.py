import json
import os
from unittest import TestCase
from dotenv import load_dotenv
from jarvis.prompts import QnAPrompt
from functools import partial
load_dotenv()

processed_dir = partial(os.path.join, os.path.dirname(
    __file__), "..", "data", "processed")


class TestQnA(TestCase):

    def test_basic(self):

        with open(processed_dir("macro.json"), "r") as f:
            macro = json.loads(f.read())

        with open(processed_dir("NVDA-positives.json"), "r") as f:
            positives = json.loads(f.read())

        with open(processed_dir("NVDA-negatives.json"), "r") as f:
            negatives = json.loads(f.read())

        question = "What is the sentiment of NVDA?"

        for chunk in QnAPrompt(macro=macro, positives=positives, negatives=negatives, question=question):
            print(chunk, end="")

from unittest import TestCase
from jarvis.prompts import ExtractInsights
import os
from functools import partial
from dotenv import load_dotenv
load_dotenv()

base_dir = partial(os.path.join, os.path.dirname(__file__), "..", "data")
raw_dir = partial(base_dir, "raw")
processed_dir = partial(base_dir, "processed")


class TestExtractInsights(TestCase):

    def test_basic(self):

        with open(raw_dir("fool-nvda.md"), "r") as f:
            data = f.read()

        for chunk in ExtractInsights(article=data):
            print(chunk, end="")

    def test_basic2(self):

        with open(raw_dir("bi-nvda.md"), "r") as f:
            data = f.read()

        for chunk in ExtractInsights(article=data):
            print(chunk, end="")

    def test_basic3(self):
            
        with open(raw_dir("io-nvda.md"), "r") as f:
            data = f.read()

        for chunk in ExtractInsights(article=data):
            print(chunk, end="")
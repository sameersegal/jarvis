from functools import partial
import os
from unittest import TestCase
from dotenv import load_dotenv
from jarvis.processor import process_file

load_dotenv()

raw_dir = partial(os.path.join, os.path.dirname(__file__), "..", "data", "raw")


class TestProcessorCheck(TestCase):

    def test_files(self):
        process_file(raw_dir("fool-nvda.md"))
        process_file(raw_dir("bi-nvda.md"))
        process_file(raw_dir("io-nvda.md"))

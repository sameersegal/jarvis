import json
from functools import partial
import os
from .llm import completion
import gradio as gr
from .prompts import QnAPrompt
from dotenv import load_dotenv
load_dotenv()

processed_dir = partial(os.path.join, os.path.dirname(
    __file__), "..", "data", "processed")


def add_user_message(history, text):
    history += [(text, None)]
    return history, gr.Text(interactive=False)


def add_chatbot_message(history):
    question = history[-1][0]
    history[-1][1] = ""

    with open(processed_dir("macro.json"), "r") as f:
        macro = json.loads(f.read())

    with open(processed_dir("NVDA-positives.json"), "r") as f:
        positives = json.loads(f.read())

    with open(processed_dir("NVDA-negatives.json"), "r") as f:
        negatives = json.loads(f.read())

    for chunk in QnAPrompt(macro=macro, positives=positives, negatives=negatives, question=question):
        history[-1][1] += chunk
        yield history


with gr.Blocks() as demo:

    with gr.Row():
        chatbot = gr.Chatbot(height=600)

    with gr.Row():
        text = gr.Textbox(lines=2, 
                          placeholder="Ask me anything!", 
                          scale=9
                          show_label=False,
                          container=False)
        submit = gr.Button("Submit", variant="primary")

    text.submit(add_user_message, [chatbot, text], [chatbot, text], queue=False).then(
        add_chatbot_message, chatbot, chatbot)
    text.then(lambda: gr.Textbox(interactive=True),
                 None, [text], queue=False)

    demo.queue()
    demo.launch()

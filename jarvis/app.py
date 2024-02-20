import gradio as gr
from dotenv import load_dotenv
from .brain import answer
load_dotenv()


def add_user_message(history, text):
    history += [(text, None)]
    return history, gr.Text(interactive=False)


def add_chatbot_message(history):
    question = history[-1][0]
    history[-1][1] = ""

    for chunk in answer(question, history[:-1]):
        history[-1][1] += chunk
        yield history


with gr.Blocks() as demo:

    with gr.Row():
        chatbot = gr.Chatbot(height=600)

    with gr.Row():
        text = gr.Textbox(lines=2,
                          placeholder="Ask me anything",
                          scale=9,
                          show_label=False,
                          container=False)
        submit = gr.Button("Submit", variant="primary")

    with gr.Row():
        checkbox = gr.Checkbox(label="Debug Mode")

    text_fn = text.submit(add_user_message, [chatbot, text], [chatbot, text], queue=False).then(
        add_chatbot_message, chatbot, chatbot)
    text_fn.then(lambda: gr.Textbox(interactive=True),
                 None, [text], queue=False)

    submit_fn = submit.click(add_user_message, [chatbot, text], [chatbot, text], queue=False).then(
        add_chatbot_message, chatbot, chatbot)
    submit_fn.then(lambda: gr.Textbox(interactive=True),
                   None, [text], queue=False)

    demo.queue()
    demo.launch()

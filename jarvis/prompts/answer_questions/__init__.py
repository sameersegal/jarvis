from ..base import BasePrompt


class QA(BasePrompt):
    def __init__(self):
        super().__init__("answer_questions")

    def __call__(self, **kwargs):
        kwargs["macro"] = "\n".join(
            [f"- {x}" for x in kwargs["macro"]])
        kwargs["positives"] = "\n".join(
            [f"- {x}" for x in kwargs["positives"]])
        kwargs["negatives"] = "\n".join(
            [f"- {x}" for x in kwargs["negatives"]])
        for chunk in super().__call__(**kwargs):
            yield chunk


QnAPrompt = QA()

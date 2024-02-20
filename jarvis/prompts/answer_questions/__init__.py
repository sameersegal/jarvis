from ..base import BasePrompt, um, am


class QA(BasePrompt):

    valid_keywords = ["macro", "positives", "negatives", "question", "history"]

    def __init__(self):
        super().__init__("answer_questions")

    def __call__(self, **kwargs):

        if not all([x in self.valid_keywords for x, _ in kwargs.items()]):
            raise ValueError(
                f"Invalid keyword(s) passed to QnAPrompt. Valid keywords are: {', '.join(self.valid_keywords)}")

        kwargs["macro"] = "\n".join(
            [f"- {x['content']}\n\t- Author: {x['author']}\n\t- Url: {x['url']}" for x in kwargs["macro"]])
        kwargs["positives"] = "\n".join(
            [f"- {x['content']}\n\t- Author: {x['author']}\n\t- Url: {x['url']}" for x in kwargs["positives"]])
        kwargs["negatives"] = "\n".join(
            [f"- {x['content']}\n\t- Author: {x['author']}\n\t- Url: {x['url']}" for x in kwargs["negatives"]])

        messages = self.create_prompt(**kwargs)
        history = []
        for row in history:
            history.append(um(row[0]))
            history.append(am(row[1]))

        print(messages)
        print(history)

        kwargs['messages'] = [messages[0]] + history + [messages[1]]

        for chunk in super().__call__(**kwargs):
            yield chunk


QnAPrompt = QA()

from ..base import BasePrompt


class XI(BasePrompt):

    def __init__(self):
        super().__init__("extract_insights")

    def __call__(self, **kwargs):
        kwargs['response_format'] = {'type': 'json_object'}
        for chunk in super().__call__(**kwargs):
            yield chunk


ExtractInsights = XI()

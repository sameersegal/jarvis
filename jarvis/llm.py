import openai
import os


def completion(**kwargs):
    client = openai.Client(
        api_key=os.getenv('OPENAI_API_KEY')
    )

    kwargs['debug'] = kwargs.get('debug', os.getenv('DEBUG', False))
    kwargs['model'] = kwargs.get('model', "gpt-4-turbo-preview")
    kwargs['stream'] = True

    if kwargs.get('system_prompt') and kwargs.get('user_prompt'):
        kwargs['messages'] = [
            {
                "role": "system",
                "content": kwargs.get('system_prompt')
            },
            {
                "role": "user",
                "content": kwargs.get('user_prompt')
            }
        ]
    elif not kwargs.get('messages'):
        raise ValueError("messages is required")

    args = {k: v for k, v in kwargs.items() if k in [
        'model', 'messages', 'stream', 'response_format']}

    if kwargs.get('debug'):
        print("*"*10)
        print(args['messages'][0]['content'])
        print("**")
        print(args['messages'][1]['content'])
        print("*"*10)

    completions = client.chat.completions.create(
        **args
    )

    for chunk in completions:
        for choice in chunk.choices:
            if choice.finish_reason == 'stop':
                break
            if choice.delta.content is not None:
                yield choice.delta.content

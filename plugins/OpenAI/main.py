import openai
from openai.types.completion import Completion

from engine.plugins import register, events
from engine.structs import ArgNamespace, Plugin


@register
class OpenAIPlugin(Plugin):
    name = "OpenAI"
    description = "OpenAI API"
    author = ["FallingShrimp"]


@events.whenRequest("gpt4")
@events.whenRequest("openai")
@events.whenRequest("gpt")
def request(prompt: str, apikey: str, _: ArgNamespace, content: str) -> str:
    ai = openai.OpenAI(api_key=apikey)
    response = ai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": content,
            },
        ],
        response_format={
            "type": "json_object",
        },
    )
    if isinstance(response, Completion):
        responsed = response.choices[0].message.content
        if responsed:
            return responsed
        else:
            raise ValueError("Empty response.")
    else:
        raise ValueError("Unexpected response type or empty choices.")

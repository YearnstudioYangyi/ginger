import openai
from openai.types.completion import Completion

from engine.plugins import plugin, events
from engine.structs import ArgNamespace, Plugin


@plugin
class OpenAIPlugin(Plugin):
    name = "OpenAI"
    description = "OpenAI API"
    author = ["FallingShrimp"]

    @events.whenRequest("gpt4")
    @events.whenRequest("openai")
    @events.whenRequest("gpt")
    def request(self, prompt: str, apikey: str, namespace: ArgNamespace) -> str:
        ai = openai.OpenAI(api_key=apikey)
        response = ai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt},
                {
                    "role": "user",
                    "content": open(namespace.file, encoding="utf8").read(),
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

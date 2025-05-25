import zhipuai
from zhipuai.api_resource.chat.completions import Completion

from engine.plugins import plugin, events
from engine.structs import ArgNamespace, Plugin


@plugin
class ChatGLMPlugin(Plugin):
    name = "ChatGLM"
    description = "Zhipu API"
    author = ["FallingShrimp"]

    @events.whenRequest("glm")
    @events.whenRequest("zhipu")
    @events.whenRequest("chatglm")
    def request(self, prompt: str, apikey: str, namespace: ArgNamespace) -> str:
        ai = zhipuai.ZhipuAI(api_key=apikey)
        response = ai.chat.completions.create(
            model="glm-4-flash-250414",
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

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
    @staticmethod
    def request(prompt: str, apikey: str, _: ArgNamespace, content: str) -> str:
        ai = zhipuai.ZhipuAI(api_key=apikey)
        response = ai.chat.completions.create(
            model="glm-4-flash-250414",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": content},
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

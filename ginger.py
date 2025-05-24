import zhipuai, re, json, structs, os
from zhipuai.api_resource.chat.completions import Completion
from argparse import ArgumentParser


def parseResult(hasCodeBlock: str):
    pattern = re.compile(r"```(\w*)\n(.*?)\n```", re.DOTALL)
    matches = pattern.search(hasCodeBlock)
    if matches:
        return matches.group(2).strip()
    else:
        return hasCodeBlock


def getOutput(aiResponse: str) -> str:
    return json.loads(parseResult(aiResponse))["output"]


def getExtension(aiResponse: str) -> str:
    return json.loads(parseResult(aiResponse))["extension"]


def getStatus(aiResponse: str) -> bool:
    return json.loads(parseResult(aiResponse))["status"]


def getDependencies(aiResponse: str) -> list[str]:
    return json.loads(parseResult(aiResponse))["dependencies"]


def getData(output: str):
    return "\n".join(output)


def format(data: str, extension: str = ""):
    return (
        data.replace("$language", namespace.language)
        .replace("$traceback", namespace.traceback)
        .replace("$indent", str(namespace.indent))
        .replace("$filename", os.path.basename(namespace.file))
        .replace("$basename", os.path.splitext(os.path.basename(namespace.file))[0])
        .replace("$extension", extension)
    )


args = ArgumentParser()
args.add_argument("-f", "--file", required=True)
args.add_argument("-k", "--key", required=True)
args.add_argument("-l", "--language", default="Python")
args.add_argument("-t", "--traceback", default="en-US")
args.add_argument("-i", "--indent", default=4, type=int)
args.add_argument("-p", "--show-prompt", action="store_true")
args.add_argument("-o", "--output", default="$basename$extension")
namespace = structs.ArgNamespace(**vars(args.parse_args()))
prompt = format(open("prompt.txt", encoding="utf8").read())
if namespace.show_prompt:
    print(prompt)
ai = zhipuai.ZhipuAI(api_key=namespace.key)
response = ai.chat.completions.create(
    model="glm-4-flash-250414",
    messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": open(namespace.file, encoding="utf8").read()},
    ],
    response_format={
        "type": "json_object",
    },
)
if isinstance(response, Completion):
    response_content = response.choices[0].message.content
    if response_content:
        output = getOutput(response_content)
        print("Status:", getStatus(response_content))
        if getStatus(response_content):
            print(
                "Dependencies:\n -",
                "\n - ".join(getDependencies(response_content)),
            )
            open(
                format(namespace.output, getExtension(response_content)),
                "w",
                encoding="utf8",
            ).write(getData(output))
        else:
            print(getData(output))
else:
    raise ValueError("Unexpected response type or empty choices.")

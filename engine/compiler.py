import os, zhipuai
from zhipuai.api_resource.chat.completions import Completion

from .structs import *
from .tools import *
from .watcher import *
from .progressbar import *

defaultConfig = {"includes": [], "common": {}}
defaultInclude = {
    "input": "input.gg",
    "language": "Python",
    "output": "$basename$extension",
    "traceback": "en-US",
    "indent": 4,
    "show_prompt": False,
    "watch": False,
}
promptTemplate = open("prompt.txt", encoding="utf8").read()
key: str | None = None


def setKey(new: str):
    global key
    key = new


def format(data: str, namespace: ArgNamespace, extension: str = ""):
    return (
        data.replace("$language", namespace.language)
        .replace("$traceback", namespace.traceback)
        .replace("$indent", str(namespace.indent))
        .replace("$filename", os.path.basename(namespace.file))
        .replace("$basename", os.path.splitext(os.path.basename(namespace.file))[0])
        .replace("$extension", extension)
    )


def run(namespace: ArgNamespace, showState: bool = True):
    # print(f"Compiling: {os.path.basename(namespace.file)}...", flush=True, end="")
    progress = ProgressBar(f"$flower Compiling: {os.path.basename(namespace.file)}...")
    prompt = format(promptTemplate, namespace)
    if namespace.show_prompt:
        print(prompt)
    ai = zhipuai.ZhipuAI(api_key=key)
    progress.start()
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
    progress.stop()
    if isinstance(response, Completion):
        response_content = response.choices[0].message.content
        if response_content:
            output = getOutput(response_content)
            if showState:
                print("Status:", getStatus(response_content))
            if getStatus(response_content):
                if showState:
                    dependencies = getDependencies(response_content)
                    if len(dependencies) > 0:
                        print("Dependencies:")
                        for i in dependencies:
                            print(f" - {i}")
                    else:
                        print("No dependencies.")
                open(
                    format(namespace.output, namespace, getExtension(response_content)),
                    "w",
                    encoding="utf8",
                ).write(getData(output))
            else:
                print(getData(output))
    else:
        raise ValueError("Unexpected response type or empty choices.")
    if namespace.watch:
        print("Watching...")
        namespace.watch = False
        watch(namespace, run)


def parseConfigFile(path: str):
    haveWatch = False
    mergedDict = mergeDictRecursive(
        defaultConfig,
        json.load(open(path, encoding="utf8")),
    )
    mergedDict["includes"] = list(
        map(
            lambda x: mergeDictRecursive(
                defaultInclude,
                mergedDict["common"],
                x,
            ),
            mergedDict["includes"],
        )
    )
    if mergedDict["common"].get("watch") == True:
        haveWatch = True
    else:
        for i in mergedDict["includes"]:
            if i.get("watch") == True:
                haveWatch = True
                break
    configData: ConfigFile = ConfigFile(mergedDict)
    return configData, mergedDict, haveWatch


def generateNamespaceFromInclude(include: ConfigInclude):
    return ArgNamespace(file=include.input, **vars(include))

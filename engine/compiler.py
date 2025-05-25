import os
from rich import print

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
    "model": "chatglm",
}
promptTemplate = open("prompt.txt", encoding="utf8").read()
key: str | None = None
pluginInstances: dict[str, Plugin] = {}
pluginEvents: dict[str, dict[str, Callable]] = {
    "whenRequest": {},
    "formatPrompt": {},
    "fileChangeHandled": {},
}  # 事件名称->插件别名->函数


def hasEvent(event: str, alias: str):
    return event in pluginEvents and alias in pluginEvents[event]


def callEvent(event: str, alias: str, must: bool, *args):
    if hasEvent(event, alias):
        return pluginEvents[event][alias](*args)
    elif must:
        raise ValueError(f"calling event {event} but not found in {alias}.")


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
        .replace("$model", namespace.model)
    )


def run(namespace: ArgNamespace, showState: bool = True):
    progress = ProgressBar(
        f"[bold yellow]$flower.0[/bold yellow] Compiling: {os.path.basename(namespace.file)}...",
        Flower("-", "\\\\", "|", "/"),
    )
    prompt = format(promptTemplate, namespace)
    if hasEvent("formatPrompt", namespace.model):
        prompt = callEvent("formatPrompt", namespace.model, False, prompt, namespace)
    if namespace.show_prompt:
        print("[bold]Prompt[/bold]:", prompt)
    progress.start()
    response_content = ""
    try:
        response_content = callEvent(
            "whenRequest",
            namespace.model,
            True,
            object(),
            prompt,
            key,
            namespace,
        )
    finally:
        progress.stop()
    if type(response_content) == str:
        output = getOutput(response_content)
        if showState:
            print(
                "[bold]Status[/bold]:",
                (
                    "[cyan]Success[/cyan]"
                    if getStatus(response_content)
                    else "[red]Failed[/red]"
                ),
            )
        if getStatus(response_content):
            if showState:
                dependencies = getDependencies(response_content)
                if len(dependencies) > 0:
                    print("[bold]Dependencies[/bold]:")
                    for i in dependencies:
                        print(f" - {i}")
                else:
                    print("[bold]No[/bold] dependencies.")
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

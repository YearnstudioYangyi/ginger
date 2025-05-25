from typing import Callable, Any
from ..structs import ArgNamespace
from .. import compiler


def whenRequest(alias: str):
    def wrapper(func: Callable[[str, str, ArgNamespace, str], str]):
        compiler.pluginEvents["whenRequest"][alias] = func
        return func

    return wrapper


def formatPrompt(alias: str):
    def wrapper(func: Callable[[str, ArgNamespace], str]):
        compiler.pluginEvents["formatPrompt"][alias] = func
        return func

    return wrapper


def fileChangeHandled(alias: str):
    def wrapper(func: Callable[[str, ArgNamespace], None]):
        compiler.pluginEvents["fileChangeHandled"][alias] = func
        return func

    return wrapper

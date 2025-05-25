from .. import compiler
from ..structs import Plugin
from typing import Type


def register(func: Type[Plugin]):
    instance = func()
    compiler.pluginInstances[instance.name] = instance
    return func

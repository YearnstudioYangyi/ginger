from .. import compiler
from ..structs import Plugin
from typing import Type


def plugin(func: Type[Plugin]):
    instance = func()
    compiler.pluginInstances[instance.name] = instance
    return func

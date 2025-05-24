from argparse import Namespace


class ArgNamespace(Namespace):
    file: str
    config_file: str
    language: str
    traceback: str
    indent: int
    key: str
    show_prompt: bool
    output: str
    watch: bool


class ConfigInclude:
    input: str
    language: str
    output: str
    traceback: str
    indent: int
    show_prompt: bool
    watch: bool

    def __init__(self, data: dict) -> None:
        self.__dict__ = data


class ConfigFile:
    includes: list[ConfigInclude]
    common: ConfigInclude

    def __init__(self, data: dict) -> None:
        self.common = ConfigInclude(data["common"])
        self.includes = []
        for i in data["includes"]:
            self.includes.append(ConfigInclude(i))

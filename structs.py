from argparse import Namespace


class ArgNamespace(Namespace):
    file: str
    language: str
    traceback: str
    indent: int
    key: str

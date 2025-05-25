import os, importlib, sys
from argparse import ArgumentParser
from rich import print

from engine.structs import *
from engine.compiler import *
from engine.watcher import *
from engine.tools import *

if __name__ == "__main__":
    sys.path.append(os.getcwd())
    args = ArgumentParser()
    args.add_argument("-k", "--key", required=True)
    args.add_argument("-f", "--file")
    args.add_argument("-c", "--config-file")
    args.add_argument("-l", "--language", default="Python")
    args.add_argument("-t", "--traceback", default="en-US")
    args.add_argument("-i", "--indent", default=4)
    args.add_argument("-o", "--output", default="$basename$extension")
    args.add_argument("-m", "--model", default="chatglm")
    args.add_argument("-p", "--show-prompt", action="store_true")
    args.add_argument("-w", "--watch", action="store_true")
    namespace = ArgNamespace(**vars(args.parse_args()))
    namespace.indent = int(namespace.indent)

    setKey(namespace.key)
    if namespace.file and namespace.config_file:
        raise ValueError("You cannot specify both file and config file.")
    elif not namespace.file and not namespace.config_file:
        raise ValueError("You must specify either file or config file.")

    for dirName in os.listdir("plugins"):
        pluginDir = os.path.join("plugins", dirName)
        pluginMainFile = os.path.join(pluginDir, "main.py")
        if os.path.isdir(pluginDir):
            if os.path.exists(pluginMainFile):
                if os.path.isfile(pluginMainFile):
                    importlib.import_module(f"plugins.{dirName}.main")
                else:
                    raise FileNotFoundError(f"Plugin {dirName} main.py is not a file")
            else:
                raise FileNotFoundError(f"Plugin {dirName} does not have main.py")

    if namespace.file:
        run(namespace, not namespace.watch)
        if namespace.watch:
            waitPress()
            clearTerminal()
            print("Watching...")
            blockWait()
    elif namespace.config_file:
        config, merged, haveWatch = parseConfigFile(namespace.config_file)
        for dirName in config.includes:
            current = generateNamespaceFromInclude(dirName)
            run(current, not current.watch)
        if haveWatch:
            waitPress()
            clearTerminal()
            print("Watching...")
            blockWait()

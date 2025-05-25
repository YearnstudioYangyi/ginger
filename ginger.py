from argparse import ArgumentParser
from engine.structs import *
from engine.compiler import *
from engine.watcher import *
from engine.tools import *

if __name__ == "__main__":
    args = ArgumentParser()
    args.add_argument("-k", "--key", required=True)
    args.add_argument("-f", "--file")
    args.add_argument("-c", "--config-file")
    args.add_argument("-l", "--language", default="Python")
    args.add_argument("-t", "--traceback", default="en-US")
    args.add_argument("-i", "--indent", default=4, type=int)
    args.add_argument("-o", "--output", default="$basename$extension")
    args.add_argument("-p", "--show-prompt", action="store_true")
    args.add_argument("-w", "--watch", action="store_true")
    namespace = ArgNamespace(**vars(args.parse_args()))

    setKey(namespace.key)
    if namespace.file and namespace.config_file:
        raise ValueError("You cannot specify both file and config file.")
    elif not namespace.file and not namespace.config_file:
        raise ValueError("You must specify either file or config file.")
    elif namespace.file:
        run(namespace, not namespace.watch)
        if namespace.watch:
            clearTerminal()
            blockWait()
    elif namespace.config_file:
        config, merged, haveWatch = parseConfigFile(namespace.config_file)
        for i in config.includes:
            current = generateNamespaceFromInclude(i)
            run(current, not current.watch)
        if haveWatch:
            clearTerminal()
            blockWait()

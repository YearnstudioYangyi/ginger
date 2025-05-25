import os, time, sys
from watchdog import observers, events
from typing import Callable
from rich import print

from .structs import *
from .tools import *


class WatchFileChange(events.FileSystemEventHandler):
    namespace: ArgNamespace
    run: Callable
    callEvent: Callable

    def update(self, event: events.FileSystemEvent):
        if not event.is_directory and areSameFile(self.namespace.file, event.src_path):
            print("File changing handled:", event.src_path)
            self.callEvent(
                "fileChangeHandled",
                self.namespace.model,
                False,
                self.namespace.file,
                self.namespace,
            )
            self.run(self.namespace, False)

    def __init__(self, namespace: ArgNamespace, run: Callable, callEvent: Callable):
        self.namespace = namespace
        self.run = run
        self.callEvent = callEvent

    def on_modified(self, event):
        self.update(event)

    def on_created(self, event):
        self.update(event)


def watch(namespace: ArgNamespace, run: Callable, callEvent: Callable):
    handler = WatchFileChange(namespace, run, callEvent)
    observer = observers.Observer()
    observer.schedule(handler, os.path.dirname(namespace.file), recursive=False)
    observer.start()


def blockWait():
    try:
        while True:
            time.sleep(1)
    except:
        sys.exit(0)

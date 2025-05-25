import threading, time
from rich import print

from .tools import getTerminalRenderLength


class Flower:
    chars: list[str]
    index: int = 0

    def __init__(self, *chars: str) -> None:
        self.chars = list(chars)

    def get(self):
        return self.chars[self.index % len(self.chars)]

    def next(self):
        self.index += 1
        return self.get()


class ProgressBar:
    running: bool = False
    times: int = 0
    thread: threading.Thread | None = None
    lastRendered: str = ""

    flowers: list[Flower]
    template: str
    interval: float = 100

    def __init__(self, template: str, *flowers: Flower):
        self.thread = threading.Thread(target=self.render)
        self.flowers = list(flowers)
        self.template = template

    def format(self, done: bool = False):
        result = self.template
        for index in range(len(self.flowers)):
            flower = self.flowers[index]
            result = result.replace(f"$flower.{index}", "√" if done else flower.next())
        return result.replace("$times", str(self.times))

    def render(self, one: bool = False, end: str = "\r", done: bool = False):
        if one:
            print(getTerminalRenderLength(self.lastRendered) * " ", end="\r")
            self.lastRendered = self.format(done)
            print(self.lastRendered, end=end, flush=True)
        else:
            while self.running:
                self.render(True)
                self.times += 1
                time.sleep(self.interval / 1000)

    def start(self):
        if self.thread:
            self.running = True
            self.thread.start()

    def stop(self):
        self.running = False
        self.render(True, "", True)
        print("[green]Done![/green]")

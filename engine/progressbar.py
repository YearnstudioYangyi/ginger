import threading, time, random


class ProgressBar:
    running: bool = False
    times: int = 0
    thread: threading.Thread | None = None
    flower: str = "-\\|/"
    interval: float = 100
    template: str = "$flower"

    def __init__(self, template: str, flower: str = "-\\|/", interval: float = 100):
        self.thread = threading.Thread(target=self.render)
        self.flower = flower
        self.interval = interval
        self.template = template

    def getFlowerChar(self):
        return self.flower[self.times % len(self.flower)]

    def format(self, done: bool = False):
        return (
            self.template.replace("$flower", "√" if done else self.getFlowerChar())
            .replace("$times", str(self.times))
            .replace("$interval", str(self.interval))
            .replace("$random", str(random.randint(0, 10000)))
        )

    def render(self, one: bool = False, end: str = "\r", done: bool = False):
        if one:
            print(self.format(done), end=end, flush=True)
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
        print("Done!")

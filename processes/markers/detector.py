from threading import Thread
from . import detection
from time import sleep

class MarkDetector:
    def __init__(self, time = 0.1, name = "MarkDetector"):
        self.name = name
        self.frame = None
        self.result = None
        self.time = time
        self.image = None

    def update (self):
        while True:
            sleep(self.time)
            if self.frame is not None:
                (self.result, self.image) = detect(self.frame)

    def setFrame(self, frame):
        self.frame = frame
        if self.frame is not None:
            (self.result, self.image) = detect(self.frame)

    def read(self):
        return self.result, self.image



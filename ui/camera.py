from threading import Thread
from cv2 import VideoCapture
from time import sleep

class WebcamVideoStream:
    def __init__(self, src = 0, time = 0.01, name = "WebcamVideoStream"):
        self.stream = VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.name = name
        self.stopped = False
        self.time = time

    def start(self):
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return
            sleep(self.time)
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True

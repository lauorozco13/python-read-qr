#!/usr/bin/env python

from sys import stdout
from cv2 import COLOR_BGR2RGB, flip, cvtColor
from processes.markers.detector import MarkDetector
from PIL.Image import fromarray
from PIL.ImageTk import PhotoImage
from ui.window import Window
from ui.camera import WebcamVideoStream
from imutils import resize

class Attendance:

    def __init__(self, title, width, height, x, y):
        self.window = Window(title, width, height, x, y)
        self.width = width
        self.window.canvas(width, height)
        self.detector = MarkDetector()
        self.capture = WebcamVideoStream(src = 0).start()
        self.markerList = []
        self.prevRead = 0
        self.readQty = 0

    def update(self):
        self.process()

    def start(self):
        while True:
            self.update()

    def startLoop(self):
        self.loopAfter()
        self.window.mainLoop()

    def loopAfter(self):
        try:
            self.process()
            self.window.after(target = self.loopAfter)
        except:
            self.__del__()

    def process(self):
        result = None
        frame = self.capture.read()

        
        if self.capture.grabbed is None or frame is None:
            return

        self.detector.setFrame(frame)
        (result, image) = self.detector.read()
        
        if image is not None and result is not None and len(result) > 0:
            frame = image
        frame = resize(frame, width=self.width)
        photo = PhotoImage(image = fromarray(flip(cvtColor(frame, COLOR_BGR2RGB), 1)))
        self.window.updateImageCanvas(photo)
        self.window.update()
        self.report(result)


    def report(self, result):
        if result is not None and len(result) > 0:
            for r in result:
                if self.prevRead == r[0]:
                    self.readQty += 1
                    first_or_default = next((x for x in self.markerList if x[0] == r[0]), None)
                    if first_or_default is not None:
                        stdout.write(",".join(str(x) for x in r) + "\n")
                        stdout.flush()
                    elif self.readQty >= 10:
                        self.markerList.append(r)
                        stdout.write(",".join(str(x) for x in r) + "\n")
                        stdout.flush()
                else:
                    self.readQty = 0
                self.prevRead = r[0]

    def __del__(self):
        try:
            self.capture.stop()
            stdout.write("exit\n")
            stdout.flush()
            self.window.remove()
        except:
            pass

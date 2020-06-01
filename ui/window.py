from Tkinter import Tk, Canvas, NW, Label

class Window:
    def __init__(self, title = "Window", width = None, height = None, x = None, y = None):
        self._window = Tk()
        self._window.title(title)
        self._window.geometry('%sx%s+%s+%s' % (width, height, x, y))
        self._delay = 0

    def canvas(self, width, height):
        self._canvas = Canvas(self._window, width = width, height = height)
        self._canvas.pack(pady=50)
        self._canvas.pack()

    def updateImageCanvas(self, photo):
        self._canvas.create_image(0, 0, image = photo, anchor = NW)

    def setDelay(self, delay = 0):
        self._delay = delay

    def update(self):
        self._window.update_idletasks()
        self._window.update()

    def after(self, target):
        if target is not None:
            self._window.after(self._delay, target)

    def remove(self):
        self._window.destroy()
        self._window.quit()

    def mainLoop(self):
        self._window.mainloop()

    def addText(self, title, width, height):
        self.label = Label(self._window, text = title, font = ("Helvetica", 16))
        self.label.place(x = 60, y = height - 50)
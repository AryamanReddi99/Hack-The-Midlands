# ImageRouter.py
# Routes video sources to video sinks

from PyQt5.QtCore import QThread
from imutils.video import VideoStream, FileVideoStream

class ImageRouter(QThread):
    source_is_file = False
    sinks = []

    def __init__(self, filename = ''):
        super(ImageRouter, self).__init__()
        if (filename == ''):
            self.vs = VideoStream(src=0).start()
            self.source_is_file = False
        else:
            self.vs = FileVideoStream(filename).start()
            self.source_is_file = True

        print("Started ImageRouter")

    def __del__(self):
        print("Stopped ImageRouter")
        self.vs.stop()

    def add_sink(self, sink):
        self.sinks.append(sink)

    def remove_sink(self, sink):
        self.sinks.remove(sink)

    def tick(self):
        if self.source_is_file and not self.vs.more():
            return False
        frame = self.vs.read()
        if frame is None:
            return False
        for sink in self.sinks:
            sink.handle(frame)
        return True

    def run(self):
        while self.isRunning() and self.tick():
            QThread.msleep(10)

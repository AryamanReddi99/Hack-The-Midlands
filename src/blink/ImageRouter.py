# ImageRouter.py
# Routes video sources to video sinks
from time import sleep

import numpy as np
from PyQt5 import QtCore
from imutils.video import VideoStream, FileVideoStream


class ImageRouter(QtCore.QObject):
    source_is_file = False
    on_frame = QtCore.pyqtSignal(np.ndarray)

    def __init__(self, filename=''):
        super().__init__()
        if filename == '':
            self.vs = VideoStream(src=0).start()
            self.source_is_file = False
        else:
            self.vs = FileVideoStream(filename).start()
            self.source_is_file = True

    def __del__(self):
        self.vs.stop()

    def tick(self):
        if self.source_is_file and not self.vs.more():
            return False
        frame = self.vs.read()
        if frame is None:
            return False
        self.on_frame.emit(frame)
        return True

    def run(self):
        print("[INFO] Started ImageRouter")
        while self.tick():
            None
        print("[INFO] Stopped ImageRouter")

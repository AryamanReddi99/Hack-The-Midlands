from twilio.rest import Client
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

#Temporary, will be removed when blink number implemented
import time

from blink.ImageRouter import *
from blink.BlinkDetector import *

from BlinkReminder import *

from blink_app import secrets, config, APP_NAME

class AppWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create main AppWindow and layout
        self.setWindowTitle(APP_NAME)
        layout = QVBoxLayout()
        label = QLabel(APP_NAME)
        label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        layout.addWidget(label)
        self.imageview = QLabel()
        self.imageview.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        layout.addWidget(self.imageview)

        # Create and register ImageRouter on its own QThread
        self.router = ImageRouter()
        self.route_thread = QtCore.QThread()
        self.router.moveToThread(self.route_thread)
        self.route_thread.started.connect(self.router.run)

        # Create and register BlinkDetector plugin
        self.blink_detector = BlinkDetector('shape_predictor_68_face_landmarks.dat')
        self.blink_detector.moveToThread(self.route_thread)
        self.router.on_frame.connect(self.blink_detector.handle_frame)
        self.blink_detector.result.connect(self.update_image)

        # H@K3RY 1Z H3R3
        # Create BlinkReminder (needs a better name than that)
        self.blink_reminder = BlinkReminder(BlinkDetector)

        # Start ImageRouter
        self.route_thread.start()

    @QtCore.pyqtSlot(np.ndarray)
    def update_image(self, image):
        rgbImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        (h, w, c) = rgbImage.shape
        qtImage = QtGui.QImage(rgbImage.data, w, h, w * c, QtGui.QImage.Format_RGB888)
        h = self.imageview.height()
        w = self.imageview.width()
        self.imageview.setPixmap(QPixmap.fromImage(qtImage).scaled(h, w, QtCore.Qt.KeepAspectRatio))

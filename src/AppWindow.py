from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

from blink.ImageRouter import *
from blink.BlinkDetector import *

class AppWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('blink // =_=')
        layout = QVBoxLayout()

        label = QLabel('Hello World')
        layout.addWidget(label)
        self.imageview = QLabel()
        layout.addWidget(self.imageview)
        btn_blink = QPushButton('Blink!')
        layout.addWidget(btn_blink)

        self.setLayout(layout)

        self.router = ImageRouter()
        self.blink_detector = BlinkDetector('shape_predictor_68_face_landmarks.dat')
        self.blink_detector.result.connect(self.update_image)
        self.router.add_sink(self.blink_detector)
        self.router.start()

    @QtCore.pyqtSlot(np.ndarray)
    def update_image(self, image):
        rgbImage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        (h, w, c) = rgbImage.shape
        qtImage = QtGui.QImage(rgbImage.data, w, h, w * c, QtGui.QImage.Format_RGB888)
        self.imageview.setPixmap(QPixmap.fromImage(qtImage))
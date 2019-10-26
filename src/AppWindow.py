from twilio.rest import Client
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

from blink.ImageRouter import *
from blink.BlinkDetector import *

from blink_app import secrets, config, APP_NAME

def make_call():
    account_sid = secrets['twilio']['account_sid']
    auth_token = secrets['twilio']['auth_token']
    from_ = secrets['twilio']['phone_number']
    to = config['user']['phone_number']
    client = Client(account_sid, auth_token)

    call = client.calls.create(
                            url='http://demo.twilio.com/docs/voice.xml',
                            to=to,
                            from_=from_
                            )

class AppWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        layout = QVBoxLayout()
        label = QLabel(APP_NAME)

        layout.addWidget(label)
        self.imageview = QLabel()
        layout.addWidget(self.imageview)

        btn_blink = QPushButton('Call!')
        btn_blink.clicked.connect(make_call)
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
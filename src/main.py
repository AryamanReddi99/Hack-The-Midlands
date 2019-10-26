# Blink demo
from PyQt5.QtWidgets import *

from blink_app import *


print(APP_NAME + ' - Copyright 2019 ' + COMPANY_NAME)

app = QApplication([])

from AppWindow import *
mainwindow = AppWindow()
mainwindow.show()

app.exec_()

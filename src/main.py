# Blink demo

APP_NAME = 'blink // =_='
COMPANY_NAME = 'C.R.E.D.'
print(APP_NAME + ' - Copyright 2019 ' + COMPANY_NAME)

from PyQt5.QtWidgets import *
app = QApplication([])

window = QWidget()
window.setWindowTitle('blink // =_=')
layout = QVBoxLayout()

label = QLabel('Hello World')
layout.addWidget(label)
btn_blink = QPushButton('Blink!')
layout.addWidget(btn_blink)

window.setLayout(layout)
window.show()

app.exec_()

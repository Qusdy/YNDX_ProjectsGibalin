import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog

import registration_form

class Main_Form(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.sign_in = uic.loadUi('Designs(примерно)/sign_in.ui', self)
        self.btn_registration.clicked.connect(self.open_registration)

    def open_registration(self):
        self.registration_form = registration_form.Registration_Form()
        self.registration_form.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Main_Form()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
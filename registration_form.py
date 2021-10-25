from PyQt5 import uic
from PyQt5.QtWidgets import QDialog


class Registration_Form(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('Designs(примерно)/registration.ui', self)
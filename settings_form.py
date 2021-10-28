import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QFileDialog

class Settings_Form(QDialog):
    def __init__(self, login):
        super().__init__()
        self.initUI(login)

    def initUI(self, login):
        self.new_form = uic.loadUi('Designs/settings.ui', self)
        self.new_form.show()
        self.lbl_name.setText(login)
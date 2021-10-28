import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QFileDialog


class Registration_Form(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.registration_form = uic.loadUi('Designs/registration.ui', self)
        self.btn_to_registrate.clicked.connect(self.add_account)

    # Пока не реализовано изменение фотграфии профиля, не прописаны условия пароля и имени пользователя
    def add_account(self):
        login = self.name_input.text()
        password = self.password_input.text()
        con = sqlite3.connect('bd_users.sqlite')
        cur = con.cursor()
        if cur.execute("""SELECT id FROM name_password
            WHERE name = ?""", (login, )).fetchall() == [] and password != '':
            cur.execute("""INSERT into name_password(name, password) VALUES(?, ?)""", (login, password))
            con.commit()
            self.registration_form.close()
        else:
            self.error_label.setText('Такой логин уже есть')
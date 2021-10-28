import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog

import registration_form, settings_form


class Main_Form(QDialog):
    def __init__(self, obj, login):
        super().__init__()
        self.main_display_open(obj, login)

    def main_display_open(self, obj, login):
        self.login = login
        self.main_window = uic.loadUi('Designs/main_window.ui', self)
        self.main_window.show()
        obj.close()

        self.lbl_name.setText(self.login)
        self.btn_settings.clicked.connect(self.settings_open)

    def settings_open(self):
        settings_form.Settings_Form(self.login)


# Т.к. сначала запускается вход, а потом главное окно,
# то я добавил "вход в аккаунт" в мейн файле
class Sign_In(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.form_window = uic.loadUi('Designs/sign_in.ui', self)
        self.btn_registration.clicked.connect(self.open_registration)
        self.btn_enter.clicked.connect(self.checking)

    def open_registration(self):
        self.registration_form = registration_form.Registration_Form()
        self.registration_form.show()

    def checking(self):
        login = self.login_input.text()
        password = self.password_input.text()
        con = sqlite3.connect('bd_users.sqlite')
        cur = con.cursor()
        if cur.execute("""SELECT id FROM name_password
        WHERE name = ?""", (login,)).fetchall() == []:
            self.lbl_error_enter.setText('Нет такого имени')
        elif str(cur.execute("""SELECT password FROM name_password
        WHERE id=(
        SELECT id FROM name_password 
        WHERE name = ?)""", (login, )).fetchone()[0]) != password:
            self.lbl_error_enter.setText('Неверный пароль')
        else:
            Main_Form(self.form_window, login)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Sign_In()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
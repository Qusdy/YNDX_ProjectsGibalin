import sys
from PyQt5.QtWidgets import QApplication
from errors import Invalid_Login, Incorrect_Password
from registration_form import *
from creating_block import *
import settings_form
from WORKING_WITH_DB_USERS import *


class Main_Form(QDialog):
    def __init__(self, last_form, login):
        super().__init__()
        self.initUI(last_form, login)

    def initUI(self, last_form, login):
        self.main_form = uic.loadUi('Designs/main_window.ui', self)
        self.main_form.show()
        last_form.close()

        self.login = login

        self.set_profile_settings()

        self.connecting_btns()

    def connecting_btns(self):
        self.btn_making_block.clicked.connect(self.create_block)

    def create_block(self):
        id = get_id(self.login)
        Create_Block(id, self.login, self.main_form)

    def set_profile_settings(self):
        self.lbl_name.setText(self.login)

        self.photo_of_profile = get_picture(self.login) + '.' + get_picture_format(self.login)
        self.lbl_picture.setPixmap(QPixmap(f'Фотографии пользователей/{self.photo_of_profile}'))

        self.btn_settings.clicked.connect(self.settings_form_open)

    def settings_form_open(self):
        settings_form.Settings_Form(self.login, self.main_form)


class Sign_In(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.sign_in_form = uic.loadUi('Designs/sign_in.ui', self)
        self.sign_in_form.show()

        self.btn_registration.clicked.connect(self.open_registration_form)
        self.btn_enter.clicked.connect(self.entering)

    def open_registration_form(self):
        Registration_Form()

    def entering(self):
        login = self.login_input.text()
        password = self.password_input.text()

        try:
            self.correct_or_not(login, password)

            Main_Form(self.sign_in_form, login)
        except Invalid_Login:
            self.lbl_error_enter.setText('Нет такого имени')
        except Incorrect_Password:
            self.lbl_error_enter.setText('Неверный пароль')

    def correct_or_not(self, login, password):
        if not is_there_that_name(login):
            raise Invalid_Login
        elif get_password(login) != password:
            raise Incorrect_Password

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Sign_In()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
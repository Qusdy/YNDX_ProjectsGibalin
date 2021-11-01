import sys
import sqlite3
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog

import registration_form, settings_form


class Main_Form(QDialog):
    def __init__(self, form, login):
        # После входа в аккаунт мы передаем в основной класс предыдущую форму и логин пользователя
        super().__init__()
        self.main_display_open(form, login)

    def main_display_open(self, form, login):
        # Тут мы открываем нашу форму, закрываем предыдущую форму
        # Тут мы записываем значение логина, чтобы не искать его по-новой в базе данных
        self.login = login
        self.main_window = uic.loadUi('Designs/main_window.ui', self)
        self.main_window.show()
        form.close()

        # Тут мы расставляем в вкладку профиля всю нужную информацию, подключаем нужные кнопки
        # Потом это перекочует в отдельный метод
        self.lbl_name.setText(self.login)
        self.photo_of_profile = self.get_the_photo_of_profile()
        self.lbl_picture.setPixmap(QPixmap(f'Фотографии пользователей/{self.photo_of_profile}'))
        self.btn_settings.clicked.connect(self.settings_open)


    def get_the_photo_of_profile(self):
        # Метод для получения имени фотографии в папке с фотографими профиля
        con = sqlite3.connect('bd_users.sqlite')
        cur = con.cursor()
        photo_name = cur.execute("""SELECT picture, picture_format FROM name_password WHERE name = ?""",
                                 (self.login, )).fetchall()[0]

        con.close()
        return photo_name[0] + '.' + photo_name[1]

    def settings_open(self):
        # Открытие окна settings при нажатиии на соответствующую кнопку
        settings_form.Settings_Form(self.login, self.photo_of_profile, self.main_window)


# Т.к. сначала запускается вход, а потом главное окно,
# то я добавил "вход в аккаунт" в мейн файле
class Sign_In(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self): # Запуск окна входа в аккаунт и подключение нужных кнопок к методам
        self.form_window = uic.loadUi('Designs/sign_in.ui', self)
        self.btn_registration.clicked.connect(self.open_registration)
        self.btn_enter.clicked.connect(self.checking_in_db)

    def open_registration(self): # Открытие формы для регистрации пользователя
        self.registration_form = registration_form.Registration_Form()

    def checking_in_db(self): # Проверка в бд наличия аккаунта и правильности введенного пароля
        login = self.login_input.text() # Получим текст, введенный в поле для логина и текст, введенный в поле пароля
        password = self.password_input.text()
        con = sqlite3.connect('bd_users.sqlite')
        cur = con.cursor()

        if cur.execute("""SELECT id FROM name_password WHERE name = ?""",
                       (login,)).fetchall() == []: # Проверка наличия логина в дб
            self.lbl_error_enter.setText('Нет такого имени')
        elif str(cur.execute("""SELECT password FROM name_password WHERE id=(SELECT id FROM name_password WHERE name = ?)""",
                             (login, )).fetchone()[0]) != password: # Проверка правильности пароля
            self.lbl_error_enter.setText('Неверный пароль')
        else: # Если все правильно, открываем главную форму
            Main_Form(self.form_window, login)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Sign_In()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
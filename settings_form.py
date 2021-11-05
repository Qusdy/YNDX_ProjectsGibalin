from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QFileDialog, QInputDialog, QMessageBox
from WORKING_WITH_DB_USERS import *
from errors import Name_Already_Taken_Error
import os
from main import *

class Settings_Form(QDialog):
    def __init__(self, login, main_form):
        super().__init__()
        self.initUI(login, main_form)

    def initUI(self, login, main_form):
        self.new_form = uic.loadUi('Designs/settings.ui', self)
        self.new_form.setModal(True)
        self.new_form.show()

        self.main_form = main_form

        self.last_login = login
        self.last_photo = get_picture(self.last_login) + '.' + get_picture_format(self.last_login)

        self.new_login = False
        self.new_photo = False

        self.set_settings()

    def set_settings(self):
        self.lbl_picture.setPixmap(QPixmap(f'Фотографии пользователей/{self.last_photo}'))
        self.lbl_name.setText(self.last_login)

        # Подключение кнопок к методам
        self.btn_to_change_name.clicked.connect(self.changing_name)
        self.btn_to_change_pic.clicked.connect(self.changing_photo)
        self.btn_to_save.clicked.connect(self.saving_changes)
        self.btn_to_delete_account.clicked.connect(self.delete_account)

    def changing_name(self):
        # Открытие диалогового окна для получения нового имени пользователя
        new_login, ok_pressed = QInputDialog.getText(self, "Введите имя",
                                                "Введите имя пользователя:")
        if ok_pressed:
            self.lbl_name.setText(new_login)
            self.new_login = new_login

    def changing_photo(self):
        # Открытие диалогового окна для получения новой фотографии пользователя
        new_photo = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.jpg);;Картинка (*.png);; Картинка (*.bmp);; Картинка (*.gif);;Картинка (*.jpeg)')[0]
        if new_photo:
            self.lbl_picture.setPixmap(QPixmap(new_photo))
            self.new_photo = new_photo

    def saving_changes(self):
        if self.new_login:
            try:
                self.check_login()
                updating_login(self.new_login, self.last_login)

                if self.new_photo:
                    self.change_photo(self.new_login)
                else:
                    self.change_photo_name()
                self.update_the_main_window(self.new_login)
            except Name_Already_Taken_Error:
                self.lbl_error.setText('Это имя уже занято, поменяйте!')
        else:
            if self.new_photo:
                self.change_photo(self.last_login)
            self.update_the_main_window(self.last_login)

    def check_login(self):
        if is_there_that_name(self.new_login) and self.new_login != self.last_login:
            raise Name_Already_Taken_Error

    def change_photo(self, login):
        self.delete_last_photo()

        saving_new_profile_photo(self.new_photo, login)
        change_photo_in_db(login, self.new_photo.split('.')[1])

    def change_photo_name(self):
        saving_new_profile_photo(f'Фотографии пользователей/{self.last_photo}', self.new_login)
        saving_new_picture_name(self.new_login)

        self.delete_last_photo()

    def delete_last_photo(self):
        if self.last_photo != 'standart_pic.png':
            os.remove(f'Фотографии пользователей/{self.last_photo}')

    def update_the_main_window(self, login):
        self.main_form.close()
        Main_Form(self.new_form, login)

    def delete_account(self):
        if self.open_dialog():
            delete_account(self.last_login)
            Sign_In()
            self.new_form.close()
            self.main_form.close()

    def open_dialog(self):
        msgBox = QMessageBox()
        msgBox.setModal(True)
        msgBox.setText("Вы уверены?")
        msgBox.setWindowTitle("Удаление аккаунта")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        result = msgBox.exec()

        if result == msgBox.Ok:
            return True
        return False
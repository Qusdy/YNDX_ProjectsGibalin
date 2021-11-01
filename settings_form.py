import sqlite3
from PyQt5 import uic
from PIL import Image
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QFileDialog, QInputDialog
import os
import main

class Settings_Form(QDialog):
    def __init__(self, login, photo, main_form):
        # Сюда мы передаем имя пользователя,
        # фотографию профиля,
        # Главную форму, которую будем перезапускать после внесения изменений
        super().__init__()
        self.initUI(login, photo, main_form)

    def initUI(self, login, photo, main_form):
        # Открытие нашей формы
        self.new_form = uic.loadUi('Designs/settings.ui', self)
        self.new_form.setModal(True)
        self.new_form.show()
        self.main_form = main_form

        # Значения логина и фотографии
        # до изменения
        self.last_login, self.last_photo = login, photo

        # Значения указывающие на наличие изменений фотографии профиля и
        #  Логина
        self.avatar_is_there = None
        self.changed_name = None

        # Подстановка логина и фотографии в соответствующие label'ы
        self.lbl_picture.setPixmap(QPixmap(f'Фотографии пользователей/{photo}'))
        self.lbl_name.setText(login)

        # Подключение кнопок к методам
        self.btn_to_change_name.clicked.connect(self.changing_name)
        self.btn_to_change_pic.clicked.connect(self.changing_photo)
        self.btn_to_save.clicked.connect(self.saving_changes)

    def changing_name(self):
        # Открытие диалогового окна для получения нового имени пользователя
        new_login, ok_pressed = QInputDialog.getText(self, "Введите имя",
                                                "Введите имя пользователя:")
        if ok_pressed:
            self.lbl_name.setText(new_login)
            self.changed_name = new_login

    def changing_photo(self):
        # Открытие диалогового окна для получения новой фотографии пользователя
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.jpg);;Картинка (*.png);; Картинка (*.bmp);; Картинка (*.gif);;Картинка (*.jpeg)')[0]
        if fname:
            self.lbl_picture.setPixmap(QPixmap(fname))
            self.avatar_is_there = fname

    # Следующий код работает не совсем корректно, поэтому будет ещё переписан.

    def saving_changes(self):
        con = sqlite3.connect('bd_users.sqlite')
        cur = con.cursor()
        if self.changed_name != None:
            if cur.execute("""SELECT name FROM name_password WHERE name = ?""",
                           (self.changed_name,)).fetchall() == [] or self.changed_name == self.last_login:
                cur.execute("""UPDATE name_password SET name = ? WHERE name = ?""", (self.changed_name, self.last_login,))
                con.commit()
                if self.avatar_is_there == None:
                    self.changing_photo_name(self.last_login, self.changed_name, cur)
            else:
                self.lbl_error.setText('Извините, но это имя занято, поменяйте его.')
            login = self.changed_name
        else:
            login = self.last_login
        if self.avatar_is_there != None and (cur.execute("""SELECT name FROM name_password WHERE name = ?""",
                                                        (self.changed_name,)).fetchall() == [] or self.changed_name == self.last_login):
            self.deleting_last_photo(cur, login)
            self.saving_new_avatar(login, con, cur)

        con.close()
        self.main_form.close()
        main.Main_Form(self.new_form, login)

    def deleting_last_photo(self, cur, login):
        if cur.execute("""SELECT picture FROM name_password WHERE name = ?""", (login, )).fetchall()[0][0] != 'standart_pic':
            last_format_name = cur.execute("""SELECT picture_format FROM name_password WHERE name = ?""", (login,)).fetchall()[0][0]
            os.remove(f'Фотографии пользователей/{self.last_login}.{last_format_name}')

    def saving_new_avatar(self, login, con, cur):
        format_name = self.avatar_is_there.split('.')[1]
        image = Image.open(self.avatar_is_there)
        image.save(f'Фотографии пользователей/{login}.{format_name}')

        cur.execute("""UPDATE name_password SET picture = ?, picture_format = ? WHERE name = ?""", (login, format_name, login))
        con.commit()
        # Напомню, что имя фотографии совпадает с именем пользователя

    def changing_photo_name(self, last_login, changed_login, cur):
        last_picture_name = cur.execute("""SELECT picture FROM name_password WHERE name = ?""",
                       (changed_login,)).fetchall()[0][0]
        if last_picture_name != 'standart_pic':
            last_picture_format = cur.execute("""SELECT picture_format FROM name_password WHERE picture = ?""",
                                         (last_login,)).fetchall()[0][0]
            image = Image.open(f'Фотографии пользователей/{last_login}.{last_picture_format}')
            new_picture_format = self.avatar_is_there.split('.')[1]
            image.save(f'Фотографии пользователей/{changed_login}.{new_picture_format}')
            self.deleting_last_photo(cur, changed_login)


import sqlite3
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QFileDialog
from PIL import Image


class Length_Of_Password_Error(Exception): # Ошибка в случае, если длина меньше 6 символов
    pass


class Name_Already_Taken_Error(Length_Of_Password_Error): # Ошибка в случае, если имя, введенное пользователем уже есть
    pass


class Registration_Form(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self): # Открытие формы и подключение кнопок к методам
        self.registration_form = uic.loadUi('Designs/registration.ui', self)
        self.registration_form.setModal(True)
        self.registration_form.show()

        self.avatar_is_there = None # Переменная, где буде храниться путь к фотографии пользователя, если он её поменяет

        self.btn_pic_changing.clicked.connect(self.add_photo)
        self.btn_to_registrate.clicked.connect(self.add_account)

    def add_account(self): # Метод для проверки выполнения всех условий и для записи данных в базу данных
        login = self.name_input.text() # Считываем логин и пароль, введенные пользователем
        password = self.password_input.text()

        con = sqlite3.connect('bd_users.sqlite')
        cur = con.cursor()
        try:
            self.checking_password_and_login(login, password) # Проверяем на ошибки введенные логин и пароль

            if self.avatar_is_there != None: # Если фотография была выбрана
                # Сохраняем в папке Фотографии пользователей фотографию, выбранную пользователем в виде
                # Имя пользователя.Имя формата
                format_name = self.avatar_is_there.split('.')[1]
                image = Image.open(self.avatar_is_there)
                image.save(f'Фотографии пользователей/{login}.{format_name}')

                # Записываем в базу данных всю информацию о пользователе
                cur.execute("""INSERT into name_password(name, password, picture, picture_format) VALUES(?, ?, ?, ?)""",
                            (login, password, login, format_name)) # Файлы изображений имеют то же самое имя, что и логин
                con.commit()

                self.registration_form.close()

            else: # В ином случае записываем имя и пароль пользователя, а фотография остается стандартной
                cur.execute("""INSERT into name_password(name, password) VALUES(?, ?)""", (login, password))
                con.commit()
                self.registration_form.close()
        # Вывод ошибок на эран
        except Name_Already_Taken_Error:
            self.error_label.setText('Имя уже занято!')
        except Length_Of_Password_Error:
            self.error_label.setText('Пароль слишком короткий!')

    def checking_password_and_login(self, login, password): # Метод для проверки наличия ошибок при регистрации пользователя
        con = sqlite3.connect('bd_users.sqlite')
        cur = con.cursor()
        if cur.execute("""SELECT id FROM name_password WHERE name = ?""",
                       (login, )).fetchall() != []:
            raise Name_Already_Taken_Error
        elif len(password) < 6:
            raise Length_Of_Password_Error


    def add_photo(self): # Метод изменения фотографии пользователя при помощи диалогового окна
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.jpg);;Картинка (*.png);; Картинка (*.bmp);; Картинка (*.gif);;Картинка (*.jpeg)')[0]
        if fname:
            self.lbl_pic.setPixmap(QPixmap(fname)) # Отображение выбранной картинки в рамке для картинки
            self.avatar_is_there = fname

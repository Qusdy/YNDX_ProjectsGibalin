from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QFileDialog
from errors import Length_Of_Password_Error, Name_Already_Taken_Error, Name_Is_Not_Written
from WORKING_WITH_DB_USERS import *


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

        try:
            self.checking_password_and_login(login, password) # Проверяем на ошибки введенные логин и пароль

            if self.avatar_is_there != None: # Если фотография была выбрана
                # Сохраняем в папке Фотографии пользователей фотографию, выбранную пользователем в виде
                # Имя пользователя.Имя формата

                saving_new_profile_photo(self.avatar_is_there, login)
                format_name = self.avatar_is_there.split('.')[1]
                # Записываем в базу данных всю информацию о пользователе
                registration_with_changing_photo(login, password, format_name) # Файлы изображений имеют то же самое имя, что и логин
            else: # В ином случае записываем имя и пароль пользователя, а фотография остается стандартной
                registration_without_changing_photo(login, password)

            id = get_id(login)
            create_tables(id)

            self.registration_form.close()
        # Вывод ошибок на эран
        except Name_Already_Taken_Error:
            self.error_label.setText('Имя уже занято!')
        except Length_Of_Password_Error:
            self.error_label.setText('Пароль слишком короткий!')
        except Name_Is_Not_Written:
            self.error_label.setText('Вы ничего не ввели!')

    def checking_password_and_login(self, login, password): # Метод для проверки наличия ошибок при регистрации пользователя
        if is_there_that_name(login):
            raise Name_Already_Taken_Error
        elif login == '':
            raise Name_Is_Not_Written
        elif len(password) < 6:
            raise Length_Of_Password_Error


    def add_photo(self): # Метод изменения фотографии пользователя при помощи диалогового окна
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.jpg);;Картинка (*.png);; Картинка (*.bmp);; Картинка (*.gif);;Картинка (*.jpeg)')[0]
        if fname:
            self.lbl_pic.setPixmap(QPixmap(fname)) # Отображение выбранной картинки в рамке для картинки
            self.avatar_is_there = fname

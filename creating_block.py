from PyQt5 import uic
from WORKING_WITH_DB_USERS import *
from PyQt5.QtWidgets import QDialog
from errors import Name_Is_Not_Written, Name_Already_Taken_Error
import datetime as dt
import main


class Create_Block(QDialog):
    def __init__(self, id, login, main_form):
        super().__init__()
        self.initUI(id, login, main_form)

    def initUI(self, id, login, main_form):
        self.new_form = uic.loadUi('Designs/folder_creating.ui', self)
        self.new_form.setModal(True)
        self.new_form.show()

        self.main_form = main_form
        self.id = id
        self.login = login

        self.btns_connecting()

    def btns_connecting(self):
        self.btn_today.clicked.connect(self.today)
        self.btn_tomorrow.clicked.connect(self.tomorrow)
        self.btn_to_create.clicked.connect(self.creating_folder)

    def today(self):
        date = dt.datetime.now().date()
        self.dateEdit.setDate(date)

    def tomorrow(self):
        date = dt.datetime.now().date() + dt.timedelta(days=1)
        self.dateEdit.setDate(date)

    def creating_folder(self):
        name = self.name_of_folder_input.text()
        try:
            self.check_name(name)

            date = '-'.join(self.dateEdit.text().split('-')[::-1])

            creating_block_in_db('blocks_' + str(self.id), name + '(БЛОК)', date)

            self.main_form.close()
            main.Main_Form(self.new_form, self.login)
        except Name_Is_Not_Written:
            self.lbl_error.setText('Введите имя папки!')
        except Name_Already_Taken_Error:
            self.lbl_error.setText('Такая папка уже есть!')

    def check_name(self, name):
        if name == '':
            raise Name_Is_Not_Written
        elif is_there_that_folder_name('blocks_' + str(self.id), name + '(БЛОК)'):
            raise Name_Already_Taken_Error
from PyQt5 import uic
from WORKING_WITH_DB_USERS import *
from PyQt5.QtWidgets import QDialog
from errors import Name_Is_Not_Written, Using_The_Distinctive_Target_Of_Block
import datetime as dt
import main

class Creating_Goal(QDialog):
    def __init__(self, id, login, main_form):
        super().__init__()
        self.initUI(id, login, main_form)

    def initUI(self, id, login, main_form):
        self.new_form = uic.loadUi('Designs/goal_creation.ui', self)
        self.new_form.setModal(True)
        self.new_form.show()

        self.main_form = main_form
        self.id = id
        self.login = login

        self.btns_connecting()
        self.folders_connecting()

    def btns_connecting(self):
        self.btn_today.clicked.connect(self.today)
        self.btn_tomorrow.clicked.connect(self.tomorrow)
        self.btn_to_create.clicked.connect(self.creating_goal)

    def folders_connecting(self):
        name_of_table = 'blocks_' + str(self.id)
        for el in get_all_blocks(name_of_table):
            self.folder_selection.addItem(*el)

    def today(self):
        date = dt.datetime.now().date()
        self.dateEdit.setDate(date)

    def tomorrow(self):
        date = dt.datetime.now().date() + dt.timedelta(days=1)
        self.dateEdit.setDate(date)

    def creating_goal(self):
        name_of_goal = self.name_of_goal_input.text()
        try:
            self.check_name(name_of_goal)

            date = '-'.join(self.dateEdit.text().split('-')[::-1])
            if self.folder_selection.currentText() != 'Без папки':
                folder = get_block_id('blocks_' + str(self.id), self.folder_selection.currentText())
            else:
                folder = None

            creating_goal_in_db('goals_' + str(self.id), name_of_goal, date, folder)

            self.main_form.close()
            main.Main_Form(self.new_form, self.login)
        except Name_Is_Not_Written:
            self.lbl_error.setText('Введите имя цели!')
        except Using_The_Distinctive_Target_Of_Block:
            self.lbl_error.setText('Уберите "(БЛОК)" из названия!')

    def check_name(self, name):
        if name == '':
            raise Name_Is_Not_Written
        elif '(БЛОК)' in name:
            raise Using_The_Distinctive_Target_Of_Block
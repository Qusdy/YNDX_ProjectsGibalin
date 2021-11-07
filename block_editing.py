from PyQt5 import uic
from WORKING_WITH_DB_USERS import *
from PyQt5.QtWidgets import QDialog, QCheckBox, QListWidget, QWidget
import main

class Block_Editing(QDialog):
    def __init__(self, id, login, block_name, main_form):
        super().__init__()
        self.initUI(id, login, block_name, main_form)

    def initUI(self, id, login, block_name, main_form):
        self.new_form = uic.loadUi('Designs/folder_editing.ui', self)
        self.new_form.setModal(True)
        self.new_form.show()

        self.main_form = main_form
        self.id = id
        self.login = login
        self.blocks_name_in_db = 'blocks_' + str(id)
        self.goals_name_in_db = 'goals_' + str(id)

        self.set_values(block_name)

    def set_values(self, block_name):
        self.name_of_block.setText(block_name)
        self.lbl_deadline.setText('Дедлайн до ' + get_date(self.blocks_name_in_db, block_name + '(БЛОК)'))

        #goals_dates = get_dates_without_repeating(get_list(search_goals_in_block_dates(self.goals_name_in_db, self.id)))
        #for date in goals_dates:
            #self.goals_listWidget.addItem('До ' + date)
            #goals = get_list(get_goals_in_block_at_this_date(self.goals_name_in_db, self.id, date))
            #for name in goals:

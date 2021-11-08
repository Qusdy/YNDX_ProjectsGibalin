from PyQt5 import uic
from WORKING_WITH_DB_USERS import *
from PyQt5.QtWidgets import QDialog, QListWidgetItem, QInputDialog
from PyQt5 import QtCore
import main
from MessageBox import open_dialog

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
        self.block_name = block_name
        self.blocks_name_in_db = 'blocks_' + str(id)
        self.goals_name_in_db = 'goals_' + str(id)

        self.set_values(block_name)
        self.connect_btns()

    def set_values(self, block_name):
        self.name_of_block.setText(block_name)
        self.lbl_deadline.setText('Дедлайн до ' + get_date(self.blocks_name_in_db, block_name + '(БЛОК)'))

        goals_dates = get_dates_without_repeating(get_list(search_goals_in_block_dates(self.goals_name_in_db,
                                                                                       get_block_id(self.blocks_name_in_db, block_name + '(БЛОК)'))))
        self.all_goals = []
        for date in goals_dates:
            self.goals_listWidget.addItem('До ' + date)
            goals = get_list(get_goals_in_block_at_this_date(self.goals_name_in_db, get_block_id(self.blocks_name_in_db, block_name + '(БЛОК)'), date))
            for el in goals:
                self.all_goals.append(el)
            for name in goals: # Очень заумная штука, которую я не совсем понял, нашел в интернете
                item = QListWidgetItem()
                item.setText(f'{name}')
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                item.setCheckState(QtCore.Qt.Unchecked)
                self.goals_listWidget.addItem(item)

    def connect_btns(self):
        self.btn_delete_goal.clicked.connect(self.delete_goal_from_block)
        self.btn_to_delete_block.clicked.connect(self.are_you_sure)

    def delete_goal_from_block(self):
        if self.all_goals != []:
            goal, ok_pressed = QInputDialog.getItem(
                self, "Выберите цель", "Какую цель ты удаляешь?",
                (self.all_goals), 1, False)
            if ok_pressed:
                remove_goal_from_block_db(goal, get_block_id(self.blocks_name_in_db, self.block_name + '(БЛОК)'),
                                        self.goals_name_in_db)
                self.goals_listWidget.clear()
                self.set_values(self.block_name)

    def are_you_sure(self):
        if open_dialog():
            for goal in self.all_goals:
                remove_goal_from_block_db(goal, get_block_id(self.blocks_name_in_db, self.block_name + '(БЛОК)'),
                                          self.goals_name_in_db)
            delete_block(self.blocks_name_in_db, self.block_name + '(БЛОК)')
            self.main_form.close()
            main.Main_Form(self.new_form, self.login)
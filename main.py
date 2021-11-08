import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QPixmap
from errors import Invalid_Login, Incorrect_Password
import registration_form, creating_block, block_editing, creating_goal, settings_form
from WORKING_WITH_DB_USERS import *
import datetime as dt


class Main_Form(QDialog):
    def __init__(self, last_form, login):
        super().__init__()
        self.initUI(last_form, login)

    def initUI(self, last_form, login):
        self.main_form = uic.loadUi('Designs/main_window.ui', self)
        self.main_form.show()
        last_form.close()

        self.login = login
        self.id = get_id(self.login)
        self.table_goals = 'goals_' + str(self.id)
        self.table_blocks = 'blocks_' + str(self.id)

        self.set_profile_settings()

        self.set_standart_sorted_goals()

        self.connecting_btns()

    def connecting_btns(self):
        self.btn_making_block.clicked.connect(self.create_block)
        self.btn_making_goal.clicked.connect(self.create_goal)
        self.comboBox_to_sort.currentIndexChanged.connect(self.change_sorting)
        self.goals_listWidget.itemDoubleClicked.connect(self.double_click_handling)
        self.calendarWidget.clicked.connect(self.get_goals_from_widget_date)

    def get_goals_from_widget_date(self):
        self.listWidget_from_calendar.clear()
        date_in_bd = self.sender().selectedDate().toString('yyyy-MM-dd')
        self.listWidget_from_calendar.addItem('.'.join(date_in_bd.split('-')[::-1]))
        for el in get_list(get_goals_on_this_date(self.table_goals, date_in_bd)):
            self.listWidget_from_calendar.addItem(f'\t{el}')
        for el in get_list(get_blocks_on_this_date(self.table_blocks, date_in_bd)):
            self.listWidget_from_calendar.addItem(f'\t{el}')

    def set_standart_sorted_goals(self):
        # Получим отсортированный список дат
        # Всех объектов (Целей, блоков целей)
        dates = get_all_dates(self.table_goals, self.table_blocks)
        for date in dates:
            objects = get_all_objects(self.table_goals, self.table_blocks, date)
            # Для удобного отображения приведем дату в привычный для нас вид
            self.goals_listWidget.addItem('Дедлайн до: ' + '.'.join(date.split('-')[::-1]))
            for name in objects:
                self.goals_listWidget.addItem('\t' + name)

    def set_only_blocks(self):
        all_blocks_dates = get_dates_without_repeating(get_list(search_blocks_dates(self.table_blocks))) # Убираем повторяющиеся даты из полученного списка дат
        for date in all_blocks_dates:
            blocks = get_list(get_blocks_on_this_date(self.table_blocks, date))

            self.goals_listWidget.addItem('Дедлайн до: ' + '.'.join(date.split('-')[::-1]))
            for name in blocks:
                self.goals_listWidget.addItem('\t' + name)

    def set_only_goals(self):
        all_goals_dates = get_dates_without_repeating(get_list(search_goals_dates(self.table_goals))) # Убираем повторяющиеся даты из полученного списка дат
        for date in all_goals_dates:
            goals = get_list(get_goals_on_this_date(self.table_goals, date))

            self.goals_listWidget.addItem('Дедлайн до: ' + '.'.join(date.split('-')[::-1]))
            for name in goals:
                self.goals_listWidget.addItem('\t' + name)

    def change_sorting(self):
        self.goals_listWidget.clear()

        if self.comboBox_to_sort.currentIndex() == 0:
            self.set_standart_sorted_goals()
        elif self.comboBox_to_sort.currentIndex() == 1:
            self.set_only_blocks()
        else:
            self.set_only_goals()

    def double_click_handling(self):
        if self.sender().currentItem().text()[:11] != 'Дедлайн до:':
            if self.sender().currentItem().text()[-6:] == '(БЛОК)':
                block_editing.Block_Editing(self.id, self.login, self.sender().currentItem().text()[1:-6], self.main_form)
            else:
                print('Не реализовано')

    def create_block(self):
        id = get_id(self.login)
        creating_block.Create_Block(id, self.login, self.main_form)

    def create_goal(self):
        creating_goal.Creating_Goal(self.id, self.login, self.main_form)

    def set_profile_settings(self):
        self.lbl_name.setText(self.login)

        self.photo_of_profile = get_picture(self.login) + '.' + get_picture_format(self.login)
        self.lbl_picture.setPixmap(QPixmap(f'Фотографии пользователей/{self.photo_of_profile}'))
        today = dt.datetime.now().date()
        for el in get_list(get_blocks_on_this_date(self.table_blocks, today)):
            self.listWidget_profile.addItem(el)
        for el in get_list(get_goals_on_this_date(self.table_goals, today)):
            self.listWidget_profile.addItem(el)
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
        registration_form.Registration_Form()

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
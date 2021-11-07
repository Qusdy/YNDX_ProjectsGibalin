from PyQt5.QtWidgets import QMessageBox

def open_dialog():
    msgBox = QMessageBox()
    msgBox.setModal(True)
    msgBox.setText("Вы уверены?")
    msgBox.setWindowTitle("Удаление аккаунта")
    msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    result = msgBox.exec()

    if result == msgBox.Ok:
        return True
    return False
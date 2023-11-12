#MainWindowWithClose.py
#A custom main window widget class for Console 2
#Distributed under GNU GPL v3
#Nicholas A. Jose
#Feb 2022

from PyQt5 import QtWidgets

class MainWindow(QtWidgets.QMainWindow):

    is_running = True

    def __init__(self, flab):
        super().__init__()
        self.flab = flab

    def closeEvent(self,event):
        event.ignore()
        closing_question = QtWidgets.QMessageBox()
        closing_question.setStyleSheet("background-color: rgb(255, 255, 255);")
        result = closing_question.question(None,"Confirm Exit...","Are you sure you want to exit ?",QtWidgets.QMessageBox.Yes| QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            completed = self.flab.close_flab()
            self.is_running = False
            event.accept()




from PyQt5 import QtWidgets
import time
import os

class MainWindow(QtWidgets.QMainWindow):

    is_running = True

    def __init__(self, flab):
        super().__init__()
        self.flab = flab

    def closeEvent(self,event):
        event.ignore()
        closing_question = QtWidgets.QMessageBox()
        closing_question.setStyleSheet("background-color: rgb(255, 255, 255);")
        if self.flab.restart:
            if self.flab.project_path != 'NA':
                result = closing_question.question(None,"Confirm Exit...","Are you sure you want to restart " + os.path.basename(self.flab.project_path) + "? This will kill all running tasks.",QtWidgets.QMessageBox.Yes| QtWidgets.QMessageBox.No)
            else:
                result = closing_question.question(None,"Confirm Exit...","Are you sure you want to restart? This will kill all running tasks.",QtWidgets.QMessageBox.Yes| QtWidgets.QMessageBox.No)
        else:
            result = closing_question.question(None,"Confirm Exit...","Are you sure you want to exit? This will kill all running tasks.",QtWidgets.QMessageBox.Yes| QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            self.close()
            completed = self.flab.close_flab()
            self.is_running = False
            event.accept()





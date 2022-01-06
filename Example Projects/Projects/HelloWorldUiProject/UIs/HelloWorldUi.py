from Projects.HelloWorldUiProject.UIs.Designs import HelloWorldDesign
from Projects.HelloWorldUiProject.UIs.Actions import HelloWorldActions
from PyQt5 import QtWidgets
import sys

#A UI for HelloWorld

class UI(HelloWorldDesign.Ui_MainWindow, HelloWorldActions.Actions):

    ui_name = 'HelloWorldUi'

    def __init__(self, flab):
        self.flab = flab

    #The method responsible for starting the UI
    def run(self):
        app = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.setupUi(self.MainWindow)
        self.configure_actions()
        self.MainWindow.show()
        app.exec_()


    #The method responsible for stopping the UI
    def stop(self):
        pass


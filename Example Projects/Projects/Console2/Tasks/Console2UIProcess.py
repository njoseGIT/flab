#Console2UIProcess.py
#A task for running Console 2's UI
#Distributed under GNU GPL v3
#Nicholas A. Jose
#Feb 2022

from UIs.Windows import Console2Window
from PyQt5 import QtWidgets
import sys

class Task():
    task_name = 'Console2UIProcess'
    task_type = 'process'
    queues = ()
    pipes = ()

    def __init__(self, flab):
        self.flab = flab

    #method called when process is running
    def run(self, flab, ui_queue, flab_queue):
        try:
            self.flab = flab
            self.ui_queue = ui_queue
            self.flab_queue = flab_queue
            app = QtWidgets.QApplication(sys.argv)
            ui = Console2Window.GUI(flab, self.ui_queue, self.flab_queue)
            ui.run()
            ui.list_loaded_tasks()
            app.exec_()

        except Exception as e:
            self.flab.display('Error in ConsoleUI')
            self.flab.display(e)
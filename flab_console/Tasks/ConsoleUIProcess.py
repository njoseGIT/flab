from flab_console.UIs import ConsoleUI
from PyQt5 import QtWidgets
import sys

from flab.Templates import TaskTemplate

class Task(TaskTemplate.Task):
    task_name = 'ConsoleUIProcess'
    task_type = 'process'
    queues = ()
    proxies = ()
    pipes = ()

    def __init__(self, flab):
        self.flab = flab

    #method called when process is running
    def run(self, flab, ui_queue, flab_queue, project_path = ''):

        try:
            self.flab = flab
            self.ui_queue = ui_queue
            self.flab_queue = flab_queue
            app = QtWidgets.QApplication(sys.argv)
            #print('project_path= ' + str(project_path))
            ui = ConsoleUI.GUI(flab, self.ui_queue, self.flab_queue, project_path = project_path)
            ui.run()
            ui.list_loaded_tasks()
            app.exec_()

        except Exception as e:
            self.flab.display('Error in ConsoleUI')
            self.flab.display(e)





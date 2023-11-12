#Console2Window.py
#A class for creating Console2's GUI
#Distributed under GNU GPL v3
#Nicholas A. Jose
#Feb 2022

from UIs.Designs import Console2Design
from UIs.Actions import Console2Actions

class GUI(Console2Design.Ui_MainWindow, Console2Actions.Actions):

    def __init__(self, flab, ui_queue, flab_queue):
        self.flab = flab
        self.ui_queue = ui_queue
        self.flab_queue = flab_queue

    def run(self):
        self.create_window()
        self.configure_actions()
        self.start_queue_thread()
        self.MainWindow.show()
        self.click_open_project()



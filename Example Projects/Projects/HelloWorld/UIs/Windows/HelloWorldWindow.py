from PyQt5.QtWidgets import QWidget, QLabel

class GUI():

    def __init__(self, ui_queue, flab_queue):
        self.ui_queue = ui_queue
        self.flab_queue = flab_queue

    def run(self):
        self.window = QWidget()
        self.window.setWindowTitle('Hello, World!')
        helloMsg = QLabel('Hello, World!', parent=self.window)
        helloMsg.move(50, 50)
        self.window.setGeometry(100, 100, 200, 100)
        self.window.show()



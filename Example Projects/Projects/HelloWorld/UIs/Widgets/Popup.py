from PyQt5.QtWidgets import QApplication, QWidget, QLabel

class Popup(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("Popup")

        # Create a label to display the message
        label = QLabel("Hello World!", self)
        label.move(50, 50)

        # Set the size of the window
        self.setGeometry(300, 300, 200, 100)
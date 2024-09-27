from flab3.Templates import UiTemplate
from PyQt5 import QtWidgets, QtGui, QtCore


class Ui(UiTemplate.Ui):
    ui_name = "ExampleUi"

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            app = QtWidgets.QApplication([])
            label = QtWidgets.QLabel("Hello World")
            label.setStyleSheet(
                "QLabel { color: white; font-size: 24px; padding: 10px; background-color: rgba(0, 0, 0, 0); }")

            # Create a translucent window with no frame
            window = QtWidgets.QWidget()
            window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            window.setAttribute(QtCore.Qt.WA_TranslucentBackground)

            # Create a QVBoxLayout and set it as the window's layout
            layout = QtWidgets.QVBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            window.setLayout(layout)

            # Add the label to the layout
            layout.addWidget(label)

            # Start the animation: fade in over 2 seconds
            animation = QtCore.QPropertyAnimation(window, b"windowOpacity")
            animation.setDuration(2000)
            animation.setStartValue(0.0)
            animation.setEndValue(1.0)

            # Show the window and start the animation
            window.show()
            animation.start()

            app.exec_()
        except Exception as e:
            self.flab.display(str(e))

    def stop(self):
        # Perform any necessary cleanup here
        pass
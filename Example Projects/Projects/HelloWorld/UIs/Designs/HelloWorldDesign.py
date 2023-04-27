from PyQt5.QtWidgets import QApplication, QWidget, QLabel

class UI_MainWindow
    window = QWidget()
    window.setWindowTitle('Hello, World!')
    helloMsg = QLabel('Hello, World!', parent=window)
    helloMsg.move(50, 50)
    window.setGeometry(100, 100, 200, 100)
    window.show()
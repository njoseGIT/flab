from flab.Templates import UiTemplate
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

class Ui(UiTemplate.Ui):

    ui_name = 'HelloWorldPyQtUi'

    def __init__(self):
        self.window = None

    def run(self):


        class PopupWindow(QWidget):

            def __init__(self):
                super().__init__()

                # Set window title and size
                self.setWindowTitle('Popup Window')
                self.setGeometry(100, 100, 250, 100)

                # Create label and set text
                label = QLabel('Hello World', self)
                label.move(80, 50)

        # Create QApplication instance
        app = QApplication(sys.argv)

        # Create PopupWindow instance and show it
        popup = PopupWindow()
        popup.show()

        # Run event loop
        sys.exit(app.exec_())

        # Create a new tkinter window
        #self.window = tk.Tk()
        # Set the window title
        #self.window.title(str(self.flab.vars['Hello']))
        # Create a label widget to display the text
        #self.label = tk.Label(self.window, text="Hello, World!")
        # Pack the label widget into the window
        #self.label.pack()
        # Start the tkinter event loop
        #self.window.mainloop()

    def stop(self):
        pass
        #self.window.destroy()
        #self.window.exit()



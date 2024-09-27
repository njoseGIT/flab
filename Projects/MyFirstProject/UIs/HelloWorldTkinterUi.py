import tkinter as tk
from flab3.Templates import UiTemplate

class Ui(UiTemplate.Ui):

    ui_name = 'HelloWorldTkinterUi'

    def __init__(self):
        self.window = None

    def run(self):
        # Create a new tkinter window
        self.window = tk.Tk()
        # Set a variable name
        self.flab.vars.update({'Hello':'World'})
        # Set the window title to a variable value
        self.window.title(str(self.flab.vars['Hello']))
        # Create a label widget to display the text
        self.label = tk.Label(self.window, text="Hello, World!")
        # Pack the label widget into the window
        self.label.pack()
        self.flab.start_task('HelloWorld',0)
        # Start the tkinter event loop
        self.window.mainloop()

    def stop(self):
        self.flab.stop_task('HelloWorld')
        #self.window.quit()
        #self.window.exit()



from PyQt5 import QtWidgets

class LineEdit(QtWidgets.QLineEdit):

    def __init__(self, obj):
        super().__init__(obj)
        self.commandHistory = ['']
        self.commandHistoryPosition = 0

    def keyPressEvent(self,event):
        #key up
        if event.key() == 16777235:
            if len(self.commandHistory) >= 1:
                if self.commandHistoryPosition < len(self.commandHistory)-1:
                    self.commandHistoryPosition = self.commandHistoryPosition+1
                    self.setText(self.commandHistory[self.commandHistoryPosition])
        elif event.key() == 16777237:
            if len(self.commandHistory) >= 1:
                if self.commandHistoryPosition <= len(self.commandHistory)-1 and self.commandHistoryPosition >= 1:
                    self.commandHistoryPosition = self.commandHistoryPosition-1
                    self.setText(self.commandHistory[self.commandHistoryPosition])
        else:
            super().keyPressEvent(event)
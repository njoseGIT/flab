import sys
from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QDateEdit, QSpinBox, QPushButton
from PyQt5.QtCore import QDateTime, QDate, Qt, QTime

class DateTimeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QGridLayout(self)
        self.setWindowTitle("Schedule Task")

        self.dateEdit = QDateEdit(self)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setDate(QDate.currentDate())

        self.hourSpinBox = QSpinBox(self)
        self.hourSpinBox.setRange(0, 23)
        self.hourSpinBox.setValue(QDateTime.currentDateTime().time().hour())

        self.minuteSpinBox = QSpinBox(self)
        self.minuteSpinBox.setRange(0, 59)
        self.minuteSpinBox.setValue(QDateTime.currentDateTime().time().minute())

        self.secondSpinBox = QSpinBox(self)
        self.secondSpinBox.setRange(0, 59)
        self.secondSpinBox.setValue(QDateTime.currentDateTime().time().second())

        okButton = QPushButton('OK', self)
        okButton.clicked.connect(self.accept)

        cancelButton = QPushButton('Cancel', self)
        cancelButton.clicked.connect(self.reject)

        layout.addWidget(QLabel('Date'), 0, 0)
        layout.addWidget(self.dateEdit, 1, 0)
        layout.addWidget(QLabel('Hours'), 0, 1)
        layout.addWidget(self.hourSpinBox, 1, 1)
        layout.addWidget(QLabel('Minutes'), 0, 2)
        layout.addWidget(self.minuteSpinBox, 1, 2)
        layout.addWidget(QLabel('Seconds'), 0, 3)
        layout.addWidget(self.secondSpinBox, 1, 3)
        layout.addWidget(okButton, 2, 0, 1, 2)
        layout.addWidget(cancelButton, 2, 2, 1, 2)

    def getDateTime(self):
        selected_date = self.dateEdit.date()
        selected_time = QTime(self.hourSpinBox.value(), self.minuteSpinBox.value(), self.secondSpinBox.value())

        selected_date_time = QDateTime(selected_date, selected_time)
        return selected_date_time

    def accept(self):
        super().accept()

    def reject(self):
        super().reject()

    def get_timestamp(self):
        timestamp = None
        if self.exec_() == QDialog.Accepted:
            selected_date_time = self.getDateTime()
            timestamp = selected_date_time.toSecsSinceEpoch()

        return timestamp

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     dialog = DateTimeDialog()
#     print(dialog.get_timestamp())
#     dialog.close()
#     app.exit()




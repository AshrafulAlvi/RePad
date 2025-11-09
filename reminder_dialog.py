from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QDateTimeEdit, QPushButton, QMessageBox
from PyQt6.QtCore import QDateTime, Qt

class ReminderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModal(True)
        self.setWindowTitle("Set Reminder")
        self.resize(300,200)

        #small instruction to what to do in the window
        layout = QVBoxLayout(self)
        label = QLabel("Choose date and time")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        #basically setting up the default suggested time
        self.datetime_edit = QDateTimeEdit(self)
        self.datetime_edit.setDisplayFormat("yyyy-MM-dd HH:mm AP")
        min_dateTime = QDateTime.currentDateTime()
        self.datetime_edit.setMinimumDateTime(min_dateTime)
        default = min_dateTime.addSecs(3600)
        self.datetime_edit.setDateTime(default)
        layout.addWidget(self.datetime_edit)

        #Adding buttons
        button_layout = QHBoxLayout()

        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        save_button.clicked.connect(self.accept_dialog)
        cancel_button.clicked.connect(self.reject)

        #Add button layout to main layout
    
    def accept_dialog(self):

        chosen = self.datetime_edit.dateTime()
        if chosen < QDateTime.currentDateTime():
            QMessageBox.warning(self, "Invalid Time", "Please choose a future date and time.")
            return
        else:
            self.accept()
    
    def selected_datetime(self):
        return self.datetime_edit.dateTime()



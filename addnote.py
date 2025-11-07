import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QPushButton, QTextEdit
from PyQt6.QtGui import QIcon, QFont

#This is going to be the new window
class NoteWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Pad")
        self.setGeometry(400,400, 400, 250)

        layout = QHBoxLayout()
        self.text_edit = QTextEdit("")
        font = QFont("Comic Sans MS", 14)
        self.text_edit.setFont(font)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)
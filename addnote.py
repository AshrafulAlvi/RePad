import sys
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTextEdit, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

#This is going to be the new window
class NoteWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Pad")
        self.setGeometry(400,400, 400, 250)

        main_layout = QVBoxLayout() #This is the main window Layout

        #Setting up the top layer for the button colors
        top_bar = QHBoxLayout()
        top_bar.addStretch() #Pushing everything after it to the right
        top_bar.setSpacing(6)
        top_bar.setContentsMargins(0,0,10,0)

        #Setting up the buttons for the top layer
        self.color_buttons = []

        color_list = ["#A7C7E7", "#B7D3C6", "#F5E6A1", "#F4C2C2", "#F8F8F8"]

        for color in color_list:
            btn = QPushButton("")
            btn.setFixedSize(30,30)
            top_bar.addWidget(btn)
            self.color_buttons.append((btn, color))

            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color : {color};
                    border-radius: 4px;
                    border: 1px solid #ccc;
                }}
                QpushButton:hover {{
                    border: 2px solid #555
                }}
                QPushButton:pressed {{
                    border: 2px solid #222
                }}
            """)

            btn.setCursor(Qt.CursorShape.PointingHandCursor)

            #This is to when color button is clicked, it changes text edit background
            btn.clicked.connect(lambda checked, c=color: self.change_pad_color(c))


        bottom_bar = QHBoxLayout() #This is where the save and set reminder will be

        #Setting up the buttons for the bottom layer
        save_button = QPushButton("Save")
        reminder_button = QPushButton("Set Reminder")

        bottom_buttons = [save_button, reminder_button]

        for btn in bottom_buttons:
            btn.setFixedHeight(32)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #e8f0fe;
                    color: #222;
                    font-weight: bold;
                    border-radius: 6px;
                    border: 1px solid #ccc;
                    padding: 6px 12px;
                }
                QPushButton:hover { background-color: #d2e3fc; }
                QPushButton:pressed { background-color: #aecbfa; }
            """)
        
        bottom_bar.addWidget(save_button)
        bottom_bar.addWidget(reminder_button)

        #This is where the user will write
        self.text_edit = QTextEdit("")
        font = QFont("Comic Sans MS", 14)
        self.text_edit.setFont(font)

        #This is where the layouts are actually laying out
        main_layout.addLayout(top_bar)
        main_layout.addWidget(self.text_edit)
        main_layout.addLayout(bottom_bar)
        self.setLayout(main_layout)

    def change_pad_color(self, color):
        self.text_edit.setStyleSheet(f"background-color: {color}")
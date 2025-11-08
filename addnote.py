from reminder_dialog import ReminderDialog
import sys
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QTextEdit, QPushButton, QDialog
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSignal
import os, json, uuid




#This is going to be the new window
class NoteWindow(QWidget):
    note_saved = pyqtSignal()
    def __init__(self, note_data=None):
        super().__init__()
        self.setWindowTitle("New Pad")
        self.setGeometry(400,400, 400, 250)
        self.color = "#F8F8F8"
        self.file_path = "notes.json"

        self.edit_mode = note_data is not None
        self.note_id = None

        if note_data:
            #Load existing note details
            self.note_id = note_data.get("id")
            self.color = note_data.get("color", self.color)

        self.reminder_datetime = None

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
                QPushButton:hover {{
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
        save_button.clicked.connect(self.save_note)

        reminder_button = QPushButton("Set Reminder")
        reminder_button.clicked.connect(self.set_reminder)

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
        self.text_edit.setStyleSheet(f"background-color: {self.color}")

        # If editing an existing note, prefill the content and color
        if self.edit_mode and note_data:
            self.text_edit.setPlainText(note_data.get("content", ""))
            self.change_pad_color(self.color)

        #This is where the layouts are actually laying out
        main_layout.addLayout(top_bar)
        main_layout.addWidget(self.text_edit)
        main_layout.addLayout(bottom_bar)
        self.setLayout(main_layout)

    def change_pad_color(self, color):
        self.color = color
        self.text_edit.setStyleSheet(f"background-color: {color}")

    def save_note(self):
        text = self.text_edit.toPlainText().strip()
        if not text:
            return

        # Load existing notes
        notes = []
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    notes = json.load(f)
            except json.JSONDecodeError:
                pass

        # Helper to format reminder data safely
        def make_reminder():
            if self.reminder_datetime:
                return {
                    "enabled": True,
                    "datetime": self.reminder_datetime.toString(Qt.DateFormat.ISODate)
                }
            else:
                return {"enabled": False, "datetime": None}

        if self.edit_mode and self.note_id:
            # --- Edit existing note ---
            updated = False
            for n in notes:
                if n["id"] == self.note_id:
                    n["content"] = text
                    n["color"] = self.color
                    n["reminder"] = make_reminder()
                    updated = True
                    break
            if not updated:
                notes.append({
                    "id": self.note_id,
                    "content": text,
                    "color": self.color,
                    "reminder": make_reminder()
                })
        else:
            # --- Add new note ---
            note_id = uuid.uuid4().hex
            notes.append({
                "id": note_id,
                "content": text,
                "color": self.color,
                "reminder": make_reminder()
            })

        # --- Save to JSON ---
        with open(self.file_path, 'w') as f:
            json.dump(notes, f, indent=4)

        # Notify & reset
        self.note_saved.emit()
        self.text_edit.clear()
        self.reminder_datetime = None

    def set_reminder(self):
        dlg = ReminderDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            self.reminder_datetime = dlg.selected_datetime()
        else:
            return
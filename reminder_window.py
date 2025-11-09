from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QSizePolicy, QScrollArea, QFrame
from PyQt6.QtCore import pyqtSignal
import json, os

class ReminderWindow(QWidget):
    reminder_updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.file_path = "notes.json"
        self.setWindowTitle("Reminderwindow")
        layout = QVBoxLayout()
        self.setMinimumWidth(350)

        # Making the scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()

        self.scroll_layout = QVBoxLayout()

        # Keeping margins and spacing lines
        layout.setContentsMargins(10, 10, 10, 10)
        self.scroll_layout.setSpacing(5)

        # Adding layouts
        container.setLayout(self.scroll_layout)

        # Setting the layout of the container
        scroll.setWidget(container)
        layout.addWidget(scroll)

        self.setLayout(layout)
        self.load_reminders()

        # --- CSS STUFF ---
        self.setStyleSheet("""
            QPushButton {
                border: none;
                border-radius: 6px;
                padding: 6px 10px;
                font-weight: bold;
                color: #222;
                background-color: #e8f0fe;
            }
            QPushButton:hover {background-color: #d2e3fc;}
            QPushButton:pressed {background-color: #aecbfa;}
            
            QPushButton#delete {background-color: #ff944d; color: white;}
            QPushButton#delete:hover {background-color: #ff7733;}
            QPushButton#delete:pressed {background-color: #e65c00;}
            """)
    
    def load_reminders(self):

        if not os.path.exists(self.file_path):
            return
        with open(self.file_path, 'r') as f:
            notes = json.load(f)
        
        reminders = [n for n in notes if n.get("reminder", {}).get("enabled")]

        for r in reminders:
            card = QWidget()
            card_layout = QVBoxLayout(card)

            # Creating top row
            top_row = QHBoxLayout()
            note_btn = QPushButton(r['content'].splitlines()[0])
            note_btn.setStyleSheet(f"background-color: {r['color']}; border-radius: 6px;")
            note_btn.setFixedHeight(35)
            note_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            top_row.addWidget(note_btn)

            # Creating bottom row
            bottom_row = QHBoxLayout()
            time_btn = QPushButton(r['reminder']['datetime'])
            time_btn.setStyleSheet("""
                QPushButton {
                    background-color: #cbe4f9;
                    border-radius: 6px;
                    color: #333;
                }
                QPushButton:hover {
                    background-color: #e6e6e6;
                }
            """)
            delete_btn = QPushButton("X")
            delete_btn.setObjectName("delete")
            delete_btn.clicked.connect(lambda checked, nid=r["id"]: self.delete_reminder(nid))
            time_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            delete_btn.setFixedSize(40, 35)
            bottom_row.addWidget(time_btn, 2)
            bottom_row.addWidget(delete_btn, 1)

            card_layout.addLayout(top_row)
            card_layout.addLayout(bottom_row)
            self.scroll_layout.addWidget(card)
            self.scroll_layout.addSpacing(8)
    
    def delete_reminder(self, note_id):
        if not os.path.exists(self.file_path):
            return
        with open(self.file_path, 'r') as f:
            notes = json.load(f)

        updated = []
        for n in notes:
            if n["id"] == note_id:
                # Instead of deleting the note, disabling the reminder
                n["reminder"]["enabled"] = False
            updated.append(n)

        with open(self.file_path, "w") as f:
            json.dump(updated, f, indent=4)

        # Clear and reload the UI
        self.setUpdatesEnabled(False)
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.layout():
                while item.layout().count():
                    sub = item.layout().takeAt(0)
                    if sub.widget():
                        sub.widget().deleteLater()
                item.layout().deleteLater()
            elif item.widget():
                item.widget().deleteLater()
        self.load_reminders()
        self.setUpdatesEnabled(True)
        self.reminder_updated.emit()

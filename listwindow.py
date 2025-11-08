from PyQt6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QLabel, QScrollArea, QFrame, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
import json, os

class ListWindow(QWidget):
    def __init__(self, default_tab="list"):
        super().__init__()
        self.setWindowTitle("Notes & Reminders")
        

        layout = QVBoxLayout()
        self.tabs = QTabWidget()

        #making two blank tabs
        self.tab_notes = QWidget()
        self.tab_reminders = QWidget()

        self.tabs.addTab(self.tab_notes, "List")
        self.tabs.addTab(self.tab_reminders, "Reminders")

        # This is where to add the scrolable area

        layout.addWidget(self.tabs)
        self.setLayout(layout)

        # This will open the right tab

        if default_tab == "reminder":
            self.tabs.setCurrentIndex(1)
        else:
            self.tabs.setCurrentIndex(0)
        self.load_notes()

    def load_notes(self):

        if self.tab_notes.layout():
            old_layout = self.tab_notes.layout()
            while old_layout.count():
                child = old_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            QWidget().setLayout(old_layout) #detach old layout


        self.file_path = "notes.json"

        if not os.path.exists(self.file_path):
            return
        
        try:
            with open(self.file_path, 'r') as f:
                notes = json.load(f)
        except json.JSONDecodeError:
            notes = []
        
        #filter only notes without reminders
        simple_notes = [n for n in notes if not n["reminder"]["enabled"]]

        #This will make the scrollable area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        # Making container for all notes
        container = QWidget()
        vbox = QVBoxLayout(container)

        # Adding each note as a colored card
        for note in simple_notes:
            card = QFrame()
            card.setFrameShape(QFrame.Shape.StyledPanel)
            card.setStyleSheet(f"""
                background-color: {note['color']};
                border-radius: 8px;
                padding: 8px;
                margin-bottom: 6px;
            """)

            label = QLabel(note["content"])
            label.setWordWrap(True)
            label.setAlignment(Qt.AlignmentFlag.AlignTop)

            # delete button
            delete_btn = QPushButton("Delete")
            delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ffb3b3;
                    border: none;
                    padding: 4px 10px;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover { background-color: #ff8080; }
                QPushButton:pressed { background-color: #ff4d4d; }
            """)

            delete_btn.clicked.connect(lambda checked, nid=note["id"]: self.delete_note(nid))

            #layout text on left, button on right
            hbox = QHBoxLayout(card)
            hbox.addWidget(label)
            hbox.addStretch()
            hbox.addWidget(delete_btn)

            vbox.addWidget(card)
        
        # Finalizing scroll
        scroll.setWidget(container)

        # Putting scroll area insite tab

        tab_layout = QVBoxLayout()
        tab_layout.addWidget(scroll)
        self.tab_notes.setLayout(tab_layout)

    def delete_note(self, note_id):
        # Read JSON

        if not os.path.exists(self.file_path):
            return
        
        with open(self.file_path, 'r') as f:
            notes = json.load(f)
        
        # Keep everything except the one being deleted
        updated = [n for n in notes if n["id"] != note_id]

        # Save it back

        with open(self.file_path, "w") as f:
            json.dump(updated, f, indent=4)

        # Refresh UI
        self.load_notes()
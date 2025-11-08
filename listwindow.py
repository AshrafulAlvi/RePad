from addnote import NoteWindow
from PyQt6.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QLabel, QScrollArea, QFrame, QPushButton, QHBoxLayout, QSizePolicy
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
        simple_notes = [n for n in notes if not n.get("reminder", {}).get("enabled", False)]

        #This will make the scrollable area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Making container for all notes
        container = QWidget()
        vbox = QVBoxLayout(container)

        container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        vbox.setContentsMargins(8, 8, 8, 8)

        # Adding each note as a colored card
        for note in simple_notes:
            card = QPushButton()
            card.note_id = note["id"]
            card.clicked.connect(lambda checked, btn=card: self.open_note_window(btn.note_id))
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(6,6,6,6)
            card.setStyleSheet(f"""
                QPushButton {{
                    background-color: {note['color']};
                    border-radius: 8px;
                    border: none;
                    padding: 8px;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background-color: #d9e8f5;
                }}
            """)


            #creating set width size
            card.setMinimumHeight(40)
            card.setMinimumWidth(250)
            card.setMaximumWidth(250)
            card.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

            # Create a horizontal layout for each row
            row_layout = QHBoxLayout()
            row_layout.setSpacing(8)

            # Add the note to the left side
            row_layout.addWidget(card)

            # creating the delete button to the right side


            label = QLabel(note["content"])
            label.setText(note["content"].split('\n', 2)[0][:60] + "..." if len(note["content"]) > 60 else note["content"])
            #label.setText(note["content"][:120] + "..." if len(note["content"]) > 120 else note["content"])
            label.setWordWrap(True)
            label.setAlignment(Qt.AlignmentFlag.AlignTop)
            card_layout.addWidget(label)
            

            # delete button
            delete_btn = QPushButton("X")
            delete_btn.setFixedSize(40,40)
            delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ff944d;
                    border: none;
                    padding: 4px 10px;
                    border-radius: 5px;
                    color: white;
                    font-weight: bold;
                }
                QPushButton:hover { background-color: #ff7733; }
                QPushButton:pressed { background-color: #e65c00; }
            """)
            
            row_layout.addStretch()
            row_layout.addWidget(delete_btn, alignment=Qt.AlignmentFlag.AlignRight)

            delete_btn.clicked.connect(lambda checked, nid=note["id"]: self.delete_note(nid))

            vbox.addLayout(row_layout)
        
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
    
    def open_note_window(self, note_id):
        # Load all notes from file
        if not os.path.exists(self.file_path):
            return
        
        with open(self.file_path, 'r') as f:
            notes = json.load(f)
        
        # Find the matching note
        selected_note = next((n for n in notes if n["id"] == note_id), None)


        if not selected_note:
            print("note not found")
            return
        
        #Open notewindow in edit mode
        self.editor = NoteWindow(note_data=selected_note)
        self.editor.show()
        self.editor.note_saved.connect(self.load_notes)
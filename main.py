import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QPushButton
from PyQt6.QtGui import QIcon

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RePad")

        #This is to set up the window in users bottom right corner 
        window_width = 400
        window_height = 100

        # Get the current running QApplication instance
        app_instance = QApplication.instance()

        screen = app_instance.primaryScreen()  # getting the display
        geometry = screen.availableGeometry()  # get usable area without the taskbar

        screen_width = geometry.width()
        screen_height = geometry.height()

        margin = 10

        x = screen_width - window_width - margin
        y = screen_height - window_height - margin

        self.setGeometry(int(x), int(y), window_width, window_height)  # x, y, width, height
        self.setWindowIcon(QIcon('icon.png'))  # TODO Replace Icon later


        #This is for the buttons within the main window
        central_widget = QWidget() # Create horizontal layout
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout()
        layout.setSpacing(10)

        self.add_note = QPushButton("add") #add note button
        layout.addWidget(self.add_note) #adding the button to the layout
        central_widget.setLayout(layout)

        self.add_list = QPushButton("list") #add list button
        layout.addWidget(self.add_list) #adding the button to the layout
        central_widget.setLayout(layout)

        self.add_reminder = QPushButton("reminder") #add note button
        layout.addWidget(self.add_reminder) #adding the button to the layout
        central_widget.setLayout(layout)

        self.setStyleSheet("""
            QPushButton {
                height: 80px;
                width: 100px;
                border-radius: 6px;
                background-color: #cbe4f9;
                color: #222;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #a9d6f5;
            }
            QPushButton:pressed {
                background-color: #82c3f5;
            }
        """)
    
    def on_button_clicked(self):
        print("Button was clicked")
        self.add_note.setText("Clicked")


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create the application instance
    window = MyWindow()
    window.show()
    sys.exit(app.exec())

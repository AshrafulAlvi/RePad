from addnote import NoteWindow
from listwindow import ListWindow
from reminder import ReminderWatcher

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QPushButton, QSystemTrayIcon, QMenu
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
        self.setWindowIcon(QIcon('icon.png'))


        #This is for the buttons within the main window
        central_widget = QWidget() # Create horizontal layout
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout()
        layout.setSpacing(10)

        self.add_note = QPushButton("add") #add note button
        layout.addWidget(self.add_note) #adding the button to the layout
        central_widget.setLayout(layout)
        self.add_note.clicked.connect(self.open_new_window)

        self.add_list = QPushButton("list") #add list button
        layout.addWidget(self.add_list) 
        central_widget.setLayout(layout)
        self.add_list.clicked.connect(lambda: self.open_list_window("list"))

        self.add_reminder = QPushButton("reminder") #add reminder button
        layout.addWidget(self.add_reminder) 
        central_widget.setLayout(layout)
        self.add_reminder.clicked.connect(lambda: self.open_list_window("reminder"))

        
        #This CSS is for the main window on how the buttons looks
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

        #System Tray Setup
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))
        self.tray_icon.setToolTip("RePad - Notes & Reminders")
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        # Tray menu setup
        tray_menu = QMenu()

        # Add actions directly through the menu
        open_action = tray_menu.addAction("Open Repad")
        quit_action = tray_menu.addAction("Quit")

        # Connect them
        open_action.triggered.connect(self.restore_from_tray)
        quit_action.triggered.connect(QApplication.quit)

        # Attach the menu to the tray icon
        self.tray_icon.setContextMenu(tray_menu)
        
        # Start reminder watcher
        self.reminder_watcher = ReminderWatcher(self.tray_icon)
        self.reminder_watcher.start()


    
    def on_button_clicked(self):
        self.add_note.setText("Clicked")

    def open_new_window(self):
        self.new_window = NoteWindow()
        self.new_window.show()

    def open_list_window(self, default_tab):
        new_window_width = 400
        new_window_height = 250

        main_geo = self.geometry()
        x = main_geo.x()
        y = main_geo.y() - new_window_height - 10 # Above main window

        self.list_window = ListWindow(default_tab)
        self.list_window.setGeometry(x, y, new_window_width, new_window_height)
        self.list_window.show()

    def on_tray_icon_activated(self, reason):
        # Reopen main window when tray icon is clicked.
        if reason == QSystemTrayIcon.ActivationReason.Trigger: # Left-click
            self.showNormal()
            self.raise_()
            self.activateWindow()
    
    def restore_from_tray(self):
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def closeEvent(self, event):
        #Ensure tray icon is removed properly on close.
        self.tray_icon.hide()
        self.tray_icon.deleteLater()
        QApplication.quit()
        event.accept()

        


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create the application instance
    app.setQuitOnLastWindowClosed(False)
    app.setWindowIcon(QIcon("icon.png"))
    window = MyWindow()
    window.show()
    sys.exit(app.exec())

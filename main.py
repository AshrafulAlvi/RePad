import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RePad")

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


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create the application instance
    window = MyWindow()
    window.show()
    sys.exit(app.exec())

from PyQt6.QtCore import QObject, QTimer
from datetime import datetime
import json, os

class ReminderWatcher(QObject):
    def __init__(self, tray_icon, file_path="notes.json"):
        super().__init__()
        self.tray_icon = tray_icon
        self.file_path = file_path

        self.timer = QTimer(self)
        self.timer.setInterval(60000)
        self.timer.timeout.connect(self.check_reminders)

    def start(self):
        self.timer.start()

    def check_reminders(self):
        # stop if file doesn't exist
        if not os.path.exists(self.file_path):
            return

        try:
            with open(self.file_path, "r") as f:
                notes = json.load(f)
        except json.JSONDecodeError:
            return

        now = datetime.now()

        for note in notes:
            reminder = note.get("reminder", {})
            if reminder.get("enabled") and reminder.get("datetime"):
                try:
                    reminder_time = datetime.fromisoformat(reminder["datetime"])
                except ValueError:
                    continue

                if now >= reminder_time:
                    # show tray message
                    self.tray_icon.showMessage(
                        "RePad Reminder",
                        f"You have a reminder: {note['content'][:40]}...\nCheck the List tab for full view.",
                    )

                    # disable reminder
                    note["reminder"]["enabled"] = False

        # save updated JSON
        with open(self.file_path, "w") as f:
            json.dump(notes, f, indent=4)

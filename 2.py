import sys
from datetime import datetime
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox

class DiaryWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("2.ui", self)
        self.events = []  # список кортежей (datetime, text)
        self.btnAdd.clicked.connect(self.add_event)

    def add_event(self):
        text = self.editEvent.text().strip()
        if not text:
            QMessageBox.warning(self, "Ошибка", "Введите название события")
            return
        d = self.calendar.selectedDate().toPyDate()
        t = self.timeEdit.time().toPyTime()
        dt = datetime(d.year, d.month, d.day, t.hour, t.minute)
        self.events.append((dt, text))
        self.events.sort(key=lambda x: x[0])
        self.refresh()
        self.editEvent.clear()

    def refresh(self):
        self.listWidget.clear()
        for dt, text in self.events:
            self.listWidget.addItem(f"{dt.strftime('%d.%m.%Y %H:%M')} — {text}")

app = QApplication(sys.argv)
w = DiaryWindow()
w.show()
sys.exit(app.exec())

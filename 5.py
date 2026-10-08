import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QColor

class AntiPlagWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("5.ui", self)
        self.btnCheck.clicked.connect(self.check)

    def check(self):
        lines1 = [l.strip().lower() for l in self.text1.toPlainText().splitlines() if l.strip()]
        lines2 = [l.strip().lower() for l in self.text2.toPlainText().splitlines() if l.strip()]

        if not lines1 or not lines2:
            self.statusbar.setStyleSheet("color: orange;")
            self.statusbar.showMessage("Один из текстов пуст")
            return

        set2 = set(lines2)
        matches = sum(1 for l in lines1 if l in set2)
        percent = matches / len(lines1) * 100.0
        threshold = self.spinThreshold.value()

        msg = f"Совпадение: {percent:.1f}% (порог {threshold:.1f}%)"
        if percent >= threshold:
            self.statusbar.setStyleSheet("color: red; font-weight: bold;")
            self.statusbar.showMessage("ПЛАГИАТ! " + msg)
        else:
            self.statusbar.setStyleSheet("color: green; font-weight: bold;")
            self.statusbar.showMessage("Оригинально. " + msg)

app = QApplication(sys.argv)
w = AntiPlagWindow()
w.show()
sys.exit(app.exec())

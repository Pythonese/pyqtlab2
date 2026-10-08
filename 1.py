import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget, QButtonGroup

class FlagWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("1.ui", self)
        self.setFixedSize(self.size())  # запрет изменения размера

        # группируем радиокнопки по строкам
        self.groups = []
        for names in (("topRed","topGreen","topBlue","topWhite"),
                      ("midRed","midGreen","midBlue","midWhite"),
                      ("botRed","botGreen","botBlue","botWhite")):
            g = QButtonGroup(self)
            for n in names:
                g.addButton(getattr(self, n))
            self.groups.append(g)

        self.btnDraw.clicked.connect(self.draw)

    def _color(self, group):
        for b in group.buttons():
            if b.isChecked():
                return b.text()
        return "?"

    def draw(self):
        colors = [self._color(g) for g in self.groups]
        self.lblResult.setText(", ".join(colors))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = FlagWindow()
    w.show()
    sys.exit(app.exec())

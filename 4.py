import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox

class NimWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("4.ui", self)
        self.stones = 0
        self.game_over = True
        self.btnNewGame.clicked.connect(self.new_game)
        self.btnTake.clicked.connect(self.player_move)
        self.update_label()

    def new_game(self):
        self.stones = self.spinStones.value()
        self.game_over = False
        self.log.clear()
        self.log.append(f"Новая игра. Камней: {self.stones}. Ваш ход.")
        self.update_label()

    def update_label(self):
        self.lblStones.setText(f"Осталось камней: {self.stones}")

    def player_move(self):
        if self.game_over:
            QMessageBox.information(self, "Игра", "Начните новую игру")
            return
        take = self.spinTake.value()
        if take < 1 or take > 3:
            QMessageBox.warning(self, "Ошибка", "Можно взять 1–3 камня")
            return
        if take > self.stones:
            QMessageBox.warning(self, "Ошибка", "В куче меньше камней")
            return

        self.stones -= take
        self.log.append(f"Вы взяли {take}. Осталось {self.stones}.")
        self.update_label()

        if self.stones == 0:
            self.finish("Вы выиграли!")
            return
        self.ai_move()

    def ai_move(self):
        # выигрышная стратегия: оставить сопернику число, кратное 4
        take = self.stones % 4
        if take == 0:
            take = 1
        take = min(take, 3, self.stones)
        self.stones -= take
        self.log.append(f"Компьютер взял {take}. Осталось {self.stones}.")
        self.update_label()
        if self.stones == 0:
            self.finish("Компьютер выиграл!")

    def finish(self, msg):
        self.game_over = True
        self.log.append(msg)
        QMessageBox.information(self, "Игра окончена", msg)

app = QApplication(sys.argv)
w = NimWindow()
w.show()
sys.exit(app.exec())

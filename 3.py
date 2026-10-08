import re
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox

# Разрешённые форматы:
#   +7XXXXXXXXXX        +79991234567
#   8XXXXXXXXXX         89991234567
#   7XXXXXXXXXX         79991234567
#   с любыми разделителями (пробел, дефис, скобки) между цифрами
PHONE_RE = re.compile(
    r"^\s*(?:\+?7|8)\s*[\(\-]?\s*\d{3}\s*[\)\-]?\s*\d{3}\s*[\-]?\s*\d{2}\s*[\-]?\s*\d{2}\s*$"
)


def normalize_phone(raw: str) -> str:
    """Приводит номер к виду +7XXXXXXXXXX."""
    digits = re.sub(r"\D", "", raw)
    if digits.startswith("8"):
        digits = "7" + digits[1:]
    elif digits.startswith("7"):
        pass
    else:
        digits = "7" + digits
    return "+" + digits


class PhoneBookWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("3.ui", self)
        self.btnAdd.clicked.connect(self.add_contact)
        self.contacts = {}  # нормализованный номер -> имя

    def add_contact(self):
        name = self.editName.text().strip()
        phone_raw = self.editPhone.text().strip()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите имя контакта")
            self.editName.setFocus()
            return

        if not phone_raw:
            QMessageBox.warning(self, "Ошибка", "Введите номер телефона")
            self.editPhone.setFocus()
            return

        if not PHONE_RE.match(phone_raw):
            QMessageBox.warning(
                self, "Ошибка",
                "Неверный формат номера.\n"
                "Допустимые примеры:\n"
                "  +7 (999) 123-45-67\n"
                "  89991234567\n"
                "  7-999-123-45-67"
            )
            self.editPhone.setFocus()
            self.editPhone.selectAll()
            return

        phone = normalize_phone(phone_raw)

        if phone in self.contacts:
            QMessageBox.warning(
                self, "Ошибка",
                f"Номер {phone} уже есть в книжке (контакт: {self.contacts[phone]})"
            )
            return

        self.contacts[phone] = name
        self.listWidget.addItem(f"{name}: {phone}")

        self.editName.clear()
        self.editPhone.clear()
        self.editName.setFocus()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PhoneBookWindow()
    w.show()
    sys.exit(app.exec())

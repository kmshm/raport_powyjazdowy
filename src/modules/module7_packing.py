"""
Module 7 — Packing List.
Dynamic list of items to bring on the trip.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QLabel
)
from PyQt6.QtCore import Qt

from src.modules.base_module import BaseModule
from src.theme import TEXT_SEC, FONT_SIZE_SM

DEFAULT_ITEMS = [
    "Laptop / komputer",
    "Kable światłowodowe",
    "Złącza i narzędzia do światłowodów",
    "Drabina",
    "Namiot / plandeka",
    "Nagrzewnica",
    "Kalosze / buty robocze",
    "Kask ochronny",
    "Kamizelka odblaskowa",
    "Apteczka",
]


class PackingItem(QWidget):
    def __init__(self, text: str, on_remove, parent=None):
        super().__init__(parent)
        self._on_remove = on_remove
        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(6)

        bullet = QLabel("•")
        bullet.setStyleSheet(f"color: {TEXT_SEC}; font-size: {FONT_SIZE_SM}pt;")
        bullet.setFixedWidth(12)
        row.addWidget(bullet)

        self.edit = QLineEdit(text)
        self.edit.setPlaceholderText("Pozycja na liście…")
        row.addWidget(self.edit, 1)

        rm_btn = QPushButton("✕")
        rm_btn.setFixedSize(24, 24)
        rm_btn.setStyleSheet(
            "QPushButton { background: #FEE2E2; color: #DC2626; "
            "border: 1px solid #FECACA; border-radius: 4px; font-weight: 700;}"
            "QPushButton:hover { background: #FCA5A5; }"
        )
        rm_btn.clicked.connect(lambda: self._on_remove(self))
        row.addWidget(rm_btn)

    def text(self) -> str:
        return self.edit.text().strip()


class Module7Packing(BaseModule):
    MODULE_ID = 7
    MODULE_TITLE = "Lista Rzeczy do Zabrania"

    def _build_content(self, container: QWidget):
        layout = container.layout()
        self._items: list[PackingItem] = []
        self._container = QVBoxLayout()
        self._container.setSpacing(4)
        layout.addLayout(self._container)

        for text in DEFAULT_ITEMS:
            self._add_item(text)

        add_btn = QPushButton("+ Dodaj pozycję")
        add_btn.setObjectName("small")
        add_btn.setMaximumWidth(160)
        add_btn.clicked.connect(lambda: self._add_item(""))
        layout.addWidget(add_btn)

    def _add_item(self, text: str):
        item = PackingItem(text, self._remove_item)
        self._items.append(item)
        self._container.addWidget(item)

    def _remove_item(self, item: PackingItem):
        if item in self._items:
            self._items.remove(item)
        item.deleteLater()

    def get_data(self) -> dict:
        return {"items": [i.text() for i in self._items if i.text()]}

    def set_data(self, data: dict):
        for item in list(self._items):
            item.deleteLater()
        self._items.clear()
        for text in data.get("items", []):
            self._add_item(text)
        if not self._items:
            for text in DEFAULT_ITEMS:
                self._add_item(text)

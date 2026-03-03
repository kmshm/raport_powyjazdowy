"""
Module 8 — General Notes.
Free text + optional images.
"""
from PyQt6.QtWidgets import QWidget, QTextEdit
from src.modules.base_module import BaseModule
from src.modules.module6_measurements import ImageListWidget


class Module8Notes(BaseModule):
    MODULE_ID = 8
    MODULE_TITLE = "Uwagi"

    def _build_content(self, container: QWidget):
        layout = container.layout()

        self.notes = QTextEdit()
        self.notes.setPlaceholderText("Uwagi ogólne…")
        self.notes.setFixedHeight(120)
        layout.addLayout(self.field_row("Uwagi", self.notes))

        self.images = ImageListWidget()
        layout.addWidget(self.images)

    def get_data(self) -> dict:
        return {
            "notes":  self.notes.toPlainText().strip(),
            "images": self.images.get_paths(),
        }

    def set_data(self, data: dict):
        self.notes.setPlainText(data.get("notes", ""))
        self.images.set_paths(data.get("images", []))

"""
Module 9 — Logistics and Organisation.
Text fields: parking, site location, accommodation, other.
"""
from PyQt6.QtWidgets import QWidget, QTextEdit
from src.modules.base_module import BaseModule


class Module9Logistics(BaseModule):
    MODULE_ID = 9
    MODULE_TITLE = "Logistyka i Organizacja"

    def _build_content(self, container: QWidget):
        layout = container.layout()

        self.parking = QTextEdit()
        self.parking.setPlaceholderText("Informacje o parkowaniu…")
        self.parking.setFixedHeight(70)
        layout.addLayout(self.field_row("Parkowanie samochodu", self.parking))

        self.site_location = QTextEdit()
        self.site_location.setPlaceholderText("Lokalizacja miejsca pomiarów, dojście, klucze…")
        self.site_location.setFixedHeight(70)
        layout.addLayout(self.field_row("Lokalizacja miejsca pomiarów", self.site_location))

        self.accommodation = QTextEdit()
        self.accommodation.setPlaceholderText("Informacje o noclegu, rezerwacje…")
        self.accommodation.setFixedHeight(70)
        layout.addLayout(self.field_row("Nocleg", self.accommodation))

        self.other = QTextEdit()
        self.other.setPlaceholderText("Inne informacje organizacyjne…")
        self.other.setFixedHeight(70)
        layout.addLayout(self.field_row("Inne", self.other))

    def get_data(self) -> dict:
        return {
            "parking":       self.parking.toPlainText().strip(),
            "site_location": self.site_location.toPlainText().strip(),
            "accommodation": self.accommodation.toPlainText().strip(),
            "other":         self.other.toPlainText().strip(),
        }

    def set_data(self, data: dict):
        self.parking.setPlainText(data.get("parking", ""))
        self.site_location.setPlainText(data.get("site_location", ""))
        self.accommodation.setPlainText(data.get("accommodation", ""))
        self.other.setPlainText(data.get("other", ""))

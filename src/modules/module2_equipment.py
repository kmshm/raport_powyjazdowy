"""
Module 2 — Measurement Equipment.
Optical recorders (predefined checklist + custom) and other devices.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QLineEdit,
    QPushButton, QLabel, QFrame
)
from PyQt6.QtCore import Qt

from src.modules.base_module import BaseModule
from src.theme import BORDER, TEXT_SEC, FONT_SIZE_SM

OPTICAL_RECORDERS = [
    "Interrogator ODISI-B (Luna Innovations)",
    "Interrogator si155 (Micron Optics)",
    "Interrogator sm130 (Micron Optics)",
    "Interrogator SpectraQuest (HBK)",
    "Interrogator DiTeSt STA-R (Omnisens)",
    "Analizator widma OSA",
    "Reflektometr OTDR",
]

OTHER_DEVICES = [
    "Laptop / komputer pomiarowy",
    "Zasilacz UPS",
    "Przedłużacz / listwa zasilająca",
    "Śrubokręt elektryczny",
    "Kamera / aparat fotograficzny",
    "Stacja bazowa GPS",
    "Multimetr",
]


class ChecklistGroup(QWidget):
    """A vertical list of checkboxes with a 'custom item' field."""

    def __init__(self, items: list[str], parent=None):
        super().__init__(parent)
        self._checks: dict[str, QCheckBox] = {}
        self._custom_edits: list[QLineEdit] = []
        self._setup(items)

    def _setup(self, items: list[str]):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        for item in items:
            cb = QCheckBox(item)
            self._checks[item] = cb
            layout.addWidget(cb)

        # ── custom entries ────────────────────────────────────────────────────
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {BORDER}; background: {BORDER}; margin: 4px 0;")
        layout.addWidget(sep)

        self._custom_container = QVBoxLayout()
        self._custom_container.setSpacing(4)
        layout.addLayout(self._custom_container)

        add_btn = QPushButton("+ Dodaj własny sprzęt")
        add_btn.setObjectName("small")
        add_btn.setMaximumWidth(180)
        # Use lambda to avoid clicked(bool) being passed as text argument
        add_btn.clicked.connect(lambda: self._add_custom(""))
        layout.addWidget(add_btn)

    def _add_custom(self, text: str = ""):
        row = QHBoxLayout()
        edit = QLineEdit()
        edit.setPlaceholderText("Nazwa sprzętu...")
        if isinstance(text, str):
            edit.setText(text)
        self._custom_edits.append(edit)
        row.addWidget(edit)

        rm = QPushButton("Usuń")
        rm.setObjectName("small")
        rm.setMinimumWidth(50)
        rm.setStyleSheet(
            "QPushButton { background: #FDECEA; color: #C41920; "
            "border: 1px solid #F5C6C5; border-radius: 4px; padding: 2px 8px;}"
            "QPushButton:hover { background: #FAD4D2; }"
        )
        rm.clicked.connect(lambda: self._remove_custom(edit, row))
        row.addWidget(rm)
        row.addStretch()
        self._custom_container.addLayout(row)

    def _remove_custom(self, edit: QLineEdit, row: QHBoxLayout):
        if edit in self._custom_edits:
            self._custom_edits.remove(edit)
        # Remove all widgets from the row
        while row.count():
            item = row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def get_data(self) -> dict:
        checked = [name for name, cb in self._checks.items() if cb.isChecked()]
        custom = [e.text().strip() for e in self._custom_edits if e.text().strip()]
        return {"checked": checked, "custom": custom}

    def set_data(self, data: dict):
        checked = data.get("checked", [])
        for name, cb in self._checks.items():
            cb.setChecked(name in checked)
        # Clear existing custom
        for e in list(self._custom_edits):
            e.deleteLater()
        self._custom_edits.clear()
        for text in data.get("custom", []):
            self._add_custom(text)


class Module2Equipment(BaseModule):
    MODULE_ID = 2
    MODULE_TITLE = "Sprzęt Pomiarowy"

    def _build_content(self, container: QWidget):
        layout = container.layout()

        lbl_opt = QLabel("Rejestratory optyczne")
        lbl_opt.setStyleSheet(
            f"font-weight: 600; font-size: {FONT_SIZE_SM + 1}pt; color: #374151;"
        )
        layout.addWidget(lbl_opt)

        self.optical = ChecklistGroup(OPTICAL_RECORDERS)
        layout.addWidget(self.optical)

        # Divider
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {BORDER}; background: {BORDER}; margin: 4px 0;")
        layout.addWidget(sep)

        lbl_other = QLabel("Inne urządzenia")
        lbl_other.setStyleSheet(
            f"font-weight: 600; font-size: {FONT_SIZE_SM + 1}pt; color: #374151;"
        )
        layout.addWidget(lbl_other)

        self.other = ChecklistGroup(OTHER_DEVICES)
        layout.addWidget(self.other)

    def get_data(self) -> dict:
        return {
            "optical_recorders": self.optical.get_data(),
            "other_devices":     self.other.get_data(),
        }

    def set_data(self, data: dict):
        self.optical.set_data(data.get("optical_recorders", {}))
        self.other.set_data(data.get("other_devices", {}))

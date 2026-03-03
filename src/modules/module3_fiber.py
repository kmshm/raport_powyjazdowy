"""
Module 3 — Fiber Optic Sensors.
Dynamic list: Name, Serial, Notes, Image.
"""
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit,
    QPushButton, QLabel, QFrame, QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from src.modules.base_module import BaseModule
from src.theme import BORDER, BG_INPUT, TEXT_SEC, FONT_SIZE_SM, PRIMARY


class SensorRow(QWidget):
    """Single fiber sensor entry row."""

    def __init__(self, index: int, on_remove, parent=None):
        super().__init__(parent)
        self._image_path: str = ""
        self._on_remove = on_remove
        self._index = index
        self._setup()

    def _setup(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(6)

        # Row number + remove button header
        header = QHBoxLayout()
        num_lbl = QLabel(f"Czujnik #{self._index + 1}")
        num_lbl.setStyleSheet(
            f"font-weight: 600; font-size: {FONT_SIZE_SM}pt; color: {TEXT_SEC};"
        )
        header.addWidget(num_lbl)
        header.addStretch()
        rm_btn = QPushButton("Usuń")
        rm_btn.setObjectName("small")
        rm_btn.setStyleSheet(
            "QPushButton { background: #FEE2E2; color: #DC2626; "
            "border: 1px solid #FECACA; border-radius: 4px; padding: 2px 8px;}"
            "QPushButton:hover { background: #FCA5A5; }"
        )
        rm_btn.clicked.connect(lambda: self._on_remove(self))
        header.addWidget(rm_btn)
        outer.addLayout(header)

        # Fields row
        fields = QHBoxLayout()
        fields.setSpacing(10)

        self.name = QLineEdit()
        self.name.setPlaceholderText("Nazwa czujnika")
        name_vb = QVBoxLayout()
        name_vb.setSpacing(2)
        name_vb.addWidget(QLabel("Nazwa"))
        name_vb.addWidget(self.name)
        fields.addLayout(name_vb, 2)

        self.serial = QLineEdit()
        self.serial.setPlaceholderText("Nr seryjny")
        serial_vb = QVBoxLayout()
        serial_vb.setSpacing(2)
        serial_vb.addWidget(QLabel("Nr seryjny"))
        serial_vb.addWidget(self.serial)
        fields.addLayout(serial_vb, 2)

        self.notes = QLineEdit()
        self.notes.setPlaceholderText("Uwagi")
        notes_vb = QVBoxLayout()
        notes_vb.setSpacing(2)
        notes_vb.addWidget(QLabel("Uwagi"))
        notes_vb.addWidget(self.notes)
        fields.addLayout(notes_vb, 3)

        # Image picker
        img_vb = QVBoxLayout()
        img_vb.setSpacing(2)
        img_vb.addWidget(QLabel("Zdjęcie/rysunek"))
        img_btn_row = QHBoxLayout()
        self._img_btn = QPushButton("Wybierz…")
        self._img_btn.setObjectName("small")
        self._img_btn.clicked.connect(self._pick_image)
        img_btn_row.addWidget(self._img_btn)
        self._img_preview = QLabel()
        self._img_preview.setFixedSize(48, 36)
        self._img_preview.setStyleSheet(
            f"background: {BG_INPUT}; border: 1px solid {BORDER}; border-radius: 4px;"
        )
        self._img_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img_btn_row.addWidget(self._img_preview)
        img_btn_row.addStretch()
        img_vb.addLayout(img_btn_row)
        fields.addLayout(img_vb, 2)

        outer.addLayout(fields)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {BORDER}; background: {BORDER}; margin-top: 4px;")
        outer.addWidget(sep)

    def _pick_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Wybierz zdjęcie", "",
            "Obrazy (*.png *.jpg *.jpeg *.bmp *.tiff *.svg)"
        )
        if path:
            self._image_path = path
            px = QPixmap(path).scaled(
                48, 36,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self._img_preview.setPixmap(px)
            self._img_btn.setText("Zmień…")

    def get_data(self) -> dict:
        return {
            "name":       self.name.text().strip(),
            "serial":     self.serial.text().strip(),
            "notes":      self.notes.text().strip(),
            "image_path": self._image_path,
        }

    def set_data(self, data: dict):
        self.name.setText(data.get("name", ""))
        self.serial.setText(data.get("serial", ""))
        self.notes.setText(data.get("notes", ""))
        img = data.get("image_path", "")
        if img and os.path.exists(img):
            self._image_path = img
            px = QPixmap(img).scaled(48, 36,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation)
            self._img_preview.setPixmap(px)
            self._img_btn.setText("Zmień…")


class Module3Fiber(BaseModule):
    MODULE_ID = 3
    MODULE_TITLE = "Czujniki Światłowodowe"

    def _build_content(self, container: QWidget):
        layout = container.layout()
        self._rows: list[SensorRow] = []
        self._rows_container = QVBoxLayout()
        self._rows_container.setSpacing(4)
        layout.addLayout(self._rows_container)

        add_btn = QPushButton("+ Dodaj czujnik")
        add_btn.setObjectName("small")
        add_btn.setMaximumWidth(160)
        add_btn.clicked.connect(self._add_row)
        layout.addWidget(add_btn)

        self._add_row()  # start with one empty row

    def _add_row(self, data: dict | None = None):
        row = SensorRow(len(self._rows), self._remove_row)
        if data:
            row.set_data(data)
        self._rows.append(row)
        self._rows_container.addWidget(row)

    def _remove_row(self, row: SensorRow):
        if row in self._rows:
            self._rows.remove(row)
        row.deleteLater()

    def get_data(self) -> dict:
        return {"sensors": [r.get_data() for r in self._rows]}

    def set_data(self, data: dict):
        for r in list(self._rows):
            r.deleteLater()
        self._rows.clear()
        for s in data.get("sensors", []):
            self._add_row(s)
        if not self._rows:
            self._add_row()

"""
Module 4 — Other Sensors.
Dynamic list: Name, Serial, Type, Notes, Image.
"""
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QLabel, QFrame, QFileDialog, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from src.modules.base_module import BaseModule
from src.theme import BORDER, BG_INPUT, TEXT_SEC, FONT_SIZE_SM

SENSOR_TYPES = [
    "Inklinometr",
    "Tensometr elektrooporowy",
    "Akcelerometr",
    "Przetwornik ciśnienia",
    "Czujnik temperatury",
    "Czujnik wilgotności",
    "Czujnik przemieszczenia (LVDT)",
    "Czujnik siły",
    "Extensometr",
    "Inny",
]


class OtherSensorRow(QWidget):
    def __init__(self, index: int, on_remove, parent=None):
        super().__init__(parent)
        self._image_path = ""
        self._on_remove = on_remove
        self._index = index
        self._setup()

    def _setup(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(6)

        header = QHBoxLayout()
        lbl = QLabel(f"Czujnik #{self._index + 1}")
        lbl.setStyleSheet(f"font-weight: 600; font-size: {FONT_SIZE_SM}pt; color: {TEXT_SEC};")
        header.addWidget(lbl)
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

        fields = QHBoxLayout()
        fields.setSpacing(10)

        self.name = QLineEdit()
        self.name.setPlaceholderText("Nazwa czujnika")
        nv = QVBoxLayout(); nv.setSpacing(2)
        nv.addWidget(QLabel("Nazwa")); nv.addWidget(self.name)
        fields.addLayout(nv, 2)

        self.serial = QLineEdit()
        self.serial.setPlaceholderText("Nr seryjny")
        sv = QVBoxLayout(); sv.setSpacing(2)
        sv.addWidget(QLabel("Nr seryjny")); sv.addWidget(self.serial)
        fields.addLayout(sv, 2)

        self.sensor_type = QComboBox()
        self.sensor_type.addItems(SENSOR_TYPES)
        tv = QVBoxLayout(); tv.setSpacing(2)
        tv.addWidget(QLabel("Rodzaj")); tv.addWidget(self.sensor_type)
        fields.addLayout(tv, 2)

        self.notes = QLineEdit()
        self.notes.setPlaceholderText("Uwagi")
        notesv = QVBoxLayout(); notesv.setSpacing(2)
        notesv.addWidget(QLabel("Uwagi")); notesv.addWidget(self.notes)
        fields.addLayout(notesv, 3)

        # Image
        imgv = QVBoxLayout(); imgv.setSpacing(2)
        imgv.addWidget(QLabel("Zdjęcie"))
        img_row = QHBoxLayout()
        self._img_btn = QPushButton("Wybierz…")
        self._img_btn.setObjectName("small")
        self._img_btn.clicked.connect(self._pick_image)
        img_row.addWidget(self._img_btn)
        self._img_preview = QLabel()
        self._img_preview.setFixedSize(48, 36)
        self._img_preview.setStyleSheet(
            f"background: {BG_INPUT}; border: 1px solid {BORDER}; border-radius: 4px;"
        )
        self._img_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img_row.addWidget(self._img_preview)
        img_row.addStretch()
        imgv.addLayout(img_row)
        fields.addLayout(imgv, 2)

        outer.addLayout(fields)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {BORDER}; background: {BORDER}; margin-top: 4px;")
        outer.addWidget(sep)

    def _pick_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Wybierz zdjecie", "",
            "Obrazy (*.png *.jpg *.jpeg *.bmp *.tiff)",
            options=QFileDialog.Option.DontUseNativeDialog,
        )
        if path:
            self._image_path = path
            px = QPixmap(path).scaled(48, 36,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation)
            self._img_preview.setPixmap(px)
            self._img_btn.setText("Zmień…")

    def get_data(self) -> dict:
        return {
            "name":         self.name.text().strip(),
            "serial":       self.serial.text().strip(),
            "sensor_type":  self.sensor_type.currentText(),
            "notes":        self.notes.text().strip(),
            "image_path":   self._image_path,
        }

    def set_data(self, data: dict):
        self.name.setText(data.get("name", ""))
        self.serial.setText(data.get("serial", ""))
        idx = self.sensor_type.findText(data.get("sensor_type", ""))
        if idx >= 0:
            self.sensor_type.setCurrentIndex(idx)
        self.notes.setText(data.get("notes", ""))
        img = data.get("image_path", "")
        if img and os.path.exists(img):
            self._image_path = img
            px = QPixmap(img).scaled(48, 36,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation)
            self._img_preview.setPixmap(px)
            self._img_btn.setText("Zmień…")


class Module4Sensors(BaseModule):
    MODULE_ID = 4
    MODULE_TITLE = "Czujniki Inne"

    def _build_content(self, container: QWidget):
        layout = container.layout()
        self._rows: list[OtherSensorRow] = []
        self._rows_container = QVBoxLayout()
        self._rows_container.setSpacing(4)
        layout.addLayout(self._rows_container)

        add_btn = QPushButton("+ Dodaj czujnik")
        add_btn.setObjectName("small")
        add_btn.setMaximumWidth(160)
        add_btn.clicked.connect(self._add_row)
        layout.addWidget(add_btn)

        self._add_row()

    def _add_row(self, data: dict | None = None):
        row = OtherSensorRow(len(self._rows), self._remove_row)
        if data:
            row.set_data(data)
        self._rows.append(row)
        self._rows_container.addWidget(row)

    def _remove_row(self, row: OtherSensorRow):
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

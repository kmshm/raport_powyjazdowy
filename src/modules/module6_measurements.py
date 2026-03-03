"""
Module 6 — Measurement Progress.
  - Description text + images
  - Schedule table (stage, duration) — dynamic
  - Problems text + images
"""
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit,
    QPushButton, QLabel, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QFileDialog
)
from PyQt6.QtCore import Qt

from src.modules.base_module import BaseModule
from src.theme import BORDER, TEXT_SEC, FONT_SIZE_SM, BG_INPUT


class ImageListWidget(QWidget):
    """Compact list of attached image paths with add/remove."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._paths: list[str] = []
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self._list_layout = QVBoxLayout()
        self._list_layout.setSpacing(2)
        layout.addLayout(self._list_layout)

        add_btn = QPushButton("+ Dodaj zdjęcie")
        add_btn.setObjectName("small")
        add_btn.setMaximumWidth(150)
        add_btn.clicked.connect(self._add_image)
        layout.addWidget(add_btn)

    def _add_image(self, path: str = ""):
        if not path:
            path, _ = QFileDialog.getOpenFileName(
                self, "Wybierz zdjęcie", "",
                "Obrazy (*.png *.jpg *.jpeg *.bmp *.tiff)"
            )
        if not path:
            return
        self._paths.append(path)
        row = QHBoxLayout()
        lbl = QLabel(f"✓ {os.path.basename(path)}")
        lbl.setStyleSheet(f"color: #0E9F6E; font-size: {FONT_SIZE_SM}pt;")
        lbl.setToolTip(path)
        rm = QPushButton("✕")
        rm.setObjectName("small")
        rm.setFixedSize(22, 22)
        rm.setStyleSheet(
            "QPushButton { background: #FEE2E2; color: #DC2626; "
            "border: 1px solid #FECACA; border-radius: 3px; font-weight:700;}"
        )
        rm.clicked.connect(lambda _, p=path, r=row, l=lbl, rb=rm: self._remove(p, r))
        row.addWidget(lbl)
        row.addWidget(rm)
        row.addStretch()
        self._list_layout.addLayout(row)

    def _remove(self, path: str, row: QHBoxLayout):
        if path in self._paths:
            self._paths.remove(path)
        while row.count():
            item = row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def get_paths(self) -> list[str]:
        return list(self._paths)

    def set_paths(self, paths: list[str]):
        self._paths.clear()
        # Clear existing rows in list_layout
        while self._list_layout.count():
            item = self._list_layout.takeAt(0)
            if item.layout():
                while item.layout().count():
                    sub = item.layout().takeAt(0)
                    if sub.widget():
                        sub.widget().deleteLater()
        for p in paths:
            if os.path.exists(p):
                self._add_image(p)


class Module6Measurements(BaseModule):
    MODULE_ID = 6
    MODULE_TITLE = "Przebieg Pomiarów"

    def _build_content(self, container: QWidget):
        layout = container.layout()

        # ── Measurement description ───────────────────────────────────────────
        self.description = QTextEdit()
        self.description.setPlaceholderText("Opis sposobu prowadzenia pomiarów…")
        self.description.setFixedHeight(100)
        layout.addLayout(self.field_row("Opis sposobu prowadzenia pomiarów", self.description))

        self.desc_images = ImageListWidget()
        layout.addWidget(self.desc_images)

        sep1 = QFrame(); sep1.setFrameShape(QFrame.Shape.HLine)
        sep1.setStyleSheet(f"color: {BORDER}; background: {BORDER}; margin: 6px 0;")
        layout.addWidget(sep1)

        # ── Schedule ──────────────────────────────────────────────────────────
        sched_hdr = QHBoxLayout()
        sched_lbl = QLabel("Harmonogram pomiarów")
        sched_lbl.setStyleSheet(f"font-weight: 600; font-size: {FONT_SIZE_SM+1}pt;")
        sched_hdr.addWidget(sched_lbl)
        sched_hdr.addStretch()
        add_stage_btn = QPushButton("+ Etap")
        add_stage_btn.setObjectName("small")
        add_stage_btn.clicked.connect(self._add_stage)
        sched_hdr.addWidget(add_stage_btn)
        rm_stage_btn = QPushButton("− Etap")
        rm_stage_btn.setObjectName("small")
        rm_stage_btn.clicked.connect(self._remove_stage)
        sched_hdr.addWidget(rm_stage_btn)
        layout.addLayout(sched_hdr)

        self._schedule = QTableWidget(0, 2)
        self._schedule.setHorizontalHeaderLabels(["Etap / Opis", "Czas trwania"])
        self._schedule.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self._schedule.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Fixed
        )
        self._schedule.setColumnWidth(1, 160)
        self._schedule.setMinimumHeight(120)
        layout.addWidget(self._schedule)
        self._add_stage()  # start with one row

        sep2 = QFrame(); sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet(f"color: {BORDER}; background: {BORDER}; margin: 6px 0;")
        layout.addWidget(sep2)

        # ── Problems ──────────────────────────────────────────────────────────
        self.problems = QTextEdit()
        self.problems.setPlaceholderText("Opis problemów napotkanych w trakcie pomiarów…")
        self.problems.setFixedHeight(90)
        layout.addLayout(self.field_row("Problemy w trakcie pomiarów", self.problems))

        self.prob_images = ImageListWidget()
        layout.addWidget(self.prob_images)

    # ── Schedule helpers ──────────────────────────────────────────────────────

    def _add_stage(self):
        row = self._schedule.rowCount()
        self._schedule.insertRow(row)
        self._schedule.setItem(row, 0, QTableWidgetItem(""))
        self._schedule.setItem(row, 1, QTableWidgetItem(""))

    def _remove_stage(self):
        row = self._schedule.currentRow()
        if row >= 0:
            self._schedule.removeRow(row)
        elif self._schedule.rowCount() > 0:
            self._schedule.removeRow(self._schedule.rowCount() - 1)

    # ── Data interface ────────────────────────────────────────────────────────

    def get_data(self) -> dict:
        schedule = []
        for r in range(self._schedule.rowCount()):
            stage = (self._schedule.item(r, 0).text()
                     if self._schedule.item(r, 0) else "")
            duration = (self._schedule.item(r, 1).text()
                        if self._schedule.item(r, 1) else "")
            if stage or duration:
                schedule.append({"stage": stage, "duration": duration})
        return {
            "description":    self.description.toPlainText().strip(),
            "desc_images":    self.desc_images.get_paths(),
            "schedule":       schedule,
            "problems":       self.problems.toPlainText().strip(),
            "prob_images":    self.prob_images.get_paths(),
        }

    def set_data(self, data: dict):
        self.description.setPlainText(data.get("description", ""))
        self.desc_images.set_paths(data.get("desc_images", []))

        schedule = data.get("schedule", [])
        self._schedule.setRowCount(0)
        for item in schedule:
            self._add_stage()
            r = self._schedule.rowCount() - 1
            self._schedule.setItem(r, 0, QTableWidgetItem(item.get("stage", "")))
            self._schedule.setItem(r, 1, QTableWidgetItem(item.get("duration", "")))
        if self._schedule.rowCount() == 0:
            self._add_stage()

        self.problems.setPlainText(data.get("problems", ""))
        self.prob_images.set_paths(data.get("prob_images", []))

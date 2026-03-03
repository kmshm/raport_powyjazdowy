"""
Module 5 — Inventory.
Configurable table (add/remove rows and columns), optional description, optional image.
"""
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit,
    QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QFileDialog, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from src.modules.base_module import BaseModule
from src.theme import BORDER, BG_INPUT, TEXT_SEC, FONT_SIZE_SM


class Module5Inventory(BaseModule):
    MODULE_ID = 5
    MODULE_TITLE = "Inwentaryzacja"

    def _build_content(self, container: QWidget):
        layout = container.layout()

        # ── Toolbar: add/remove rows and columns ──────────────────────────────
        toolbar = QHBoxLayout()
        toolbar.setSpacing(6)

        add_row_btn = QPushButton("+ Wiersz")
        add_row_btn.setObjectName("small")
        add_row_btn.clicked.connect(self._add_row)
        toolbar.addWidget(add_row_btn)

        rm_row_btn = QPushButton("− Wiersz")
        rm_row_btn.setObjectName("small")
        rm_row_btn.clicked.connect(self._remove_row)
        toolbar.addWidget(rm_row_btn)

        add_col_btn = QPushButton("+ Kolumna")
        add_col_btn.setObjectName("small")
        add_col_btn.clicked.connect(self._add_col)
        toolbar.addWidget(add_col_btn)

        rm_col_btn = QPushButton("− Kolumna")
        rm_col_btn.setObjectName("small")
        rm_col_btn.clicked.connect(self._remove_col)
        toolbar.addWidget(rm_col_btn)

        toolbar.addStretch()
        layout.addLayout(toolbar)

        # ── Table ─────────────────────────────────────────────────────────────
        self._table = QTableWidget(3, 3)
        self._table.setHorizontalHeaderLabels(["Kolumna 1", "Kolumna 2", "Kolumna 3"])
        self._table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self._table.setMinimumHeight(160)
        layout.addWidget(self._table)

        # ── Description ───────────────────────────────────────────────────────
        self.description = QTextEdit()
        self.description.setPlaceholderText("Opis inwentaryzacji (opcjonalny)…")
        self.description.setFixedHeight(80)
        layout.addLayout(self.field_row("Opis", self.description))

        # ── Image ─────────────────────────────────────────────────────────────
        self._image_path = ""
        img_row = QHBoxLayout()
        img_btn = QPushButton("Dodaj zdjęcie/rysunek")
        img_btn.setObjectName("small")
        img_btn.clicked.connect(self._pick_image)
        img_row.addWidget(img_btn)
        self._img_label = QLabel("Brak zdjęcia")
        self._img_label.setStyleSheet(f"color: {TEXT_SEC}; font-size: {FONT_SIZE_SM}pt;")
        img_row.addWidget(self._img_label)
        img_row.addStretch()
        layout.addLayout(img_row)

    # ── Table management ──────────────────────────────────────────────────────

    def _add_row(self):
        self._table.insertRow(self._table.rowCount())

    def _remove_row(self):
        row = self._table.currentRow()
        if row >= 0:
            self._table.removeRow(row)
        elif self._table.rowCount() > 1:
            self._table.removeRow(self._table.rowCount() - 1)

    def _add_col(self):
        col = self._table.columnCount()
        self._table.insertColumn(col)
        self._table.setHorizontalHeaderItem(
            col, QTableWidgetItem(f"Kolumna {col + 1}")
        )

    def _remove_col(self):
        col = self._table.currentColumn()
        if col >= 0:
            self._table.removeColumn(col)
        elif self._table.columnCount() > 1:
            self._table.removeColumn(self._table.columnCount() - 1)

    # ── Image ─────────────────────────────────────────────────────────────────

    def _pick_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Wybierz zdjęcie", "",
            "Obrazy (*.png *.jpg *.jpeg *.bmp *.tiff)"
        )
        if path:
            self._image_path = path
            name = os.path.basename(path)
            self._img_label.setText(f"✓ {name}")
            self._img_label.setStyleSheet("color: #0E9F6E; font-size: 9pt;")

    # ── Data interface ────────────────────────────────────────────────────────

    def get_data(self) -> dict:
        t = self._table
        headers = [
            t.horizontalHeaderItem(c).text() if t.horizontalHeaderItem(c) else f"Kolumna {c+1}"
            for c in range(t.columnCount())
        ]
        rows = []
        for r in range(t.rowCount()):
            row_data = []
            for c in range(t.columnCount()):
                item = t.item(r, c)
                row_data.append(item.text() if item else "")
            rows.append(row_data)
        return {
            "headers":     headers,
            "rows":        rows,
            "description": self.description.toPlainText().strip(),
            "image_path":  self._image_path,
        }

    def set_data(self, data: dict):
        headers = data.get("headers", [])
        rows = data.get("rows", [])
        n_cols = len(headers) if headers else (len(rows[0]) if rows else 3)
        n_rows = len(rows) if rows else 3

        self._table.setRowCount(n_rows)
        self._table.setColumnCount(n_cols)

        if headers:
            self._table.setHorizontalHeaderLabels(headers)
        for r, row in enumerate(rows):
            for c, cell in enumerate(row):
                self._table.setItem(r, c, QTableWidgetItem(str(cell)))

        self.description.setPlainText(data.get("description", ""))
        img = data.get("image_path", "")
        if img and os.path.exists(img):
            self._image_path = img
            self._img_label.setText(f"✓ {os.path.basename(img)}")
            self._img_label.setStyleSheet("color: #0E9F6E; font-size: 9pt;")

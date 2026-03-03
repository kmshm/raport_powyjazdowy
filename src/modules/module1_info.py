"""
Module 1 — General Information (always active).
"""
from datetime import date

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit,
    QDateEdit, QPushButton, QLabel, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont

from src.modules.base_module import BaseModule
from src.theme import BORDER, PRIMARY, TEXT_SEC, BG_INPUT, FONT_FAMILY, FONT_SIZE_SM


class Module1Info(BaseModule):
    MODULE_ID = 1
    MODULE_TITLE = "Informacje Ogólne"
    ALWAYS_ON = True

    def _build_content(self, container: QWidget):
        layout = container.layout()

        # ── Row 1: Project number + Project name ──────────────────────────────
        row1 = QHBoxLayout()
        row1.setSpacing(12)

        self.project_number = QLineEdit()
        self.project_number.setPlaceholderText("np. 2024/001")
        self.project_number.setProperty("required", "true")
        row1.addLayout(self.field_row("Numer projektu", self.project_number, required=True))

        self.project_name = QLineEdit()
        self.project_name.setPlaceholderText("Nazwa projektu")
        row1.addLayout(self.field_row("Nazwa projektu", self.project_name))
        layout.addLayout(row1)

        # ── Row 2: Initials + Report date ────────────────────────────────────
        row2 = QHBoxLayout()
        row2.setSpacing(12)

        self.initials = QLineEdit()
        self.initials.setPlaceholderText("np. JK")
        self.initials.setMaximumWidth(120)
        self.initials.setProperty("required", "true")
        row2.addLayout(self.field_row("Inicjały wypełniającego", self.initials, required=True))

        self.report_date = QDateEdit()
        self.report_date.setCalendarPopup(True)
        self.report_date.setDate(QDate.currentDate())
        self.report_date.setMaximumWidth(160)
        row2.addLayout(self.field_row("Data wypełnienia raportu", self.report_date))
        row2.addStretch()
        layout.addLayout(row2)

        # ── Location ─────────────────────────────────────────────────────────
        self.location = QLineEdit()
        self.location.setPlaceholderText("Adres obiektu")
        layout.addLayout(self.field_row("Lokalizacja", self.location))

        self.maps_link = QLineEdit()
        self.maps_link.setPlaceholderText("https://maps.google.com/...")
        layout.addLayout(self.field_row("Link Google Maps", self.maps_link))

        # ── Measurement dates ─────────────────────────────────────────────────
        layout.addWidget(self.make_label("Daty pomiarów", required=True))
        self._dates_container = QVBoxLayout()
        self._dates_container.setSpacing(6)
        self._date_pickers: list[QDateEdit] = []
        layout.addLayout(self._dates_container)
        self._add_date_picker()  # start with one

        add_date_btn = QPushButton("+ Dodaj dzień")
        add_date_btn.setObjectName("small")
        add_date_btn.setMaximumWidth(130)
        add_date_btn.clicked.connect(self._add_date_picker)
        layout.addWidget(add_date_btn)

        # ── Measurement team ─────────────────────────────────────────────────
        self.team_leader = QLineEdit()
        self.team_leader.setPlaceholderText("Imię i nazwisko")
        layout.addLayout(self.field_row("Kierownik pomiarów", self.team_leader))

        self.team_members = QTextEdit()
        self.team_members.setPlaceholderText("Imię i Nazwisko, stanowisko — po jednym na linię")
        self.team_members.setFixedHeight(70)
        layout.addLayout(self.field_row("Skład zespołu pomiarowego", self.team_members))

        # ── Contact person ────────────────────────────────────────────────────
        layout.addWidget(self._section_divider("Osoba do kontaktu"))

        contact_row1 = QHBoxLayout()
        contact_row1.setSpacing(12)
        self.contact_title = QLineEdit()
        self.contact_title.setPlaceholderText("np. dr inż.")
        self.contact_title.setMaximumWidth(110)
        contact_row1.addLayout(self.field_row("Tytuł", self.contact_title))
        self.contact_first = QLineEdit()
        self.contact_first.setPlaceholderText("Imię")
        contact_row1.addLayout(self.field_row("Imię", self.contact_first))
        self.contact_last = QLineEdit()
        self.contact_last.setPlaceholderText("Nazwisko")
        contact_row1.addLayout(self.field_row("Nazwisko", self.contact_last))
        layout.addLayout(contact_row1)

        contact_row2 = QHBoxLayout()
        contact_row2.setSpacing(12)
        self.contact_phone = QLineEdit()
        self.contact_phone.setPlaceholderText("+48 000 000 000")
        contact_row2.addLayout(self.field_row("Telefon", self.contact_phone))
        self.contact_email = QLineEdit()
        self.contact_email.setPlaceholderText("email@example.com")
        contact_row2.addLayout(self.field_row("E-mail", self.contact_email))
        layout.addLayout(contact_row2)

    # ── Date picker helpers ───────────────────────────────────────────────────

    def _add_date_picker(self):
        row = QHBoxLayout()
        row.setSpacing(6)
        dp = QDateEdit()
        dp.setCalendarPopup(True)
        dp.setDate(QDate.currentDate())
        dp.setMaximumWidth(160)
        self._date_pickers.append(dp)
        row.addWidget(dp)

        if len(self._date_pickers) > 1:
            remove_btn = QPushButton("✕")
            remove_btn.setObjectName("small")
            remove_btn.setFixedSize(26, 26)
            remove_btn.setStyleSheet(
                "QPushButton { background: #FEE2E2; color: #DC2626; "
                "border: 1px solid #FECACA; border-radius: 4px; font-weight:700;}"
                "QPushButton:hover { background: #FCA5A5; }"
            )
            remove_btn.clicked.connect(lambda _, d=dp, r=row: self._remove_date(d, r))
            row.addWidget(remove_btn)

        row.addStretch()
        self._dates_container.addLayout(row)

    def _remove_date(self, picker: QDateEdit, row_layout: QHBoxLayout):
        if picker in self._date_pickers:
            self._date_pickers.remove(picker)
        while row_layout.count():
            item = row_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        # Remove the empty layout from parent
        parent = self._dates_container
        for i in range(parent.count()):
            if parent.itemAt(i) == row_layout or parent.itemAt(i).layout() is row_layout:
                parent.removeItem(parent.itemAt(i))
                break

    @staticmethod
    def _section_divider(title: str) -> QWidget:
        w = QWidget()
        h = QHBoxLayout(w)
        h.setContentsMargins(0, 8, 0, 4)
        h.setSpacing(8)
        lbl = QLabel(title)
        lbl.setStyleSheet(
            f"color: {TEXT_SEC}; font-size: {FONT_SIZE_SM}pt; font-weight: 600;"
        )
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet(f"color: {BORDER}; background: {BORDER};")
        h.addWidget(lbl)
        h.addWidget(line, 1)
        return w

    # ── Data interface ────────────────────────────────────────────────────────

    def get_data(self) -> dict:
        return {
            "project_number":   self.project_number.text().strip(),
            "project_name":     self.project_name.text().strip(),
            "initials":         self.initials.text().strip(),
            "report_date":      self.report_date.date().toPyDate(),
            "location":         self.location.text().strip(),
            "maps_link":        self.maps_link.text().strip(),
            "measurement_dates": [dp.date().toPyDate() for dp in self._date_pickers],
            "team_leader":      self.team_leader.text().strip(),
            "team_members":     self.team_members.toPlainText().strip(),
            "contact_title":    self.contact_title.text().strip(),
            "contact_first":    self.contact_first.text().strip(),
            "contact_last":     self.contact_last.text().strip(),
            "contact_phone":    self.contact_phone.text().strip(),
            "contact_email":    self.contact_email.text().strip(),
        }

    def set_data(self, data: dict):
        self.project_number.setText(data.get("project_number", ""))
        self.project_name.setText(data.get("project_name", ""))
        self.initials.setText(data.get("initials", ""))

        rd = data.get("report_date")
        if rd:
            if isinstance(rd, date):
                self.report_date.setDate(QDate(rd.year, rd.month, rd.day))
            else:
                self.report_date.setDate(QDate.fromString(str(rd), "yyyy-MM-dd"))

        self.location.setText(data.get("location", ""))
        self.maps_link.setText(data.get("maps_link", ""))

        dates = data.get("measurement_dates") or []
        # Clear existing pickers beyond the first
        while len(self._date_pickers) > 1:
            self._date_pickers[-1].deleteLater()
            self._date_pickers.pop()
        if self._date_pickers and dates:
            d = dates[0]
            self._date_pickers[0].setDate(
                QDate(d.year, d.month, d.day) if isinstance(d, date)
                else QDate.fromString(str(d), "yyyy-MM-dd")
            )
        for d in dates[1:]:
            self._add_date_picker()
            picker = self._date_pickers[-1]
            picker.setDate(
                QDate(d.year, d.month, d.day) if isinstance(d, date)
                else QDate.fromString(str(d), "yyyy-MM-dd")
            )

        self.team_leader.setText(data.get("team_leader", ""))
        self.team_members.setPlainText(data.get("team_members", ""))
        self.contact_title.setText(data.get("contact_title", ""))
        self.contact_first.setText(data.get("contact_first", ""))
        self.contact_last.setText(data.get("contact_last", ""))
        self.contact_phone.setText(data.get("contact_phone", ""))
        self.contact_email.setText(data.get("contact_email", ""))

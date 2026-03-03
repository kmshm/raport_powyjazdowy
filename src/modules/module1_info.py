"""
Module 1 - General Information (always active).
Improved layout: grouped sections with background cards, clear label/value contrast.
"""
from datetime import date

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit,
    QDateEdit, QPushButton, QLabel, QFrame,
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont

from src.modules.base_module import BaseModule
from src.theme import (
    BORDER, PRIMARY, TEXT, TEXT_SEC, BG, BG_CARD,
    FONT_FAMILY, FONT_SIZE_SM, FONT_SIZE_H3,
)

_REMOVE_BTN_STYLE = (
    "QPushButton { background: #FDECEA; color: #C41920; "
    "border: 1px solid #F5C6C5; border-radius: 4px; "
    "font-size: 8pt; padding: 2px 10px; min-width: 52px;}"
    "QPushButton:hover { background: #FAD4D2; }"
)


def _section_card(title: str) -> tuple[QWidget, QVBoxLayout]:
    """Returns a light-background card widget + its inner layout."""
    card = QWidget()
    card.setStyleSheet(
        f"background: {BG}; border-radius: 7px; border: 1px solid {BORDER};"
    )
    outer = QVBoxLayout(card)
    outer.setContentsMargins(14, 10, 14, 12)
    outer.setSpacing(10)

    hdr = QLabel(title.upper())
    hdr.setStyleSheet(
        f"color: {TEXT_SEC}; font-size: {FONT_SIZE_SM - 1}pt; font-weight: 700; "
        f"letter-spacing: 1px; border: none; background: transparent;"
    )
    outer.addWidget(hdr)

    sep = QFrame()
    sep.setFrameShape(QFrame.Shape.HLine)
    sep.setStyleSheet(f"background: {BORDER}; border: none; min-height: 1px; max-height: 1px;")
    outer.addWidget(sep)

    return card, outer


class Module1Info(BaseModule):
    MODULE_ID = 1
    MODULE_TITLE = "Informacje Ogolne"
    ALWAYS_ON = True

    def _build_content(self, container: QWidget):
        layout = container.layout()
        layout.setSpacing(10)

        # ── Section 1: Project identity ───────────────────────────────────────
        proj_card, proj_layout = _section_card("Projekt")

        row1 = QHBoxLayout()
        row1.setSpacing(14)

        self.project_number = QLineEdit()
        self.project_number.setPlaceholderText("np. 2024/001")
        self.project_number.setProperty("required", "true")
        row1.addLayout(self.field_row("Numer projektu", self.project_number, required=True))

        self.project_name = QLineEdit()
        self.project_name.setPlaceholderText("Pelna nazwa projektu lub obiektu")
        row1.addLayout(self.field_row("Nazwa projektu", self.project_name), 2)
        proj_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.setSpacing(14)

        self.initials = QLineEdit()
        self.initials.setPlaceholderText("np. JK")
        self.initials.setMaximumWidth(110)
        self.initials.setProperty("required", "true")
        row2.addLayout(self.field_row("Inicjaly wypelniajacego", self.initials, required=True))

        self.report_date = QDateEdit()
        self.report_date.setCalendarPopup(True)
        self.report_date.setDate(QDate.currentDate())
        self.report_date.setMaximumWidth(170)
        row2.addLayout(self.field_row("Data wypelnienia raportu", self.report_date))
        row2.addStretch()
        proj_layout.addLayout(row2)
        layout.addWidget(proj_card)

        # ── Section 2: Location ───────────────────────────────────────────────
        loc_card, loc_layout = _section_card("Lokalizacja")

        self.location = QLineEdit()
        self.location.setPlaceholderText("Adres obiektu, miejscowosc, kraj")
        loc_layout.addLayout(self.field_row("Adres", self.location))

        self.maps_link = QLineEdit()
        self.maps_link.setPlaceholderText("https://maps.google.com/...")
        loc_layout.addLayout(self.field_row("Link Google Maps", self.maps_link))
        layout.addWidget(loc_card)

        # ── Section 3: Measurement dates ──────────────────────────────────────
        dates_card, dates_layout = _section_card("Daty pomiarow  *")

        self._dates_container = QVBoxLayout()
        self._dates_container.setSpacing(6)
        self._date_pickers: list[QDateEdit] = []
        dates_layout.addLayout(self._dates_container)
        self._add_date_picker()

        add_date_btn = QPushButton("+ Dodaj dzien")
        add_date_btn.setObjectName("small")
        add_date_btn.setMaximumWidth(130)
        add_date_btn.clicked.connect(self._add_date_picker)
        dates_layout.addWidget(add_date_btn)
        layout.addWidget(dates_card)

        # ── Section 4: Team ───────────────────────────────────────────────────
        team_card, team_layout = _section_card("Zespol pomiarowy")

        self.team_leader = QLineEdit()
        self.team_leader.setPlaceholderText("Imie i nazwisko kierownika")
        team_layout.addLayout(self.field_row("Kierownik pomiarow", self.team_leader))

        self.team_members = QTextEdit()
        self.team_members.setPlaceholderText(
            "Imie i Nazwisko, stanowisko\nKolejny czlonek zespolu..."
        )
        self.team_members.setFixedHeight(72)
        team_layout.addLayout(self.field_row("Sklad zespolu pomiarowego", self.team_members))
        layout.addWidget(team_card)

        # ── Section 5: Contact person ─────────────────────────────────────────
        contact_card, contact_layout = _section_card("Osoba do kontaktu")

        contact_row1 = QHBoxLayout()
        contact_row1.setSpacing(14)
        self.contact_title = QLineEdit()
        self.contact_title.setPlaceholderText("np. dr inz.")
        self.contact_title.setMaximumWidth(120)
        contact_row1.addLayout(self.field_row("Tytul naukowy", self.contact_title))
        self.contact_first = QLineEdit()
        self.contact_first.setPlaceholderText("Imie")
        contact_row1.addLayout(self.field_row("Imie", self.contact_first))
        self.contact_last = QLineEdit()
        self.contact_last.setPlaceholderText("Nazwisko")
        contact_row1.addLayout(self.field_row("Nazwisko", self.contact_last))
        contact_layout.addLayout(contact_row1)

        contact_row2 = QHBoxLayout()
        contact_row2.setSpacing(14)
        self.contact_phone = QLineEdit()
        self.contact_phone.setPlaceholderText("+48 000 000 000")
        contact_row2.addLayout(self.field_row("Telefon", self.contact_phone))
        self.contact_email = QLineEdit()
        self.contact_email.setPlaceholderText("email@example.com")
        contact_row2.addLayout(self.field_row("E-mail", self.contact_email))
        contact_layout.addLayout(contact_row2)
        layout.addWidget(contact_card)

    # ── Date picker helpers ───────────────────────────────────────────────────

    def _add_date_picker(self):
        row = QHBoxLayout()
        row.setSpacing(6)
        dp = QDateEdit()
        dp.setCalendarPopup(True)
        dp.setDate(QDate.currentDate())
        dp.setMaximumWidth(170)
        self._date_pickers.append(dp)
        row.addWidget(dp)

        if len(self._date_pickers) > 1:
            remove_btn = QPushButton("Usun")
            remove_btn.setStyleSheet(_REMOVE_BTN_STYLE)
            remove_btn.clicked.connect(lambda: self._remove_date(dp, row))
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
        parent = self._dates_container
        for i in range(parent.count()):
            if parent.itemAt(i).layout() is row_layout:
                parent.removeItem(parent.itemAt(i))
                break

    # ── Data interface ────────────────────────────────────────────────────────

    def get_data(self) -> dict:
        return {
            "project_number":    self.project_number.text().strip(),
            "project_name":      self.project_name.text().strip(),
            "initials":          self.initials.text().strip(),
            "report_date":       self.report_date.date().toPyDate(),
            "location":          self.location.text().strip(),
            "maps_link":         self.maps_link.text().strip(),
            "measurement_dates": [dp.date().toPyDate() for dp in self._date_pickers],
            "team_leader":       self.team_leader.text().strip(),
            "team_members":      self.team_members.toPlainText().strip(),
            "contact_title":     self.contact_title.text().strip(),
            "contact_first":     self.contact_first.text().strip(),
            "contact_last":      self.contact_last.text().strip(),
            "contact_phone":     self.contact_phone.text().strip(),
            "contact_email":     self.contact_email.text().strip(),
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

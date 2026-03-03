"""
Application theme — colors, fonts, and reusable stylesheet snippets.
Color palette derived from company logo: charcoal #2B2A28 + red #E31E25.
"""

# ── Colour palette ────────────────────────────────────────────────────────────
PRIMARY   = "#E31E25"   # Logo red
PRIMARY_H = "#C41920"   # Hover
PRIMARY_L = "#FDECEA"   # Light red tint
ACCENT    = "#E31E25"
BG        = "#F4F4F4"
BG_CARD   = "#FFFFFF"
BG_INPUT  = "#F7F7F7"
BORDER    = "#E0E0E0"
TEXT      = "#2B2A28"   # Logo charcoal
TEXT_SEC  = "#6B6B69"
TEXT_WARN = "#C41920"
HEADER_BG = "#2B2A28"
HEADER_FG = "#FFFFFF"
TOGGLE_ON = "#E31E25"
TOGGLE_OFF= "#C8C8C6"

# ── Fonts ─────────────────────────────────────────────────────────────────────
FONT_FAMILY    = "Segoe UI"
FONT_SIZE_BASE = 10
FONT_SIZE_SM   = 9
FONT_SIZE_H1   = 17
FONT_SIZE_H2   = 12
FONT_SIZE_H3   = 10


# ── Global QSS stylesheet ─────────────────────────────────────────────────────
QSS = f"""
/* Global */
QWidget {{
    font-family: '{FONT_FAMILY}', 'Arial', sans-serif;
    font-size: {FONT_SIZE_BASE}pt;
    color: {TEXT};
    background-color: {BG};
}}

/* Scroll */
QScrollArea {{ border: none; background: {BG}; }}
QScrollArea > QWidget > QWidget {{ background: {BG}; }}
QScrollBar:vertical {{ background: {BG}; width: 8px; border-radius: 4px; margin: 0; }}
QScrollBar::handle:vertical {{ background: #CCCCCC; border-radius: 4px; min-height: 24px; }}
QScrollBar::handle:vertical:hover {{ background: #AAAAAA; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}

/* Inputs */
QLineEdit, QTextEdit, QPlainTextEdit {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 5px;
    padding: 5px 8px;
    color: {TEXT};
    selection-background-color: {PRIMARY};
    selection-color: white;
}}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border: 1.5px solid {PRIMARY};
}}
QLineEdit:hover, QTextEdit:hover, QPlainTextEdit:hover {{ border-color: #AAAAAA; }}
QLineEdit[required="true"] {{ border-left: 3px solid {PRIMARY}; }}

/* ComboBox */
QComboBox {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 5px;
    padding: 5px 28px 5px 8px;
    color: {TEXT};
    min-height: 26px;
}}
QComboBox:focus {{ border: 1.5px solid {PRIMARY}; }}
QComboBox:hover {{ border-color: #AAAAAA; }}
QComboBox::drop-down {{ border: none; width: 24px; subcontrol-origin: padding; subcontrol-position: top right; }}
QComboBox QAbstractItemView {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 5px;
    outline: none;
    selection-background-color: {PRIMARY};
    selection-color: white;
    padding: 2px;
    show-decoration-selected: 1;
}}
QComboBox QAbstractItemView::item {{
    padding: 6px 10px;
    color: {TEXT};
    min-height: 24px;
}}
QComboBox QAbstractItemView::item:hover {{
    background: {PRIMARY_L};
    color: {TEXT};
}}
QComboBox QAbstractItemView::item:selected {{
    background: {PRIMARY};
    color: white;
}}

/* Buttons */
QPushButton {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 5px;
    padding: 6px 14px;
    color: {TEXT};
    font-weight: 500;
}}
QPushButton:hover {{ background: #EBEBEB; border-color: #AAAAAA; }}
QPushButton:pressed {{ background: #DDDDDD; }}
QPushButton:disabled {{ color: #AAAAAA; background: {BG_INPUT}; border-color: {BORDER}; }}
QPushButton#primary {{ background: {PRIMARY}; color: white; border: none; font-weight: 600; }}
QPushButton#primary:hover {{ background: {PRIMARY_H}; }}
QPushButton#danger {{ background: #FDECEA; color: {TEXT_WARN}; border: 1px solid #F5C6C5; }}
QPushButton#danger:hover {{ background: #FAD4D2; }}
QPushButton#small {{ padding: 3px 8px; font-size: {FONT_SIZE_SM}pt; border-radius: 4px; }}

/* DateEdit */
QDateEdit {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 5px;
    padding: 5px 8px;
    color: {TEXT};
    min-height: 26px;
}}
QDateEdit:focus {{ border: 1.5px solid {PRIMARY}; }}
QDateEdit::drop-down {{ border: none; width: 22px; subcontrol-origin: padding; subcontrol-position: top right; }}

/* Calendar */
QCalendarWidget {{ background: {BG_CARD}; border: 1px solid {BORDER}; border-radius: 6px; }}
QCalendarWidget QWidget {{ background: {BG_CARD}; color: {TEXT}; alternate-background-color: {BG}; }}
QCalendarWidget QToolButton {{
    background: {BG_CARD}; color: {TEXT}; border: none;
    padding: 4px 8px; border-radius: 4px; font-weight: 600;
}}
QCalendarWidget QToolButton:hover {{ background: {PRIMARY_L}; color: {PRIMARY}; }}
QCalendarWidget QMenu {{ background: {BG_CARD}; color: {TEXT}; border: 1px solid {BORDER}; }}
QCalendarWidget QSpinBox {{
    background: {BG_CARD}; color: {TEXT}; border: 1px solid {BORDER};
    border-radius: 3px; padding: 2px 4px;
    selection-background-color: {PRIMARY}; selection-color: white;
}}
QCalendarWidget QAbstractItemView:enabled {{ color: {TEXT}; background: {BG_CARD}; outline: none; }}
QCalendarWidget QAbstractItemView:disabled {{ color: #BBBBBB; }}
QCalendarWidget QAbstractItemView {{ selection-background-color: {PRIMARY}; selection-color: white; }}

/* Checkboxes */
QCheckBox {{ spacing: 6px; color: {TEXT}; }}
QCheckBox::indicator {{ width: 16px; height: 16px; border-radius: 3px; border: 1.5px solid #CCCCCC; background: {BG_CARD}; }}
QCheckBox::indicator:hover {{ border-color: {PRIMARY}; }}
QCheckBox::indicator:checked {{ background: {PRIMARY}; border-color: {PRIMARY}; }}

/* Table */
QTableWidget {{
    background: {BG_CARD}; border: 1px solid {BORDER}; border-radius: 5px;
    gridline-color: {BORDER}; outline: none;
}}
QTableWidget::item {{ padding: 5px 6px; color: {TEXT}; }}
QTableWidget::item:selected {{ background: {PRIMARY_L}; color: {TEXT}; }}
QHeaderView::section {{
    background: #F0F0F0; border: none;
    border-right: 1px solid {BORDER}; border-bottom: 1px solid {BORDER};
    padding: 6px 8px; font-weight: 600; font-size: {FONT_SIZE_SM}pt; color: {TEXT_SEC};
}}

/* Tooltips */
QToolTip {{ background: {HEADER_BG}; color: white; border: none; padding: 4px 8px; border-radius: 4px; font-size: {FONT_SIZE_SM}pt; }}

/* Status bar */
QStatusBar {{ background: {BG_CARD}; color: {TEXT_SEC}; border-top: 1px solid {BORDER}; }}

/* File dialog */
QFileDialog {{ background: {BG_CARD}; }}
QFileDialog QWidget {{ background: {BG_CARD}; color: {TEXT}; }}
"""


def apply_theme(app):
    """Apply the global stylesheet to the QApplication."""
    app.setStyleSheet(QSS)

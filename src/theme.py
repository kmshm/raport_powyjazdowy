"""
Application theme — colors, fonts, and reusable stylesheet snippets.
"""

# ── Colour palette ────────────────────────────────────────────────────────────
PRIMARY   = "#1A56DB"   # vivid blue
PRIMARY_H = "#1E429F"   # hover
ACCENT    = "#0E9F6E"   # green for success / active toggles
BG        = "#F9FAFB"   # page background
BG_CARD   = "#FFFFFF"   # card / panel background
BG_INPUT  = "#F3F4F6"   # input field background
BORDER    = "#E5E7EB"   # subtle border
TEXT      = "#111827"   # primary text
TEXT_SEC  = "#6B7280"   # secondary / placeholder text
TEXT_WARN = "#DC2626"   # error / required
HEADER_BG = "#1E3A5F"   # deep navy for app header bar
HEADER_FG = "#FFFFFF"
TOGGLE_ON = "#0E9F6E"
TOGGLE_OFF= "#D1D5DB"

# ── Fonts ─────────────────────────────────────────────────────────────────────
FONT_FAMILY    = "Segoe UI"
FONT_SIZE_BASE = 10
FONT_SIZE_SM   = 9
FONT_SIZE_H1   = 18
FONT_SIZE_H2   = 13
FONT_SIZE_H3   = 11

# ── Global QSS stylesheet ─────────────────────────────────────────────────────
QSS = f"""
/* ── Global ── */
QWidget {{
    font-family: '{FONT_FAMILY}', 'Arial', sans-serif;
    font-size: {FONT_SIZE_BASE}pt;
    color: {TEXT};
    background-color: {BG};
}}

/* ── Scroll area ── */
QScrollArea {{
    border: none;
    background: {BG};
}}
QScrollArea > QWidget > QWidget {{
    background: {BG};
}}
QScrollBar:vertical {{
    background: {BG};
    width: 8px;
    border-radius: 4px;
}}
QScrollBar::handle:vertical {{
    background: {BORDER};
    border-radius: 4px;
    min-height: 24px;
}}
QScrollBar::handle:vertical:hover {{
    background: {TEXT_SEC};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

/* ── Line edit / Text edit ── */
QLineEdit, QTextEdit, QPlainTextEdit {{
    background: {BG_INPUT};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 5px 8px;
    color: {TEXT};
}}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
    border-color: {PRIMARY};
    background: {BG_CARD};
}}
QLineEdit[required="true"] {{
    border-left: 3px solid {PRIMARY};
}}

/* ── ComboBox ── */
QComboBox {{
    background: {BG_INPUT};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 5px 8px;
    color: {TEXT};
}}
QComboBox:focus {{
    border-color: {PRIMARY};
}}
QComboBox::drop-down {{
    border: none;
    width: 20px;
}}
QComboBox QAbstractItemView {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    selection-background-color: {PRIMARY};
    selection-color: white;
}}

/* ── Push buttons ── */
QPushButton {{
    background: {BG_INPUT};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 6px 14px;
    color: {TEXT};
    font-weight: 500;
}}
QPushButton:hover {{
    background: {BORDER};
    border-color: {TEXT_SEC};
}}
QPushButton:pressed {{
    background: {BORDER};
}}

QPushButton#primary {{
    background: {PRIMARY};
    color: white;
    border: none;
    font-weight: 600;
}}
QPushButton#primary:hover {{
    background: {PRIMARY_H};
}}

QPushButton#danger {{
    background: #FEE2E2;
    color: {TEXT_WARN};
    border: 1px solid #FECACA;
}}
QPushButton#danger:hover {{
    background: #FCA5A5;
}}

QPushButton#small {{
    padding: 3px 8px;
    font-size: {FONT_SIZE_SM}pt;
    border-radius: 4px;
}}

/* ── Date edit ── */
QDateEdit {{
    background: {BG_INPUT};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 5px 8px;
}}
QDateEdit:focus {{
    border-color: {PRIMARY};
}}

/* ── Check box ── */
QCheckBox {{
    spacing: 6px;
    color: {TEXT};
}}
QCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 1px solid {BORDER};
    background: {BG_INPUT};
}}
QCheckBox::indicator:checked {{
    background: {PRIMARY};
    border-color: {PRIMARY};
    image: url(:/check.png);
}}

/* ── Group box (module card) ── */
QGroupBox {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
    margin-top: 12px;
    padding-top: 10px;
    font-size: {FONT_SIZE_H3}pt;
    font-weight: 600;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 12px;
    color: {TEXT};
}}

/* ── Table widget ── */
QTableWidget {{
    background: {BG_CARD};
    border: 1px solid {BORDER};
    border-radius: 6px;
    gridline-color: {BORDER};
}}
QTableWidget::item {{
    padding: 4px;
}}
QTableWidget::item:selected {{
    background: #DBEAFE;
    color: {TEXT};
}}
QHeaderView::section {{
    background: {BG_INPUT};
    border: none;
    border-right: 1px solid {BORDER};
    border-bottom: 1px solid {BORDER};
    padding: 6px 8px;
    font-weight: 600;
    font-size: {FONT_SIZE_SM}pt;
    color: {TEXT_SEC};
}}

/* ── Label ── */
QLabel#sectionTitle {{
    font-size: {FONT_SIZE_H2}pt;
    font-weight: 700;
    color: {TEXT};
}}
QLabel#fieldLabel {{
    font-size: {FONT_SIZE_SM}pt;
    color: {TEXT_SEC};
    font-weight: 500;
}}
QLabel#required {{
    color: {TEXT_WARN};
    font-size: {FONT_SIZE_SM}pt;
}}

/* ── Splitter ── */
QSplitter::handle {{
    background: {BORDER};
}}

/* ── Tool tip ── */
QToolTip {{
    background: {HEADER_BG};
    color: white;
    border: none;
    padding: 4px 8px;
    border-radius: 4px;
}}
"""


def apply_theme(app):
    """Apply the global stylesheet to the QApplication."""
    app.setStyleSheet(QSS)

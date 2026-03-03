"""
BaseModule — shared widget logic for every report section.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPainter, QBrush

from src.theme import (
    BG_CARD, BORDER, TEXT, TEXT_SEC, PRIMARY, TOGGLE_ON, TOGGLE_OFF,
    FONT_FAMILY, FONT_SIZE_H2, FONT_SIZE_SM,
)


class ToggleSwitch(QWidget):
    """Compact on/off toggle painted manually."""
    toggled = pyqtSignal(bool)

    def __init__(self, enabled=True, parent=None):
        super().__init__(parent)
        self._checked = enabled
        self.setFixedSize(42, 24)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("Wlacz / Wylacz modul")

    def isChecked(self):
        return self._checked

    def setChecked(self, value):
        if self._checked != value:
            self._checked = value
            self.update()

    def mousePressEvent(self, event):
        self._checked = not self._checked
        self.update()
        self.toggled.emit(self._checked)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        track_color = QColor(TOGGLE_ON) if self._checked else QColor(TOGGLE_OFF)
        p.setBrush(QBrush(track_color))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(0, 4, 42, 16, 8, 8)
        thumb_x = 22 if self._checked else 2
        p.setBrush(QBrush(QColor("#FFFFFF")))
        p.drawEllipse(thumb_x, 2, 20, 20)


class BaseModule(QWidget):
    """
    Base class for all report modules.
    Subclasses implement: _build_content, get_data, set_data.
    """
    enabledChanged = pyqtSignal(bool)
    MODULE_ID: int = 0
    MODULE_TITLE: str = "Modul"
    ALWAYS_ON: bool = False

    def __init__(self, parent=None):
        super().__init__(parent)
        self._collapsed = False
        self._enabled = True
        self._setup_ui()

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 8)
        root.setSpacing(0)

        self._card = QFrame()
        self._card.setObjectName("moduleCard")
        self._card.setStyleSheet(
            f"QFrame#moduleCard {{ background: {BG_CARD}; "
            f"border: 1px solid {BORDER}; border-radius: 10px; }}"
        )
        card_layout = QVBoxLayout(self._card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)

        card_layout.addWidget(self._build_header())

        self._separator = QFrame()
        self._separator.setFrameShape(QFrame.Shape.HLine)
        self._separator.setStyleSheet(
            f"background: {BORDER}; border: none; min-height: 1px; max-height: 1px;"
        )
        card_layout.addWidget(self._separator)

        self._content_widget = QWidget()
        self._content_widget.setStyleSheet("background: transparent;")
        cl = QVBoxLayout(self._content_widget)
        cl.setContentsMargins(20, 16, 20, 20)
        cl.setSpacing(12)
        self._build_content(self._content_widget)
        card_layout.addWidget(self._content_widget)

        root.addWidget(self._card)
        if self.ALWAYS_ON:
            self._toggle.hide()

    def _build_header(self):
        header = QWidget()
        header.setStyleSheet("background: transparent;")
        header.setFixedHeight(52)
        hbox = QHBoxLayout(header)
        hbox.setContentsMargins(16, 0, 14, 0)
        hbox.setSpacing(10)

        badge = QLabel(str(self.MODULE_ID))
        badge.setFixedSize(26, 26)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(
            f"background: {PRIMARY}; color: white; border-radius: 13px; "
            f"font-weight: 700; font-size: {FONT_SIZE_SM}pt;"
        )
        hbox.addWidget(badge)

        title = QLabel(self.MODULE_TITLE)
        title.setFont(QFont(FONT_FAMILY, FONT_SIZE_H2, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {TEXT};")
        hbox.addWidget(title, 1)

        self._toggle = ToggleSwitch(enabled=True)
        self._toggle.toggled.connect(self._on_toggle)
        hbox.addWidget(self._toggle)

        self._collapse_btn = QPushButton("v")
        self._collapse_btn.setFixedSize(30, 30)
        self._collapse_btn.setStyleSheet(
            f"QPushButton {{ background: transparent; border: none; "
            f"font-size: 11pt; font-weight: bold; color: {TEXT_SEC}; border-radius: 4px; }}"
            f"QPushButton:hover {{ background: #EBEBEB; }}"
        )
        self._collapse_btn.clicked.connect(self._toggle_collapse)
        hbox.addWidget(self._collapse_btn)
        return header

    def _toggle_collapse(self):
        self._collapsed = not self._collapsed
        self._content_widget.setVisible(not self._collapsed)
        self._separator.setVisible(not self._collapsed)
        self._collapse_btn.setText(">" if self._collapsed else "v")

    def _on_toggle(self, enabled: bool):
        self._enabled = enabled
        self._content_widget.setEnabled(enabled)
        # Dim content when disabled
        self._content_widget.setStyleSheet(
            "background: transparent;" if enabled
            else "background: transparent; opacity: 0.4;"
        )
        # Auto-collapse on disable, auto-expand on re-enable
        if not enabled and not self._collapsed:
            self._toggle_collapse()
        elif enabled and self._collapsed:
            self._toggle_collapse()
        self.enabledChanged.emit(enabled)

    def is_enabled(self):
        return self._enabled

    def set_enabled(self, value: bool):
        self._toggle.setChecked(value)
        self._on_toggle(value)

    def _build_content(self, container):
        raise NotImplementedError

    def get_data(self):
        raise NotImplementedError

    def set_data(self, data: dict):
        raise NotImplementedError

    @staticmethod
    def make_label(text: str, required: bool = False):
        """Uppercase field label with optional required marker."""
        suffix = " *" if required else ""
        lbl = QLabel(text.upper() + suffix)
        lbl.setObjectName("fieldLabel")
        lbl.setStyleSheet(
            f"color: {'#C41920' if required else TEXT_SEC}; "
            f"font-size: {FONT_SIZE_SM - 1}pt; font-weight: 600; "
            f"letter-spacing: 0.5px; background: transparent;"
        )
        return lbl

    @staticmethod
    def field_row(label_text: str, widget, required: bool = False):
        """Vertical label + widget stack."""
        vbox = QVBoxLayout()
        vbox.setSpacing(4)
        vbox.addWidget(BaseModule.make_label(label_text, required))
        vbox.addWidget(widget)
        return vbox

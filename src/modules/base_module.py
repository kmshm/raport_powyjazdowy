"""
BaseModule — shared widget logic for every report section.

Each module:
  - has an enable/disable toggle (except Module 1 which is always on)
  - can be collapsed / expanded
  - exposes get_data() -> dict and set_data(dict) methods
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor

from src.theme import (
    BG_CARD, BORDER, TEXT, TEXT_SEC, PRIMARY, TOGGLE_ON, TOGGLE_OFF,
    FONT_FAMILY, FONT_SIZE_H2, FONT_SIZE_SM
)


class ToggleSwitch(QWidget):
    """Compact on/off toggle painted manually."""
    toggled = pyqtSignal(bool)

    def __init__(self, enabled: bool = True, parent=None):
        super().__init__(parent)
        self._checked = enabled
        self.setFixedSize(42, 22)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def isChecked(self) -> bool:
        return self._checked

    def setChecked(self, value: bool):
        self._checked = value
        self.update()

    def mousePressEvent(self, event):
        self._checked = not self._checked
        self.update()
        self.toggled.emit(self._checked)

    def paintEvent(self, event):
        from PyQt6.QtGui import QPainter, QBrush, QPen
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        track_color = QColor(TOGGLE_ON) if self._checked else QColor(TOGGLE_OFF)
        p.setBrush(QBrush(track_color))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(0, 3, 42, 16, 8, 8)
        thumb_x = 22 if self._checked else 2
        p.setBrush(QBrush(QColor("#FFFFFF")))
        p.drawEllipse(thumb_x, 1, 20, 20)


class BaseModule(QWidget):
    """
    Base class for all report modules.

    Subclasses must implement:
      _build_content(container: QWidget)  — add their fields to container
      get_data() -> dict
      set_data(data: dict)
    """

    # Signal emitted when the enable state changes
    enabledChanged = pyqtSignal(bool)

    # Override in subclasses
    MODULE_ID: int = 0
    MODULE_TITLE: str = "Moduł"
    ALWAYS_ON: bool = False      # Module 1 overrides to True

    def __init__(self, parent=None):
        super().__init__(parent)
        self._collapsed = False
        self._enabled = True
        self._setup_ui()

    # ── UI construction ───────────────────────────────────────────────────────

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 8)
        root.setSpacing(0)

        # Card frame
        self._card = QFrame()
        self._card.setObjectName("moduleCard")
        self._card.setStyleSheet(f"""
            QFrame#moduleCard {{
                background: {BG_CARD};
                border: 1px solid {BORDER};
                border-radius: 10px;
            }}
        """)
        card_layout = QVBoxLayout(self._card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)

        # Header bar
        header = self._build_header()
        card_layout.addWidget(header)

        # Separator line
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {BORDER}; background: {BORDER}; border: none; min-height: 1px; max-height: 1px;")
        self._separator = sep
        card_layout.addWidget(sep)

        # Content area
        self._content_widget = QWidget()
        self._content_widget.setStyleSheet(f"background: transparent;")
        content_layout = QVBoxLayout(self._content_widget)
        content_layout.setContentsMargins(20, 16, 20, 20)
        content_layout.setSpacing(12)
        self._build_content(self._content_widget)
        card_layout.addWidget(self._content_widget)

        root.addWidget(self._card)

        if self.ALWAYS_ON:
            self._toggle.hide()

    def _build_header(self) -> QWidget:
        header = QWidget()
        header.setStyleSheet("background: transparent;")
        header.setFixedHeight(50)
        hbox = QHBoxLayout(header)
        hbox.setContentsMargins(16, 0, 16, 0)
        hbox.setSpacing(10)

        # Module number badge
        badge = QLabel(str(self.MODULE_ID))
        badge.setFixedSize(26, 26)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        badge.setStyleSheet(f"""
            background: {PRIMARY};
            color: white;
            border-radius: 13px;
            font-weight: 700;
            font-size: {FONT_SIZE_SM}pt;
        """)
        hbox.addWidget(badge)

        # Title
        title = QLabel(self.MODULE_TITLE)
        title.setFont(QFont(FONT_FAMILY, FONT_SIZE_H2, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {TEXT};")
        hbox.addWidget(title, 1)

        # Enable toggle (hidden for always-on modules)
        self._toggle = ToggleSwitch(enabled=True)
        self._toggle.toggled.connect(self._on_toggle)
        hbox.addWidget(self._toggle)

        # Collapse button
        self._collapse_btn = QPushButton("▾")
        self._collapse_btn.setFixedSize(28, 28)
        self._collapse_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                font-size: 14pt;
                color: {TEXT_SEC};
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background: {BORDER};
            }}
        """)
        self._collapse_btn.clicked.connect(self._toggle_collapse)
        hbox.addWidget(self._collapse_btn)

        return header

    # ── Collapse / expand ─────────────────────────────────────────────────────

    def _toggle_collapse(self):
        self._collapsed = not self._collapsed
        self._content_widget.setVisible(not self._collapsed)
        self._separator.setVisible(not self._collapsed)
        self._collapse_btn.setText("▸" if self._collapsed else "▾")

    # ── Enable / disable ──────────────────────────────────────────────────────

    def _on_toggle(self, enabled: bool):
        self._enabled = enabled
        self._content_widget.setEnabled(enabled)
        opacity = "1.0" if enabled else "0.45"
        self._content_widget.setStyleSheet(
            f"background: transparent; opacity: {opacity};"
        )
        self.enabledChanged.emit(enabled)

    def is_enabled(self) -> bool:
        return self._enabled

    def set_enabled(self, value: bool):
        self._toggle.setChecked(value)
        self._on_toggle(value)

    # ── Abstract interface ────────────────────────────────────────────────────

    def _build_content(self, container: QWidget):
        """Subclasses fill the content area here."""
        raise NotImplementedError

    def get_data(self) -> dict:
        """Return all module data as a serialisable dict."""
        raise NotImplementedError

    def set_data(self, data: dict):
        """Populate fields from a dict (e.g. after PDF import)."""
        raise NotImplementedError

    # ── Helpers shared by child modules ───────────────────────────────────────

    @staticmethod
    def make_label(text: str, required: bool = False) -> QLabel:
        lbl = QLabel(text + (" *" if required else ""))
        lbl.setObjectName("fieldLabel")
        lbl.setStyleSheet(
            f"color: {'#DC2626' if required else TEXT_SEC}; "
            f"font-size: {FONT_SIZE_SM}pt; font-weight: 500;"
        )
        return lbl

    @staticmethod
    def field_row(label_text: str, widget: QWidget, required: bool = False) -> QVBoxLayout:
        """Vertical label + widget stack."""
        vbox = QVBoxLayout()
        vbox.setSpacing(3)
        vbox.addWidget(BaseModule.make_label(label_text, required))
        vbox.addWidget(widget)
        return vbox

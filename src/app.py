"""
Main application window.
"""
import os
import sys
import subprocess
from datetime import date

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QScrollArea, QFileDialog, QMessageBox, QFrame,
    QStatusBar, QApplication, QSizePolicy
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPixmap

from src.theme import (
    HEADER_BG, HEADER_FG, BG, BG_CARD, BORDER, PRIMARY, TEXT, TEXT_SEC,
    FONT_FAMILY, FONT_SIZE_H1, FONT_SIZE_SM
)
from src.modules.module1_info import Module1Info
from src.modules.module2_equipment import Module2Equipment
from src.modules.module3_fiber import Module3Fiber
from src.modules.module4_sensors import Module4Sensors
from src.modules.module5_inventory import Module5Inventory
from src.modules.module6_measurements import Module6Measurements
from src.modules.module7_packing import Module7Packing
from src.modules.module8_notes import Module8Notes
from src.modules.module9_logistics import Module9Logistics
from src.pdf.generator import generate_pdf
from src.utils.validators import validate_required_fields, build_filename

LOGO_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")


# ── Background worker for PDF generation ─────────────────────────────────────

class PdfWorker(QThread):
    finished = pyqtSignal(str)   # emits output path on success
    error    = pyqtSignal(str)   # emits error message on failure

    def __init__(self, all_data: dict, output_path: str):
        super().__init__()
        self._all_data = all_data
        self._output_path = output_path

    def run(self):
        try:
            generate_pdf(self._all_data, self._output_path)
            self.finished.emit(self._output_path)
        except Exception as exc:
            self.error.emit(str(exc))


# ── Header widget ─────────────────────────────────────────────────────────────

class AppHeader(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(64)
        self.setStyleSheet(f"background: {HEADER_BG};")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(14)

        # Logo
        logo_lbl = QLabel()
        logo_lbl.setFixedSize(44, 44)
        if os.path.exists(LOGO_PATH):
            px = QPixmap(LOGO_PATH).scaled(
                44, 44,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            logo_lbl.setPixmap(px)
        else:
            logo_lbl.setText("●")
            logo_lbl.setStyleSheet("color: white; font-size: 28pt;")
        logo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_lbl)

        # Title
        title = QLabel("Raport Powyjazdowy")
        title.setFont(QFont(FONT_FAMILY, FONT_SIZE_H1, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {HEADER_FG};")
        layout.addWidget(title)

        layout.addStretch()

        # Action buttons
        for text, obj_name, tooltip in [
            ("Nowy raport",     "new_btn",    "Wyczyść wszystkie pola"),
            ("Importuj PDF",    "import_btn", "Wczytaj raport z pliku PDF"),
            ("Podgląd PDF",     "preview_btn","Podgląd przed wygenerowaniem"),
            ("Generuj PDF",     "generate_btn","Wygeneruj i zapisz raport PDF"),
        ]:
            btn = QPushButton(text)
            btn.setObjectName(obj_name)
            btn.setToolTip(tooltip)
            btn.setStyleSheet(self._btn_style(text == "Generuj PDF"))
            layout.addWidget(btn)
            setattr(self, obj_name, btn)

    @staticmethod
    def _btn_style(primary: bool) -> str:
        if primary:
            return (
                f"QPushButton {{ background: {PRIMARY}; color: white; "
                f"border: none; border-radius: 6px; padding: 8px 18px; font-weight: 600; }}"
                f"QPushButton:hover {{ background: #1E429F; }}"
            )
        return (
            "QPushButton { background: rgba(255,255,255,0.12); color: white; "
            "border: 1px solid rgba(255,255,255,0.25); border-radius: 6px; "
            "padding: 7px 14px; }"
            "QPushButton:hover { background: rgba(255,255,255,0.22); }"
        )


# ── Main window ───────────────────────────────────────────────────────────────

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Raport Powyjazdowy")
        self.setMinimumSize(900, 700)
        self.resize(1100, 820)
        self._worker: PdfWorker | None = None
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Header
        self._header = AppHeader()
        root.addWidget(self._header)

        # Scroll area with module list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        content.setStyleSheet(f"background: {BG};")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 20, 24, 24)
        content_layout.setSpacing(0)

        # Instantiate all modules
        self._modules = [
            Module1Info(),
            Module2Equipment(),
            Module3Fiber(),
            Module4Sensors(),
            Module5Inventory(),
            Module6Measurements(),
            Module7Packing(),
            Module8Notes(),
            Module9Logistics(),
        ]
        for mod in self._modules:
            content_layout.addWidget(mod)

        content_layout.addStretch()
        scroll.setWidget(content)
        root.addWidget(scroll, 1)

        # Status bar
        self._status = QStatusBar()
        self._status.setStyleSheet(
            f"QStatusBar {{ background: {BG_CARD}; border-top: 1px solid {BORDER}; "
            f"font-size: {FONT_SIZE_SM}pt; color: {TEXT_SEC}; }}"
        )
        self.setStatusBar(self._status)
        self._status.showMessage("Gotowy")

    def _connect_signals(self):
        self._header.new_btn.clicked.connect(self._on_new)
        self._header.import_btn.clicked.connect(self._on_import)
        self._header.preview_btn.clicked.connect(self._on_preview)
        self._header.generate_btn.clicked.connect(self._on_generate)

    # ── Slot: New ─────────────────────────────────────────────────────────────

    def _on_new(self):
        reply = QMessageBox.question(
            self, "Nowy raport",
            "Czy na pewno chcesz wyczyścić wszystkie pola?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            for mod in self._modules:
                mod.set_data({})
            self._status.showMessage("Wyczyszczono formularz")

    # ── Slot: Import PDF ──────────────────────────────────────────────────────

    def _on_import(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Importuj raport PDF", "", "Pliki PDF (*.pdf)"
        )
        if not path:
            return
        try:
            from src.pdf.parser import parse_pdf
            all_data = parse_pdf(path)
        except ImportError as exc:
            QMessageBox.warning(self, "Brak biblioteki", str(exc))
            return
        except ValueError as exc:
            QMessageBox.critical(self, "Błąd importu", str(exc))
            return

        for mod in self._modules:
            mid = mod.MODULE_ID
            if mid in all_data:
                mod.set_data(all_data[mid])
                if mid != 1:
                    mod.set_enabled(all_data[mid].get("enabled", True))

        self._status.showMessage(f"Zaimportowano: {os.path.basename(path)}")

    # ── Slot: Preview ─────────────────────────────────────────────────────────

    def _on_preview(self):
        """Generate to a temp file and open it in the system viewer."""
        import tempfile
        errors = validate_required_fields(self._collect_module1_data())
        if errors:
            QMessageBox.warning(self, "Brakujące pola", "\n".join(errors))
            return

        tmp = tempfile.NamedTemporaryFile(
            suffix=".pdf", prefix="podglad_", delete=False
        )
        tmp.close()
        self._generate(tmp.name, open_after=True)

    # ── Slot: Generate ────────────────────────────────────────────────────────

    def _on_generate(self):
        errors = validate_required_fields(self._collect_module1_data())
        if errors:
            QMessageBox.warning(self, "Brakujące pola wymagane", "\n".join(errors))
            return

        filename = build_filename(self._collect_module1_data())
        path, _ = QFileDialog.getSaveFileName(
            self, "Zapisz raport PDF",
            os.path.join(os.path.expanduser("~"), "Desktop", filename),
            "Pliki PDF (*.pdf)",
        )
        if not path:
            return
        self._generate(path, open_after=False)

    # ── PDF generation helpers ────────────────────────────────────────────────

    def _collect_module1_data(self) -> dict:
        return self._modules[0].get_data()   # Module1Info is index 0

    def _collect_all_data(self) -> dict:
        all_data = {}
        for mod in self._modules:
            d = mod.get_data()
            d["enabled"] = mod.is_enabled()
            all_data[mod.MODULE_ID] = d
        return all_data

    def _generate(self, output_path: str, open_after: bool):
        self._header.generate_btn.setEnabled(False)
        self._header.preview_btn.setEnabled(False)
        self._status.showMessage("Generowanie PDF…")

        all_data = self._collect_all_data()
        self._worker = PdfWorker(all_data, output_path)
        self._worker.finished.connect(lambda p: self._on_pdf_done(p, open_after))
        self._worker.error.connect(self._on_pdf_error)
        self._worker.start()

    def _on_pdf_done(self, path: str, open_after: bool):
        self._header.generate_btn.setEnabled(True)
        self._header.preview_btn.setEnabled(True)
        self._status.showMessage(f"PDF zapisany: {path}")

        if open_after:
            self._open_file(path)
        else:
            reply = QMessageBox.information(
                self, "Gotowe",
                f"Raport PDF został zapisany:\n{path}",
                QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Open,
            )
            if reply == QMessageBox.StandardButton.Open:
                self._open_file(path)

    def _on_pdf_error(self, msg: str):
        self._header.generate_btn.setEnabled(True)
        self._header.preview_btn.setEnabled(True)
        self._status.showMessage("Błąd generowania PDF")
        QMessageBox.critical(self, "Błąd generowania PDF", msg)

    @staticmethod
    def _open_file(path: str):
        """Open the file in the default system viewer."""
        try:
            if sys.platform.startswith("win"):
                os.startfile(path)
            elif sys.platform.startswith("darwin"):
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
        except Exception:
            pass

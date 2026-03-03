"""
File dialog helpers — use QFileDialog instances (not static methods) so we
can apply an explicit white stylesheet and avoid the transparency issue that
occurs when the app-wide QSS makes dialog backgrounds transparent.
"""
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QDir

_DIALOG_STYLE = """
QWidget          { background-color: #FFFFFF; color: #2B2A28; }
QDialog          { background-color: #FFFFFF; }
QFrame           { background-color: #FFFFFF; border: none; }
QListView        { background-color: #FFFFFF; alternate-background-color: #F7F7F7;
                   color: #2B2A28; border: 1px solid #E0E0E0; outline: none; }
QListView::item:selected { background-color: #FDECEA; color: #2B2A28; }
QListView::item:hover    { background-color: #F4F4F4; }
QTreeView        { background-color: #FFFFFF; alternate-background-color: #F7F7F7;
                   color: #2B2A28; border: 1px solid #E0E0E0; outline: none; }
QTreeView::item:selected { background-color: #FDECEA; color: #2B2A28; }
QHeaderView::section { background-color: #F0F0F0; color: #6B6B69;
                        border: none; border-bottom: 1px solid #E0E0E0;
                        padding: 4px 6px; font-weight: 600; }
QLineEdit        { background-color: #F7F7F7; border: 1px solid #E0E0E0;
                   border-radius: 4px; padding: 4px 8px; color: #2B2A28; }
QLineEdit:focus  { border-color: #E31E25; }
QPushButton      { background-color: #F4F4F4; border: 1px solid #E0E0E0;
                   border-radius: 4px; padding: 5px 12px; color: #2B2A28; }
QPushButton:hover { background-color: #EBEBEB; }
QPushButton:default { background-color: #E31E25; color: white; border: none; }
QPushButton:default:hover { background-color: #C41920; }
QComboBox        { background-color: #F7F7F7; border: 1px solid #E0E0E0;
                   border-radius: 4px; padding: 4px 8px; color: #2B2A28; }
QLabel           { background: transparent; color: #2B2A28; }
QToolBar         { background-color: #F4F4F4; border: none; }
QToolButton      { background-color: transparent; border: none; color: #2B2A28;
                   padding: 4px; border-radius: 3px; }
QToolButton:hover { background-color: #EBEBEB; }
QSplitter::handle { background-color: #E0E0E0; }
QScrollBar:vertical   { background: #F4F4F4; width: 8px; border-radius: 4px; }
QScrollBar::handle:vertical { background: #CCCCCC; border-radius: 4px; min-height: 20px; }
"""


def open_image_dialog(parent, title: str = "Wybierz zdjecie") -> str:
    """
    Open a non-native, properly styled file dialog for selecting images.
    Returns the selected file path, or "" if cancelled.
    """
    dlg = QFileDialog(parent, title)
    dlg.setOption(QFileDialog.Option.DontUseNativeDialog, True)
    dlg.setFileMode(QFileDialog.FileMode.ExistingFile)
    dlg.setNameFilter("Obrazy (*.png *.jpg *.jpeg *.bmp *.tiff)")
    dlg.setStyleSheet(_DIALOG_STYLE)
    if dlg.exec():
        files = dlg.selectedFiles()
        return files[0] if files else ""
    return ""


def open_pdf_dialog(parent, title: str = "Importuj raport PDF") -> str:
    """Open a styled dialog for selecting a PDF file."""
    dlg = QFileDialog(parent, title)
    dlg.setOption(QFileDialog.Option.DontUseNativeDialog, True)
    dlg.setFileMode(QFileDialog.FileMode.ExistingFile)
    dlg.setNameFilter("Pliki PDF (*.pdf)")
    dlg.setStyleSheet(_DIALOG_STYLE)
    if dlg.exec():
        files = dlg.selectedFiles()
        return files[0] if files else ""
    return ""


def save_pdf_dialog(parent, default_name: str = "raport.pdf") -> str:
    """Open a styled dialog for saving a PDF file."""
    import os
    dlg = QFileDialog(parent, "Zapisz raport PDF")
    dlg.setOption(QFileDialog.Option.DontUseNativeDialog, True)
    dlg.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
    dlg.setFileMode(QFileDialog.FileMode.AnyFile)
    dlg.setNameFilter("Pliki PDF (*.pdf)")
    dlg.selectFile(default_name)
    dlg.setDirectory(os.path.expanduser("~"))
    dlg.setStyleSheet(_DIALOG_STYLE)
    if dlg.exec():
        files = dlg.selectedFiles()
        path = files[0] if files else ""
        if path and not path.endswith(".pdf"):
            path += ".pdf"
        return path
    return ""

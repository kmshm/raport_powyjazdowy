#!/usr/bin/env python3
"""
Raport Powyjazdowy — entry point.
"""
import sys
import os

# Ensure the project root is on PYTHONPATH when running directly
sys.path.insert(0, os.path.dirname(__file__))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from src.app import MainWindow
from src.theme import apply_theme, FONT_FAMILY, FONT_SIZE_BASE


def main():
    # High-DPI support (PyQt6 enables it by default, but we set the policy explicitly)
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("Raport Powyjazdowy")
    app.setOrganizationName("SensorLab")

    # Default font
    font = QFont(FONT_FAMILY, FONT_SIZE_BASE)
    app.setFont(font)

    # Apply stylesheet
    apply_theme(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

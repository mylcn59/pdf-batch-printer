#!/usr/bin/env python3
"""
PDF Batch Printer - Cross-platform PDF batch printing application
Main entry point
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from gui.main_window import MainWindow


def main():
    # High DPI scaling for modern displays
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("PDF Batch Printer")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("PDFBatchPrinter")

    # Apply modern style
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

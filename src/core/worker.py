"""
Background worker thread for batch PDF printing
"""

import os
from pathlib import Path
from PyQt6.QtCore import QThread, pyqtSignal

from core.printer import print_pdf, PrintResult


class PrintWorker(QThread):
    """
    Worker thread that handles batch PDF printing.
    Emits signals to update the UI without blocking.
    """

    # Signals
    progress = pyqtSignal(int, int)  # current, total
    file_started = pyqtSignal(int, str)  # index, filename
    file_completed = pyqtSignal(int, str)  # index, filename
    file_error = pyqtSignal(int, str, str)  # index, filename, error message
    finished = pyqtSignal(int, int)  # success_count, error_count

    def __init__(self, pdf_files: list[str], parent=None):
        super().__init__(parent)
        self.pdf_files = pdf_files
        self._cancelled = False

    def cancel(self):
        """Request cancellation of the print job"""
        self._cancelled = True

    def run(self):
        """Execute the print job in a background thread"""
        total = len(self.pdf_files)
        success_count = 0
        error_count = 0

        for index, pdf_path in enumerate(self.pdf_files):
            # Check for cancellation
            if self._cancelled:
                break

            filename = Path(pdf_path).name

            # Notify that we're starting this file
            self.file_started.emit(index, filename)
            self.progress.emit(index + 1, total)

            # Attempt to print
            try:
                result = print_pdf(pdf_path)

                if result.success:
                    self.file_completed.emit(index, filename)
                    success_count += 1
                else:
                    self.file_error.emit(index, filename, result.error_message)
                    error_count += 1

            except Exception as e:
                self.file_error.emit(index, filename, str(e))
                error_count += 1

            # Small delay to allow print queue to process
            # and prevent overwhelming the system
            if not self._cancelled:
                self.msleep(500)

        # Emit finished signal
        self.finished.emit(success_count, error_count)

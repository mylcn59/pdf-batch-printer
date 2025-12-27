"""
Main application window with folder selection and print controls
Professional dark/light theme with modern UI
"""

import os
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QProgressBar, QFileDialog,
    QListWidget, QListWidgetItem, QMessageBox, QGroupBox,
    QStatusBar, QFrame, QSplitter, QToolBar, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSlot, QSize
from PyQt6.QtGui import QFont, QIcon, QColor, QPalette, QLinearGradient, QBrush

from core.worker import PrintWorker


# Professional dark theme stylesheet
DARK_STYLE = """
QMainWindow {
    background-color: #1a1a2e;
}

QWidget {
    background-color: #1a1a2e;
    color: #eaeaea;
    font-family: 'Segoe UI', 'Ubuntu', sans-serif;
    font-size: 13px;
}

QGroupBox {
    background-color: #16213e;
    border: 2px solid #0f3460;
    border-radius: 10px;
    margin-top: 14px;
    padding-top: 10px;
    font-weight: bold;
    font-size: 14px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 15px;
    padding: 0 8px;
    color: #00d4ff;
}

QLabel {
    background-color: transparent;
    color: #eaeaea;
}

QLabel#header {
    font-size: 22px;
    font-weight: bold;
    color: #00d4ff;
}

QLabel#subheader {
    font-size: 12px;
    color: #888;
}

QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #0f3460, stop:1 #16213e);
    color: #ffffff;
    border: 2px solid #0f3460;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
    font-size: 13px;
    min-height: 20px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #1a4a7a, stop:1 #0f3460);
    border-color: #00d4ff;
}

QPushButton:pressed {
    background: #0f3460;
}

QPushButton:disabled {
    background: #2a2a4a;
    color: #666;
    border-color: #2a2a4a;
}

QPushButton#primary {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #00d4ff, stop:1 #0099cc);
    border-color: #00d4ff;
    color: #1a1a2e;
}

QPushButton#primary:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #33ddff, stop:1 #00bbee);
}

QPushButton#primary:disabled {
    background: #2a2a4a;
    color: #666;
    border-color: #2a2a4a;
}

QPushButton#danger {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #e94560, stop:1 #c23050);
    border-color: #e94560;
}

QPushButton#danger:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #ff5070, stop:1 #e94560);
}

QPushButton#danger:disabled {
    background: #2a2a4a;
    color: #666;
    border-color: #2a2a4a;
}

QListWidget {
    background-color: #16213e;
    border: 2px solid #0f3460;
    border-radius: 8px;
    padding: 5px;
    outline: none;
}

QListWidget::item {
    background-color: #1a1a2e;
    border-radius: 6px;
    padding: 10px 12px;
    margin: 3px 2px;
    border: 1px solid transparent;
}

QListWidget::item:hover {
    background-color: #0f3460;
    border-color: #00d4ff;
}

QListWidget::item:selected {
    background-color: #0f3460;
    border-color: #00d4ff;
}

QProgressBar {
    background-color: #16213e;
    border: 2px solid #0f3460;
    border-radius: 10px;
    text-align: center;
    font-weight: bold;
    color: #eaeaea;
    min-height: 30px;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #00d4ff, stop:0.5 #00ffcc, stop:1 #00d4ff);
    border-radius: 8px;
}

QStatusBar {
    background-color: #0f3460;
    color: #00d4ff;
    border-top: 1px solid #16213e;
    font-size: 12px;
    padding: 5px;
}

QScrollBar:vertical {
    background-color: #16213e;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #0f3460;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #00d4ff;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QMessageBox {
    background-color: #1a1a2e;
}

QMessageBox QLabel {
    color: #eaeaea;
}

QMessageBox QPushButton {
    min-width: 80px;
}
"""


class MainWindow(QMainWindow):
    """Main application window with professional UI"""

    APP_NAME = "PDF Batch Printer"
    APP_VERSION = "1.0.0"
    DEVELOPER = "BK Bilgi Teknolojileri"

    def __init__(self):
        super().__init__()
        self.worker = None
        self.pdf_files = []
        self.selected_folder = None

        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        """Initialize the professional user interface"""
        self.setWindowTitle(f"{self.APP_NAME} v{self.APP_VERSION}")
        self.setMinimumSize(750, 600)
        self.resize(850, 700)

        # Apply dark theme
        self.setStyleSheet(DARK_STYLE)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header section
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setSpacing(4)
        header_layout.setContentsMargins(0, 0, 0, 10)

        title_label = QLabel(self.APP_NAME)
        title_label.setObjectName("header")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title_label)

        subtitle_label = QLabel(f"Toplu PDF Yazdırma Uygulaması  |  {self.DEVELOPER}")
        subtitle_label.setObjectName("subheader")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(subtitle_label)

        layout.addWidget(header_widget)

        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #0f3460;")
        separator.setFixedHeight(2)
        layout.addWidget(separator)

        # Folder selection group
        folder_group = QGroupBox("  Klasör Seçimi")
        folder_layout = QHBoxLayout(folder_group)
        folder_layout.setContentsMargins(15, 20, 15, 15)
        folder_layout.setSpacing(15)

        folder_icon_label = QLabel("📁")
        folder_icon_label.setStyleSheet("font-size: 24px;")
        folder_layout.addWidget(folder_icon_label)

        self.folder_label = QLabel("Henüz klasör seçilmedi...")
        self.folder_label.setStyleSheet("color: #888; font-style: italic; font-size: 13px;")
        self.folder_label.setWordWrap(True)
        folder_layout.addWidget(self.folder_label, 1)

        self.select_btn = QPushButton("  Klasör Seç")
        self.select_btn.setMinimumWidth(140)
        self.select_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        folder_layout.addWidget(self.select_btn)

        layout.addWidget(folder_group)

        # PDF list group
        list_group = QGroupBox("  PDF Dosyaları (Alfabetik Sıra)")
        list_layout = QVBoxLayout(list_group)
        list_layout.setContentsMargins(15, 20, 15, 15)
        list_layout.setSpacing(10)

        self.file_list = QListWidget()
        self.file_list.setMinimumHeight(200)
        list_layout.addWidget(self.file_list)

        # File count with icon
        count_layout = QHBoxLayout()
        count_layout.addStretch()
        self.file_count_label = QLabel("📄 0 PDF dosyası bulundu")
        self.file_count_label.setStyleSheet("color: #00d4ff; font-size: 12px;")
        count_layout.addWidget(self.file_count_label)
        list_layout.addLayout(count_layout)

        layout.addWidget(list_group, 1)

        # Progress group
        progress_group = QGroupBox("  Yazdırma Durumu")
        progress_layout = QVBoxLayout(progress_group)
        progress_layout.setContentsMargins(15, 25, 15, 15)
        progress_layout.setSpacing(12)

        # Status with icon
        status_layout = QHBoxLayout()
        self.status_icon = QLabel("⏳")
        self.status_icon.setStyleSheet("font-size: 20px;")
        status_layout.addWidget(self.status_icon)

        self.status_label = QLabel("Hazır")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        status_font = QFont()
        status_font.setPointSize(14)
        status_font.setBold(True)
        self.status_label.setFont(status_font)
        self.status_label.setStyleSheet("color: #00d4ff;")
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        progress_layout.addLayout(status_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%v / %m")
        progress_layout.addWidget(self.progress_bar)

        # Current file label
        self.current_file_label = QLabel("")
        self.current_file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.current_file_label.setStyleSheet("color: #888; font-size: 11px;")
        self.current_file_label.setWordWrap(True)
        progress_layout.addWidget(self.current_file_label)

        layout.addWidget(progress_group)

        # Control buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        self.print_btn = QPushButton("  Yazdırmayı Başlat")
        self.print_btn.setObjectName("primary")
        self.print_btn.setEnabled(False)
        self.print_btn.setMinimumHeight(50)
        self.print_btn.setMinimumWidth(200)
        self.print_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_layout.addWidget(self.print_btn)

        self.cancel_btn = QPushButton("  İptal Et")
        self.cancel_btn.setObjectName("danger")
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.setMinimumHeight(50)
        self.cancel_btn.setMinimumWidth(150)
        self.cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_layout.addWidget(self.cancel_btn)

        layout.addLayout(btn_layout)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(f"  {self.APP_NAME} | Yazdırma için bir klasör seçin")

    def setup_connections(self):
        """Connect signals to slots"""
        self.select_btn.clicked.connect(self.select_folder)
        self.print_btn.clicked.connect(self.start_printing)
        self.cancel_btn.clicked.connect(self.cancel_printing)

    def update_status_icon(self, status: str):
        """Update status icon based on state"""
        icons = {
            "ready": "⏳",
            "printing": "🖨️",
            "success": "✅",
            "error": "⚠️",
            "cancelled": "🚫"
        }
        self.status_icon.setText(icons.get(status, "⏳"))

    @pyqtSlot()
    def select_folder(self):
        """Open folder selection dialog"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "PDF Klasörü Seç",
            str(Path.home()),
            QFileDialog.Option.ShowDirsOnly
        )

        if folder:
            self.selected_folder = folder
            self.folder_label.setText(folder)
            self.folder_label.setStyleSheet("color: #00ffcc; font-size: 13px;")
            self.load_pdf_files()

    def load_pdf_files(self):
        """Load and list PDF files from selected folder"""
        self.file_list.clear()
        self.pdf_files = []

        if not self.selected_folder:
            return

        # Find all PDF files
        folder_path = Path(self.selected_folder)
        pdf_files = list(folder_path.glob("*.pdf")) + list(folder_path.glob("*.PDF"))

        # Sort alphabetically (case-insensitive)
        pdf_files.sort(key=lambda x: x.name.lower())

        self.pdf_files = [str(f) for f in pdf_files]

        # Update list widget
        for i, pdf_file in enumerate(pdf_files, 1):
            item = QListWidgetItem(f"  {i:03d}  │  {pdf_file.name}")
            self.file_list.addItem(item)

        count = len(self.pdf_files)
        self.file_count_label.setText(f"📄 {count} PDF dosyası bulundu")

        # Enable/disable print button
        self.print_btn.setEnabled(count > 0)

        if count == 0:
            self.status_bar.showMessage("  ⚠️ Seçilen klasörde PDF dosyası bulunamadı")
            self.file_count_label.setStyleSheet("color: #e94560; font-size: 12px;")
        else:
            self.status_bar.showMessage(f"  ✅ {count} PDF dosyası yazdırılmaya hazır")
            self.file_count_label.setStyleSheet("color: #00ffcc; font-size: 12px;")

    @pyqtSlot()
    def start_printing(self):
        """Start the batch printing process"""
        if not self.pdf_files:
            return

        # Confirm before starting
        reply = QMessageBox.question(
            self,
            "Yazdırmayı Onayla",
            f"📄 {len(self.pdf_files)} PDF dosyası yazdırılacak.\n\n"
            "Devam etmek istiyor musunuz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        # Update UI state
        self.select_btn.setEnabled(False)
        self.print_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(len(self.pdf_files))
        self.update_status_icon("printing")

        # Reset list item styles
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            item.setBackground(QColor("transparent"))

        # Create and start worker thread
        self.worker = PrintWorker(self.pdf_files)
        self.worker.progress.connect(self.on_progress)
        self.worker.file_started.connect(self.on_file_started)
        self.worker.file_completed.connect(self.on_file_completed)
        self.worker.file_error.connect(self.on_file_error)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

        self.status_bar.showMessage("  🖨️ Yazdırma işlemi başlatıldı...")

    @pyqtSlot()
    def cancel_printing(self):
        """Cancel the ongoing print operation"""
        if self.worker and self.worker.isRunning():
            reply = QMessageBox.question(
                self,
                "İptal Onayı",
                "🚫 Yazdırma işlemi iptal edilecek.\n\n"
                "Devam etmek istiyor musunuz?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                self.worker.cancel()
                self.status_label.setText("İptal ediliyor...")
                self.update_status_icon("cancelled")
                self.status_bar.showMessage("  🚫 Yazdırma iptal ediliyor...")

    @pyqtSlot(int, int)
    def on_progress(self, current: int, total: int):
        """Update progress bar"""
        self.progress_bar.setValue(current)
        self.status_label.setText(f"{current} / {total} yazdırılıyor")

    @pyqtSlot(int, str)
    def on_file_started(self, index: int, filename: str):
        """Highlight current file being printed"""
        self.current_file_label.setText(f"🖨️ Yazdırılıyor: {filename}")

        # Highlight item in list
        if index < self.file_list.count():
            item = self.file_list.item(index)
            item.setBackground(QColor("#0f3460"))
            self.file_list.scrollToItem(item)

    @pyqtSlot(int, str)
    def on_file_completed(self, index: int, filename: str):
        """Mark file as completed"""
        if index < self.file_list.count():
            item = self.file_list.item(index)
            item.setBackground(QColor("#1a4a3a"))
            original_text = item.text()
            # Extract filename and add checkmark
            parts = original_text.split("│")
            if len(parts) == 2:
                item.setText(f"  ✅  │{parts[1]}")

    @pyqtSlot(int, str, str)
    def on_file_error(self, index: int, filename: str, error: str):
        """Mark file as failed"""
        if index < self.file_list.count():
            item = self.file_list.item(index)
            item.setBackground(QColor("#4a1a1a"))
            original_text = item.text()
            parts = original_text.split("│")
            if len(parts) == 2:
                item.setText(f"  ❌  │{parts[1]}")
            item.setToolTip(f"Hata: {error}")

        self.status_bar.showMessage(f"  ⚠️ Hata: {filename} - {error}")

    @pyqtSlot(int, int)
    def on_finished(self, success_count: int, error_count: int):
        """Handle print job completion"""
        # Reset UI state
        self.select_btn.setEnabled(True)
        self.print_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)

        self.current_file_label.setText("")

        if error_count == 0:
            self.status_label.setText(f"Tamamlandı! ({success_count} dosya)")
            self.status_label.setStyleSheet("color: #00ffcc;")
            self.update_status_icon("success")
            self.status_bar.showMessage(
                f"  ✅ Yazdırma tamamlandı: {success_count} dosya başarıyla yazdırıldı"
            )
            QMessageBox.information(
                self,
                "Yazdırma Tamamlandı",
                f"✅ {success_count} PDF dosyası başarıyla yazdırıldı."
            )
        else:
            self.status_label.setText(f"Tamamlandı ({success_count} başarılı, {error_count} hata)")
            self.status_label.setStyleSheet("color: #e94560;")
            self.update_status_icon("error")
            self.status_bar.showMessage(
                f"  ⚠️ Yazdırma tamamlandı: {success_count} başarılı, {error_count} hatalı"
            )
            QMessageBox.warning(
                self,
                "Yazdırma Tamamlandı",
                f"⚠️ Yazdırma tamamlandı.\n\n"
                f"✅ Başarılı: {success_count}\n"
                f"❌ Hatalı: {error_count}\n\n"
                f"Hatalı dosyalar için listeye bakın."
            )

        self.worker = None

    def closeEvent(self, event):
        """Handle window close event"""
        if self.worker and self.worker.isRunning():
            reply = QMessageBox.question(
                self,
                "Çıkış Onayı",
                "🖨️ Yazdırma işlemi devam ediyor.\n\n"
                "Çıkmak istediğinizden emin misiniz?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                self.worker.cancel()
                self.worker.wait()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

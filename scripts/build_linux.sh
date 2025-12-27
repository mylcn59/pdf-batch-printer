#!/bin/bash
# Build script for Linux
# Generates standalone binary and .deb package

set -e

echo "========================================"
echo "PDF Batch Printer - Linux Build"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python3 bulunamadi!${NC}"
    exit 1
fi

echo "Python: $(python3 --version)"

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "Virtual environment olusturuluyor..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Bagimliliklar yukleniyor..."
pip install -q -r requirements.txt

# Clean previous builds
echo "Onceki build temizleniyor..."
rm -rf build dist

# Build with PyInstaller
echo "PyInstaller ile derleniyor..."
pyinstaller --clean pdf_batch_printer.spec

if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Build basarisiz!${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}========================================"
echo "Binary build tamamlandi!"
echo "Executable: dist/PDFBatchPrinter"
echo -e "========================================${NC}"

# Build .deb package
echo ""
echo ".deb paketi olusturuluyor..."

DEB_DIR="installer/linux/deb"
VERSION="1.0.0"

# Copy binary to deb structure
cp dist/PDFBatchPrinter "$DEB_DIR/usr/bin/pdf-batch-printer"
chmod +x "$DEB_DIR/usr/bin/pdf-batch-printer"

# Set permissions for control scripts
chmod 755 "$DEB_DIR/DEBIAN/postinst"
chmod 755 "$DEB_DIR/DEBIAN/postrm"

# Create .deb package
mkdir -p dist/installer
dpkg-deb --build "$DEB_DIR" "dist/installer/pdf-batch-printer_${VERSION}_amd64.deb"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}========================================"
    echo ".deb paketi olusturuldu!"
    echo "Package: dist/installer/pdf-batch-printer_${VERSION}_amd64.deb"
    echo ""
    echo "Kurulum icin:"
    echo "  sudo dpkg -i dist/installer/pdf-batch-printer_${VERSION}_amd64.deb"
    echo -e "========================================${NC}"
else
    echo -e "${YELLOW}UYARI: .deb paketi olusturulamadi${NC}"
    echo "Standalone binary kullanilabilir: dist/PDFBatchPrinter"
fi

echo ""
echo "Build tamamlandi!"

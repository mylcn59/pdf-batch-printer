#!/bin/bash
# PDF Batch Printer - Otomatik Kurulum Scripti
# Tek komutla kur ve çalıştır!

set -e

# Renkler
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════╗"
echo "║     PDF Batch Printer - Kurulum            ║"
echo "╚════════════════════════════════════════════╝"
echo -e "${NC}"

# Kurulum dizini
INSTALL_DIR="$HOME/.local/share/pdf-batch-printer"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"

# Fonksiyonlar
check_and_install() {
    local pkg=$1
    local cmd=${2:-$1}

    if ! command -v $cmd &> /dev/null; then
        echo -e "${YELLOW}► $pkg kuruluyor...${NC}"
        sudo apt-get install -y $pkg
    else
        echo -e "${GREEN}✓ $pkg mevcut${NC}"
    fi
}

# Sudo şifresini başta bir kez al
echo -e "${YELLOW}Sistem paketleri için sudo şifresi gerekebilir...${NC}"
sudo -v

# Gerekli paketleri kur
echo ""
echo -e "${BLUE}[1/5] Sistem bağımlılıkları kontrol ediliyor...${NC}"

sudo apt-get update -qq

check_and_install "python3" "python3"
check_and_install "python3-pip" "pip3"
check_and_install "python3-venv"
check_and_install "cups" "lpstat"
check_and_install "libxcb-cursor0"

# Git ile projeyi indir veya güncelle
echo ""
echo -e "${BLUE}[2/5] Uygulama indiriliyor...${NC}"

mkdir -p "$INSTALL_DIR"

if [ -d "$INSTALL_DIR/.git" ]; then
    echo "Güncelleniyor..."
    cd "$INSTALL_DIR"
    git pull --quiet
else
    echo "İndiriliyor..."
    rm -rf "$INSTALL_DIR"
    git clone --quiet https://github.com/mylcn59/pdf-batch-printer.git "$INSTALL_DIR"
fi

cd "$INSTALL_DIR"

# Virtual environment oluştur
echo ""
echo -e "${BLUE}[3/5] Python ortamı hazırlanıyor...${NC}"

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# Çalıştırma scripti oluştur
echo ""
echo -e "${BLUE}[4/5] Kısayollar oluşturuluyor...${NC}"

mkdir -p "$BIN_DIR"

cat > "$BIN_DIR/pdf-batch-printer" << 'EOF'
#!/bin/bash
cd "$HOME/.local/share/pdf-batch-printer"
source venv/bin/activate
python src/main.py "$@"
EOF

chmod +x "$BIN_DIR/pdf-batch-printer"

# PATH'e ekle
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    export PATH="$BIN_DIR:$PATH"
fi

# Masaüstü kısayolu oluştur
mkdir -p "$DESKTOP_DIR"

cat > "$DESKTOP_DIR/pdf-batch-printer.desktop" << EOF
[Desktop Entry]
Name=PDF Batch Printer
Comment=Toplu PDF Yazdırma Uygulaması
Exec=$BIN_DIR/pdf-batch-printer
Icon=$INSTALL_DIR/assets/icon.png
Terminal=false
Type=Application
Categories=Utility;Office;
Keywords=pdf;print;batch;yazdır;
EOF

chmod +x "$DESKTOP_DIR/pdf-batch-printer.desktop"

# Desktop cache güncelle
update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true

echo ""
echo -e "${BLUE}[5/5] Kurulum tamamlandı!${NC}"
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════╗"
echo -e "║  ✓ PDF Batch Printer başarıyla kuruldu!   ║"
echo -e "╚════════════════════════════════════════════╝${NC}"
echo ""
echo -e "Çalıştırmak için:"
echo -e "  ${YELLOW}pdf-batch-printer${NC}  (terminalde)"
echo -e "  veya uygulama menüsünden 'PDF Batch Printer' arayın"
echo ""

# Hemen çalıştırmak ister misin?
read -p "Şimdi çalıştırılsın mı? [E/h]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Ee]?$ ]]; then
    echo -e "${GREEN}Uygulama başlatılıyor...${NC}"
    "$BIN_DIR/pdf-batch-printer" &
fi

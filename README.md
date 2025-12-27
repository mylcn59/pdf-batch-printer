# PDF Batch Printer

<p align="center">
  <img src="assets/screenshot.png" alt="PDF Batch Printer" width="600">
</p>

<p align="center">
  <strong>Toplu PDF Yazdırma Uygulaması</strong><br>
  Windows ve Linux'ta çalışan, profesyonel arayüzlü masaüstü uygulaması
</p>

<p align="center">
  <a href="#özellikler">Özellikler</a> •
  <a href="#kurulum">Kurulum</a> •
  <a href="#kullanım">Kullanım</a> •
  <a href="#geliştirme">Geliştirme</a>
</p>

---

## Özellikler

- **Toplu Yazdırma**: Klasör seçerek tüm PDF dosyalarını tek seferde yazdırın
- **Alfabetik Sıralama**: PDF'ler otomatik olarak A-Z sırasına göre yazdırılır
- **Gerçek Zamanlı Progress**: Yazdırma durumunu anlık takip edin (2/165 yazdırılıyor)
- **Modern Arayüz**: Profesyonel dark theme tasarım
- **Çoklu Platform**: Windows ve Linux desteği
- **Hata Toleransı**: Bozuk PDF'lerde uygulama çökmeden devam eder
- **Bağımsız Çalışma**: Python veya başka bir yazılım kurulumu gerektirmez

## Kurulum

### Windows

1. [Releases](https://github.com/mylcn59/pdf-batch-printer/releases) sayfasından `PDFBatchPrinter_Setup_1.0.0.exe` dosyasını indirin
2. İndirilen dosyayı çalıştırın
3. Kurulum sihirbazını takip edin
4. Masaüstündeki veya Başlat menüsündeki kısayoldan uygulamayı başlatın

### Linux (.deb - Ubuntu/Debian)

```bash
# İndirme
wget https://github.com/mylcn59/pdf-batch-printer/releases/download/v1.0.0/pdf-batch-printer_1.0.0_amd64.deb

# Kurulum
sudo dpkg -i pdf-batch-printer_1.0.0_amd64.deb

# Çalıştırma
pdf-batch-printer
```

### Linux (Standalone Binary)

```bash
# İndirme
wget https://github.com/mylcn59/pdf-batch-printer/releases/download/v1.0.0/PDFBatchPrinter-linux

# Çalıştırılabilir yapma
chmod +x PDFBatchPrinter-linux

# Çalıştırma
./PDFBatchPrinter-linux
```

## Kullanım

1. **Klasör Seç** butonuna tıklayın
2. PDF dosyalarının bulunduğu klasörü seçin
3. Dosya listesini kontrol edin (alfabetik sırayla listelenir)
4. **Yazdırmayı Başlat** butonuna tıklayın
5. Yazdırma tamamlanana kadar progress bar'ı takip edin

### Sistem Gereksinimleri

| Platform | Gereksinim |
|----------|------------|
| **Windows** | Windows 10/11, SumatraPDF veya Adobe Reader (önerilen) |
| **Linux** | CUPS kurulu olmalı (`sudo apt install cups`) |

## Geliştirme

### Kaynak Koddan Çalıştırma

```bash
# Repo'yu klonla
git clone https://github.com/mylcn59/pdf-batch-printer.git
cd pdf-batch-printer

# Virtual environment oluştur
python3 -m venv venv
source venv/bin/activate  # Linux
# veya: venv\Scripts\activate  # Windows

# Bağımlılıkları yükle
pip install -r requirements.txt

# Çalıştır
cd src
python main.py
```

### Build (Derleme)

#### Windows
```batch
scripts\build_windows.bat
```

#### Linux
```bash
./scripts/build_linux.sh
```

### Proje Yapısı

```
pdf-batch-printer/
├── src/
│   ├── main.py              # Giriş noktası
│   ├── gui/
│   │   └── main_window.py   # Ana pencere (PyQt6)
│   └── core/
│       ├── worker.py        # Background thread
│       └── printer.py       # Platform-specific yazdırma
├── installer/
│   ├── windows/             # Inno Setup script
│   └── linux/               # Deb paket dosyaları
├── scripts/
│   ├── build_windows.bat
│   └── build_linux.sh
└── requirements.txt
```

## Mimari

```
┌─────────────────────────────────────────────────────────┐
│                   MainWindow (PyQt6)                     │
│   • Klasör seçimi ve PDF listeleme                      │
│   • Progress bar ve durum göstergesi                    │
│   • Modern dark theme arayüz                            │
└─────────────────────────┬───────────────────────────────┘
                          │ QThread (Background)
┌─────────────────────────▼───────────────────────────────┐
│                    PrintWorker                           │
│   • PDF'leri sırayla işleme                             │
│   • Hata yakalama ve raporlama                          │
│   • İptal desteği                                       │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                   Printer Module                         │
│  ┌──────────────────┐  ┌──────────────────┐            │
│  │     Windows      │  │      Linux       │            │
│  │  • SumatraPDF    │  │  • lp (CUPS)     │            │
│  │  • Adobe Reader  │  │  • lpr           │            │
│  │  • ShellExecute  │  │                  │            │
│  └──────────────────┘  └──────────────────┘            │
└─────────────────────────────────────────────────────────┘
```

## Teknoloji Stack

| Bileşen | Teknoloji |
|---------|-----------|
| GUI | PyQt6 |
| Threading | QThread |
| Windows Yazdırma | SumatraPDF / Adobe Reader |
| Linux Yazdırma | CUPS (lp/lpr) |
| Build | PyInstaller 6.x |
| Windows Installer | Inno Setup 6 |
| Linux Paket | dpkg-deb |

## Lisans

MIT License - Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## Geliştirici

**BK Bilgi Teknolojileri**

---

<p align="center">
  Made with ❤️ by BK Bilgi Teknolojileri
</p>

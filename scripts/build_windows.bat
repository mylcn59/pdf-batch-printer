@echo off
REM Build script for Windows
REM Generates single-file .exe using PyInstaller

echo ========================================
echo PDF Batch Printer - Windows Build
echo ========================================

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python bulunamadi!
    exit /b 1
)

REM Create virtual environment if not exists
if not exist "venv" (
    echo Virtual environment olusturuluyor...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Bagimliliklar yukleniyor...
pip install -q -r requirements.txt

REM Clean previous builds
echo Onceki build temizleniyor...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul

REM Build with PyInstaller
echo PyInstaller ile derleniyor...
pyinstaller --clean pdf_batch_printer.spec

if errorlevel 1 (
    echo ERROR: Build basarisiz!
    exit /b 1
)

echo.
echo ========================================
echo Build tamamlandi!
echo Executable: dist\PDFBatchPrinter.exe
echo ========================================

REM Check if Inno Setup is installed
if exist "%PROGRAMFILES(X86)%\Inno Setup 6\ISCC.exe" (
    echo.
    echo Installer olusturuluyor...
    "%PROGRAMFILES(X86)%\Inno Setup 6\ISCC.exe" installer\windows\installer.iss
    echo Installer: dist\installer\PDFBatchPrinter_Setup_1.0.0.exe
) else (
    echo.
    echo UYARI: Inno Setup bulunamadi.
    echo Installer olusturmak icin Inno Setup 6 yukleyin.
)

pause

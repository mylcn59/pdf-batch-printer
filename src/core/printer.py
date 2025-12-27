"""
Platform-specific PDF printing utilities
Supports Windows (via SumatraPDF/Adobe Reader) and Linux (via CUPS/lp)
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from dataclasses import dataclass


@dataclass
class PrintResult:
    """Result of a print operation"""
    success: bool
    error_message: str = ""


def get_platform() -> str:
    """Get current platform identifier"""
    if sys.platform.startswith("win"):
        return "windows"
    elif sys.platform.startswith("linux"):
        return "linux"
    elif sys.platform.startswith("darwin"):
        return "macos"
    else:
        return "unknown"


def print_pdf(pdf_path: str) -> PrintResult:
    """
    Print a PDF file using platform-appropriate method.

    Args:
        pdf_path: Full path to the PDF file

    Returns:
        PrintResult with success status and any error message
    """
    # Validate file exists
    if not os.path.isfile(pdf_path):
        return PrintResult(False, f"Dosya bulunamadı: {pdf_path}")

    platform = get_platform()

    if platform == "windows":
        return _print_windows(pdf_path)
    elif platform == "linux":
        return _print_linux(pdf_path)
    elif platform == "macos":
        return _print_macos(pdf_path)
    else:
        return PrintResult(False, f"Desteklenmeyen platform: {platform}")


def _print_windows(pdf_path: str) -> PrintResult:
    """
    Print PDF on Windows using available methods.

    Priority:
    1. SumatraPDF (lightweight, silent printing)
    2. Adobe Reader (if installed)
    3. Windows print command (ShellExecute)
    """
    pdf_path = os.path.abspath(pdf_path)

    # Method 1: Try SumatraPDF (best for silent printing)
    sumatra_paths = [
        r"C:\Program Files\SumatraPDF\SumatraPDF.exe",
        r"C:\Program Files (x86)\SumatraPDF\SumatraPDF.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\SumatraPDF\SumatraPDF.exe"),
    ]

    for sumatra_path in sumatra_paths:
        if os.path.isfile(sumatra_path):
            try:
                # -print-to-default: print to default printer
                # -silent: no GUI
                result = subprocess.run(
                    [sumatra_path, "-print-to-default", "-silent", pdf_path],
                    capture_output=True,
                    timeout=60,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                if result.returncode == 0:
                    return PrintResult(True)
            except subprocess.TimeoutExpired:
                return PrintResult(False, "Yazdırma zaman aşımına uğradı")
            except Exception as e:
                pass  # Try next method

    # Method 2: Try Adobe Reader
    adobe_paths = [
        r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe",
        r"C:\Program Files (x86)\Adobe\Acrobat DC\Acrobat\Acrobat.exe",
        r"C:\Program Files\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe",
        r"C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe",
        r"C:\Program Files\Adobe\Reader 11.0\Reader\AcroRd32.exe",
        r"C:\Program Files (x86)\Adobe\Reader 11.0\Reader\AcroRd32.exe",
    ]

    for adobe_path in adobe_paths:
        if os.path.isfile(adobe_path):
            try:
                # /t: print to default printer and exit
                result = subprocess.run(
                    [adobe_path, "/t", pdf_path],
                    capture_output=True,
                    timeout=60,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                # Adobe Reader may return non-zero but still print successfully
                return PrintResult(True)
            except subprocess.TimeoutExpired:
                return PrintResult(False, "Yazdırma zaman aşımına uğradı")
            except Exception as e:
                pass  # Try next method

    # Method 3: Use Windows ShellExecute with "print" verb
    try:
        import ctypes
        from ctypes import wintypes

        shell32 = ctypes.windll.shell32
        result = shell32.ShellExecuteW(
            None,  # hwnd
            "print",  # operation
            pdf_path,  # file
            None,  # parameters
            None,  # directory
            0  # SW_HIDE
        )
        # ShellExecute returns > 32 on success
        if result > 32:
            return PrintResult(True)
        else:
            return PrintResult(False, f"ShellExecute hatası: {result}")
    except Exception as e:
        return PrintResult(False, f"Windows yazdırma hatası: {str(e)}")


def _print_linux(pdf_path: str) -> PrintResult:
    """
    Print PDF on Linux using CUPS (lp command).
    """
    pdf_path = os.path.abspath(pdf_path)

    # Check if lp command is available
    if not shutil.which("lp"):
        # Try lpr as fallback
        if not shutil.which("lpr"):
            return PrintResult(False, "lp veya lpr komutu bulunamadı. CUPS kurulu mu?")

        # Use lpr
        try:
            result = subprocess.run(
                ["lpr", pdf_path],
                capture_output=True,
                timeout=30,
                text=True
            )
            if result.returncode == 0:
                return PrintResult(True)
            else:
                error = result.stderr.strip() if result.stderr else "Bilinmeyen hata"
                return PrintResult(False, f"lpr hatası: {error}")
        except subprocess.TimeoutExpired:
            return PrintResult(False, "Yazdırma zaman aşımına uğradı")
        except Exception as e:
            return PrintResult(False, f"lpr hatası: {str(e)}")

    # Use lp (preferred)
    try:
        result = subprocess.run(
            ["lp", pdf_path],
            capture_output=True,
            timeout=30,
            text=True
        )
        if result.returncode == 0:
            return PrintResult(True)
        else:
            error = result.stderr.strip() if result.stderr else "Bilinmeyen hata"
            return PrintResult(False, f"lp hatası: {error}")
    except subprocess.TimeoutExpired:
        return PrintResult(False, "Yazdırma zaman aşımına uğradı")
    except Exception as e:
        return PrintResult(False, f"lp hatası: {str(e)}")


def _print_macos(pdf_path: str) -> PrintResult:
    """
    Print PDF on macOS using lpr command.
    """
    pdf_path = os.path.abspath(pdf_path)

    try:
        result = subprocess.run(
            ["lpr", pdf_path],
            capture_output=True,
            timeout=30,
            text=True
        )
        if result.returncode == 0:
            return PrintResult(True)
        else:
            error = result.stderr.strip() if result.stderr else "Bilinmeyen hata"
            return PrintResult(False, f"lpr hatası: {error}")
    except subprocess.TimeoutExpired:
        return PrintResult(False, "Yazdırma zaman aşımına uğradı")
    except Exception as e:
        return PrintResult(False, f"lpr hatası: {str(e)}")


def get_default_printer() -> str | None:
    """
    Get the name of the default printer.
    Returns None if no default printer is set.
    """
    platform = get_platform()

    if platform == "windows":
        try:
            import ctypes
            from ctypes import wintypes

            winspool = ctypes.WinDLL("winspool.drv")
            GetDefaultPrinterW = winspool.GetDefaultPrinterW
            GetDefaultPrinterW.argtypes = [wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD)]
            GetDefaultPrinterW.restype = wintypes.BOOL

            size = wintypes.DWORD(0)
            GetDefaultPrinterW(None, ctypes.byref(size))

            if size.value > 0:
                buffer = ctypes.create_unicode_buffer(size.value)
                if GetDefaultPrinterW(buffer, ctypes.byref(size)):
                    return buffer.value
        except Exception:
            pass
        return None

    elif platform in ("linux", "macos"):
        try:
            result = subprocess.run(
                ["lpstat", "-d"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                # Output format: "system default destination: PRINTER_NAME"
                output = result.stdout.strip()
                if ":" in output:
                    return output.split(":")[-1].strip()
        except Exception:
            pass
        return None

    return None


def check_print_system() -> tuple[bool, str]:
    """
    Check if the print system is properly configured.

    Returns:
        Tuple of (is_ready, message)
    """
    platform = get_platform()

    if platform == "windows":
        # Check if any print method is available
        sumatra_available = any(
            os.path.isfile(p) for p in [
                r"C:\Program Files\SumatraPDF\SumatraPDF.exe",
                r"C:\Program Files (x86)\SumatraPDF\SumatraPDF.exe",
            ]
        )
        return (True, "Windows yazdırma sistemi hazır")

    elif platform == "linux":
        if shutil.which("lp") or shutil.which("lpr"):
            printer = get_default_printer()
            if printer:
                return (True, f"CUPS hazır. Varsayılan yazıcı: {printer}")
            else:
                return (False, "Varsayılan yazıcı ayarlanmamış")
        else:
            return (False, "CUPS kurulu değil (lp/lpr bulunamadı)")

    elif platform == "macos":
        if shutil.which("lpr"):
            return (True, "macOS yazdırma sistemi hazır")
        else:
            return (False, "lpr komutu bulunamadı")

    return (False, f"Desteklenmeyen platform: {platform}")

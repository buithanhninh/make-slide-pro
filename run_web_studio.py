"""
run_web_studio.py
Make Slide Pro Web Studio V7.3 - Launcher & Server Host
Starts the FastAPI server with Uvicorn and automatically launches the web browser.
"""

import os
import sys
import time
import webbrowser
import threading
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

PORT = 8000
HOST = "127.0.0.1"
URL = f"http://{HOST}:{PORT}"


def open_browser():
    time.sleep(1.5)
    print(f"\n[Make Slide Pro Studio] Đang mở trình duyệt tại: {URL}")
    webbrowser.open(URL)


def main():
    print("=" * 80)
    print("       * MAKE SLIDE PRO V7.3 - WEB STUDIO LAUNCHER *")
    print("   Universal Document-to-PowerPoint Web Publishing & Presentation Suite")
    print("=" * 80)
    print(f"[*] Thư mục dự án: {PROJECT_ROOT}")
    print(f"[*] Máy chủ Web Studio: {URL}")
    print("[*] Nhấn Ctrl + C trong cửa sổ này khi muốn dừng máy chủ.\n")

    # Launch browser in background thread
    threading.Thread(target=open_browser, daemon=True).start()

    try:
        import uvicorn
        uvicorn.run("web.app:app", host=HOST, port=PORT, log_level="info", reload=False)
    except KeyboardInterrupt:
        print("\n[Make Slide Pro Studio] Đã dừng máy chủ Web Studio.")
    except Exception as e:
        print(f"\n[LỖI] Không thể khởi động máy chủ: {e}")
        input("Nhấn Enter để thoát...")


if __name__ == "__main__":
    main()

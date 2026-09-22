# -*- coding: utf-8 -*-
"""
scripts/export_v91_visual_artifacts.py
Exports high-resolution PNG snapshots of V9.1 visual slides (EDITORIAL_HERO & CHART_AND_INSIGHTS)
directly into the brain artifacts directory for visual verification.
"""

from __future__ import annotations

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import win32com.client
import pythoncom

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "Du_An_Outputs" / "A_Tuan_Dan_So_2"
ARTIFACTS_DIR = Path(r"C:\Users\HP\.gemini\antigravity\brain\a1c6c6ec-eb4c-4dbc-b9d2-b0f5fb78a606")

SLIDES_TO_EXPORT = [
    ("BÀI 1. Tổng quan về dịch vụ dân số - Dark.pptx", [1, 4, 13, 14, 21], "v91_bai1"),
    ("BÀI 2. DỊCH VỤ TƯ VẤN, KHÁM SỨC KHỎE TRƯỚC KHI KẾT HÔN - Dark.pptx", [4, 14], "v91_bai2"),
    ("BÀI 6. DỊCH VỤ CHĂM SÓC SỨC KHỎE NGƯỜI CAO TUỔI - Dark.pptx", [4, 13, 14], "v91_bai6"),
]


def main():
    print("================================================================================")
    print("      MAKE SLIDE PRO V9.1 - EXPORT VISUAL SLIDES TO ARTIFACTS DIRECTORY         ")
    print("================================================================================")

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    pythoncom.CoInitialize()
    ppt = win32com.client.Dispatch("PowerPoint.Application")
    ppt.Visible = 1

    try:
        for deck_name, slide_nums, prefix in SLIDES_TO_EXPORT:
            deck_path = OUTPUT_DIR / deck_name
            if not deck_path.exists():
                print(f"Skipping {deck_name} (file not found)")
                continue

            print(f"\nProcessing deck: {deck_name}")
            pres = ppt.Presentations.Open(str(deck_path.resolve()), True, False, False)
            total = pres.Slides.Count

            for s_num in slide_nums:
                if 1 <= s_num <= total:
                    slide = pres.Slides(s_num)
                    out_png = ARTIFACTS_DIR / f"{prefix}_slide_{s_num:02d}.png"
                    slide.Export(str(out_png.resolve()), "PNG", 1920, 1080)
                    print(f"  ✔ Exported Slide {s_num:02d} -> {out_png.name}")
                else:
                    print(f"  ⚠ Slide {s_num:02d} out of range (total: {total})")

            pres.Close()
    finally:
        ppt.Quit()
        pythoncom.CoUninitialize()

    print("\nVisual export completed successfully!")


if __name__ == "__main__":
    main()

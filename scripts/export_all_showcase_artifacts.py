# -*- coding: utf-8 -*-
"""
scripts/export_all_showcase_artifacts.py
Exports high-resolution showcase PNGs for Chuyên Đề and all 6 Bài presentations
directly into the conversation artifact directory for visual inspection and walkthrough.
"""

from __future__ import annotations
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

import win32com.client
import pythoncom

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ARTIFACT_DIR = Path(r"C:\Users\ANHOME\.gemini\antigravity\brain\a1c6c6ec-eb4c-4dbc-b9d2-b0f5fb78a606")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

DECKS = [
    {
        "name": "Chuyen_De",
        "path": PROJECT_ROOT / "Du_An_Outputs" / "Chuyên đề. Điều chỉnh mức sinh - Dark.pptx",
        "slides": [1, 10, 24, 52, 70, 90]
    },
    {
        "name": "Bai_1",
        "path": PROJECT_ROOT / "Du_An_Outputs" / "A_Tuan_Dan_So_2" / "BÀI 1. Tổng quan về dịch vụ dân số - Dark.pptx",
        "slides": [1, 5, 25, 50]
    },
    {
        "name": "Bai_2",
        "path": PROJECT_ROOT / "Du_An_Outputs" / "A_Tuan_Dan_So_2" / "BÀI 2. DỊCH VỤ TƯ VẤN, KHÁM SỨC KHỎE TRƯỚC KHI KẾT HÔN - Dark.pptx",
        "slides": [1, 5, 25, 50]
    },
    {
        "name": "Bai_3",
        "path": PROJECT_ROOT / "Du_An_Outputs" / "A_Tuan_Dan_So_2" / "Bài 3. Dịch vụ DS KHHGĐ - Dark.pptx",
        "slides": [1, 5, 25, 51]
    },
    {
        "name": "Bai_4",
        "path": PROJECT_ROOT / "Du_An_Outputs" / "A_Tuan_Dan_So_2" / "Bài 4. Dịch vụ CSSKSS vị thành niên-thanh niên - Dark.pptx",
        "slides": [1, 5, 25, 50]
    },
    {
        "name": "Bai_5",
        "path": PROJECT_ROOT / "Du_An_Outputs" / "A_Tuan_Dan_So_2" / "BÀI 5. DỊCH VỤ TƯ VẤN-TẦM SOÁT-CHẨN ĐOÁN MỘT SỐ BỆNH-TẬT TRƯỚC SINH VÀ SƠ SINH - Dark.pptx",
        "slides": [1, 5, 25, 50]
    },
    {
        "name": "Bai_6",
        "path": PROJECT_ROOT / "Du_An_Outputs" / "A_Tuan_Dan_So_2" / "BÀI 6. DỊCH VỤ CHĂM SÓC SỨC KHỎE NGƯỜI CAO TUỔI - Dark.pptx",
        "slides": [1, 5, 25, 50]
    }
]

def main():
    pythoncom.CoInitialize()
    app = win32com.client.Dispatch("PowerPoint.Application")
    exported = []

    print("Exporting showcase PNGs...")
    for deck in DECKS:
        deck_path = deck["path"]
        if not deck_path.exists():
            print(f"File not found: {deck_path}")
            continue

        print(f"\nProcessing: {deck_path.name}")
        pres = app.Presentations.Open(str(deck_path), WithWindow=False)
        total = pres.Slides.Count

        for s_num in deck["slides"]:
            if 1 <= s_num <= total:
                slide = pres.Slides(s_num)
                out_name = f"showcase_{deck['name'].lower()}_slide_{s_num:02d}.png"
                out_png = ARTIFACT_DIR / out_name
                slide.Export(str(out_png), "PNG", 1920, 1080)
                exported.append(str(out_png))
                print(f"  ✔ Exported slide {s_num:02d} -> {out_name}")

        pres.Close()

    print(f"\nSuccessfully exported {len(exported)} showcase slides to: {ARTIFACT_DIR}")

if __name__ == "__main__":
    main()

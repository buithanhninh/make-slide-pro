# export_showcase_slides.py
# Exports high-resolution PNG previews of the newly upgraded slides (Formula Cards, Native Tables, Publication Charts)

import os
import sys
from pathlib import Path
import win32com.client

ARTIFACT_DIR = Path(r"C:\Users\HP\.gemini\antigravity\brain\a1c6c6ec-eb4c-4dbc-b9d2-b0f5fb78a606")
USER_DIR = Path("Du An/A Tuan Dan So")

TARGETS = [
    # (Deck name, Slide num, Output filename)
    ("Bai 1. Nhap mon DSH - Dark.pptx", 1, "v72_cover_dark_b1s01.png"),
    ("Bai 1. Nhap mon DSH - Light.pptx", 1, "v72_cover_light_b1s01.png"),
    ("Bai 1. Nhap mon DSH - Dark.pptx", 3, "v72_editorial_hero_dark_b1s03.png"),
    ("Bai 1. Nhap mon DSH - Light.pptx", 3, "v72_editorial_hero_light_b1s03.png"),
    ("Bai 1. Nhap mon DSH - Dark.pptx", 4, "v72_chart_system_dark_b1s04.png"),
    ("Bai 1. Nhap mon DSH - Light.pptx", 4, "v72_chart_system_light_b1s04.png"),
    ("Bai 2. Quy mo-Co cau-Chat luong DS - Dark.pptx", 4, "v72_formula_hero_dark_b2s04.png"),
    ("Bai 2. Quy mo-Co cau-Chat luong DS - Light.pptx", 4, "v72_formula_hero_light_b2s04.png"),
    ("Bai 2. Quy mo-Co cau-Chat luong DS - Dark.pptx", 18, "v72_native_table_dark_b2s18.png"),
    ("Bai 2. Quy mo-Co cau-Chat luong DS - Light.pptx", 18, "v72_native_table_light_b2s18.png"),
    ("Bai 2. Quy mo-Co cau-Chat luong DS - Dark.pptx", 23, "v72_chart_hdi_dark_b2s23.png"),
    ("Bai 3. Bien dong dan so tu nhien - Dark.pptx", 7, "v72_formula_tfr_dark_b3s07.png"),
    ("Bai 3. Bien dong dan so tu nhien - Dark.pptx", 17, "v72_native_life_table_dark_b3s17.png"),
    ("Bai 3. Bien dong dan so tu nhien - Dark.pptx", 21, "v72_chart_transition_dark_b3s21.png"),
    ("Bai 4. Phan bo DS va Di dan-Do thi hoa - Dark.pptx", 6, "v72_native_table_regions_dark_b4s06.png"),
    ("Bai 4. Phan bo DS va Di dan-Do thi hoa - Dark.pptx", 18, "v72_chart_urban_scurve_dark_b4s18.png"),
    ("Bai 5. Du bao dan so - Dark.pptx", 14, "v72_native_table_scenarios_dark_b5s14.png"),
]

def main():
    ppt = win32com.client.DispatchEx("PowerPoint.Application")
    try:
        for deck_name, s_idx, out_name in TARGETS:
            deck_path = USER_DIR / deck_name
            if not deck_path.exists():
                print(f"Skipping {deck_name}, not found.")
                continue
            pres = ppt.Presentations.Open(str(deck_path.resolve()), ReadOnly=True, Untitled=False, WithWindow=False)
            try:
                slide = pres.Slides(s_idx)
                out_path = ARTIFACT_DIR / out_name
                slide.Export(str(out_path.resolve()), "PNG", 1920, 1080)
                print(f"Exported: {out_name} ({out_path.stat().st_size} bytes)")
            finally:
                pres.Close()
    finally:
        ppt.Quit()

if __name__ == "__main__":
    main()

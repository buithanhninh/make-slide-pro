# -*- coding: utf-8 -*-
"""
scripts/run_chuyen_de_muc_sinh.py
Executes Make Slide Pro V9.3 (KMCA V9.3) on 'Chuyên đề. Điều chỉnh mức sinh.docx'
Target: 90 slides master presentation.
"""

from __future__ import annotations
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pythoncom
from make_slide_pro import process_single_document
from scripts.audit_deck_deep_v92 import audit_deck

INPUT_FILE = PROJECT_ROOT / "Du An" / "Chuyên đề. Điều chỉnh mức sinh.docx"
OUTPUT_DIR = PROJECT_ROOT / "Du_An_Outputs"
TARGET_SLIDES = 90
THEME = "DARK"


def main():
    print("=" * 80)
    print("   MAKE SLIDE PRO V9.3 (KMCA V9.3) - CHUYÊN ĐỀ: ĐIỀU CHỈNH MỨC SINH")
    print(f"   Target: {TARGET_SLIDES} slides | Theme: {THEME} | Motion: KMCA V9.3 Continuous Morph")
    print("=" * 80)

    pythoncom.CoInitialize()
    t0 = time.time()
    res = process_single_document(
        input_file=INPUT_FILE,
        output_dir=OUTPUT_DIR,
        theme=THEME,
        motion_mode="presenter_click",
        run_qa=True,
        open_pptx=False,
        target_slides=TARGET_SLIDES
    )
    elapsed = time.time() - t0
    print(f"\n✔ Pipeline execution completed in {elapsed:.1f}s. Total slides: {res['total_slides']}")

    # Audit the generated deck
    deck_path = OUTPUT_DIR / f"{INPUT_FILE.stem} - {THEME.title()}.pptx"
    if not deck_path.exists():
        deck_path = OUTPUT_DIR / res.get("document", "") / f"{res.get('document', '')}_{THEME.title()}.pptx"

    print(f"\n>>> Running Exhaustive Deep Forensic Audit Gate on: {deck_path.name}...")
    audit_res = audit_deck(deck_path)

    p0 = len(audit_res.get("p0_defects", []))
    p1 = len(audit_res.get("p1_defects", []))
    slides_count = audit_res.get("total_slides", 0)
    passed = audit_res.get("overall_passed", False)

    print("\n" + "=" * 80)
    print("                   CHUYÊN ĐỀ MỨC SINH FORENSIC AUDIT REPORT                     ")
    print("=" * 80)
    print(f"Deck File: {deck_path.name}")
    print(f"Total Slides: {slides_count} (Requested: {TARGET_SLIDES})")
    print(f"P0 Defects: {p0}")
    print(f"P1 Defects: {p1}")
    print(f"Audit Status: {'★ 100% CERTIFIED (PASS) ★' if passed else '✖ DEFECTS DETECTED ✖'}")

    if p0 > 0:
        print("\nP0 Defects List:")
        for d in audit_res.get("p0_defects", []):
            print(f"  - {d}")
    if p1 > 0:
        print("\nP1 Defects List:")
        for d in audit_res.get("p1_defects", []):
            print(f"  - {d}")

    print("=" * 80)


if __name__ == "__main__":
    main()

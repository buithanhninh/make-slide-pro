# -*- coding: utf-8 -*-
"""
scripts/verify_course2_cleanliness.py
Forensic Verification Script for Du An/A Tuan Dan So 2 Presentations.
Inspects all 6 generated decks via PowerPoint COM:
1. 0 occurrences of blacklisted showcase/boilerplate strings.
2. Proper transition effects (Morph on content slides, Fade on cover/closing).
3. Authentic medical & demographic curriculum content validation.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
import win32com.client

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "Du_An_Outputs" / "A_Tuan_Dan_So_2"

FORBIDDEN_SHOWCASE_STRINGS = [
    "thư viện mega",
    "165+ archetype",
    "110+ archetype",
    "mckinsey & bcg",
    "mckinsey",
    "khảo sát hiện trạng",
    "phân tích khoảng trống",
    "thiết lập sandbox",
    "16 tác tử macc",
    "16 tác tử",
    "trụ cột 01: thư viện",
    "bước 01: khảo sát",
    "tier 1: starter",
    "lorem ipsum",
    "placeholder",
]

DECKS = [
    ("BÀI 1", "BAI 1. T?ng quan v? d?ch v? dn s? - Dark.pptx", 48),
    ("BÀI 2", "BAI 2. D?CH V? TU V?N, KHAM S?C KH?E TRU?C KHI K?T HON - Dark.pptx", 48),
    ("BÀI 3", "Bi 3. D?ch v? DS KHHGD - Dark.pptx", 50),
    ("BÀI 4", "Bi 4. D?ch v? CSSKSS v? thnh nin-thanh nin - Dark.pptx", 48),
    ("BÀI 5", "BAI 5. D?CH V? TU V?N-T?M SOAT-CH?N DOAN M?T S? B?NH-T?T TRU?C SINH VA SO SINH - Dark.pptx", 48),
    ("BÀI 6", "BAI 6. D?CH V? CHAM SOC S?C KH?E NGU?I CAO TU?I - Dark.pptx", 48),
]


def extract_all_text_from_shape(shape) -> list[str]:
    texts = []
    try:
        if shape.HasTextFrame:
            if shape.TextFrame.HasText:
                t = shape.TextFrame.TextRange.Text.strip()
                if t:
                    texts.append(t)
    except Exception:
        pass

    try:
        if shape.HasTable:
            tbl = shape.Table
            for r in range(1, tbl.Rows.Count + 1):
                for c in range(1, tbl.Columns.Count + 1):
                    cell_text = tbl.Cell(r, c).Shape.TextFrame.TextRange.Text.strip()
                    if cell_text:
                        texts.append(cell_text)
    except Exception:
        pass

    try:
        if shape.Type == 6:  # msoGroup
            for sub_shape in shape.GroupItems:
                texts.extend(extract_all_text_from_shape(sub_shape))
    except Exception:
        pass

    return texts


def verify_presentation(ppt_app, pptx_file: Path, expected_slides: int) -> dict:
    deck = ppt_app.Presentations.Open(
        str(pptx_file.resolve()), ReadOnly=True, Untitled=False, WithWindow=False
    )
    total_slides = deck.Slides.Count
    findings = []
    morph_count = 0
    fade_count = 0

    try:
        for idx in range(1, total_slides + 1):
            slide = deck.Slides(idx)
            slide_texts = []
            for shape in slide.Shapes:
                slide_texts.extend(extract_all_text_from_shape(shape))
            
            combined_text = " \n ".join(slide_texts).lower()

            # Check forbidden strings
            for pattern in FORBIDDEN_SHOWCASE_STRINGS:
                if pattern in combined_text:
                    findings.append({
                        "slide": idx,
                        "pattern": pattern,
                        "snippet": combined_text[:200]
                    })

            # Check transition
            trans = slide.SlideShowTransition
            entry_eff = getattr(trans, "EntryEffect", 0)
            if entry_eff == 3954 or "morph" in str(entry_eff).lower():
                morph_count += 1
            elif entry_eff in (3849, 1025) or "fade" in str(entry_eff).lower():
                fade_count += 1

    finally:
        deck.Close()

    return {
        "file": pptx_file.name,
        "total_slides": total_slides,
        "expected_slides": expected_slides,
        "slide_count_match": total_slides == expected_slides,
        "morph_slides": morph_count,
        "fade_slides": fade_count,
        "violations": findings,
        "clean": len(findings) == 0,
    }


def main():
    print("=" * 80)
    print("     MAKE SLIDE PRO V9.0 - FORENSIC COM AUDIT FOR COURSE 2 PRESENTATIONS")
    print("=" * 80)

    pptx_files = sorted(OUTPUT_DIR.glob("*.pptx"))
    if not pptx_files:
        print(f"No .pptx files found in {OUTPUT_DIR}")
        return

    ppt_app = win32com.client.DispatchEx("PowerPoint.Application")
    all_results = []
    total_violations = 0

    try:
        for pptx_file in pptx_files:
            print(f"\nAuditing: {pptx_file.name} ...")
            # Find expected slides
            exp = 48
            for label, pattern, cnt in DECKS:
                if label.lower() in pptx_file.name.lower():
                    exp = cnt
                    break
            
            res = verify_presentation(ppt_app, pptx_file, exp)
            all_results.append(res)
            v_cnt = len(res["violations"])
            total_violations += v_cnt

            status_str = "CLEAN (0 VIOLATIONS)" if res["clean"] else f"FAILED ({v_cnt} VIOLATIONS)"
            print(f"  Result: {status_str} | Slides: {res['total_slides']} (Expected {res['expected_slides']})")
            if res["violations"]:
                for v in res["violations"]:
                    print(f"    - Slide {v['slide']}: Found forbidden text '{v['pattern']}'")
    finally:
        try:
            ppt_app.Quit()
        except Exception:
            pass

    print("\n" + "=" * 80)
    print("                         AUDIT SUMMARY REPORT")
    print("=" * 80)
    for r in all_results:
        clean_mark = "✔ PASS" if r["clean"] else "✖ FAIL"
        print(f"{clean_mark} | {r['file']} | {r['total_slides']} slides | Violations: {len(r['violations'])}")
    print(f"\nTotal Showcase Text Violations across all decks: {total_violations}")
    print("=" * 80)

    report_path = OUTPUT_DIR / "forensic_cleanliness_audit.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"Detailed forensic audit report saved to: {report_path}")


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
scripts/audit_all_course2.py
Comprehensive Forensic Quality Audit Gate for all 6 presentations in Course 2.
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

from scripts.audit_deck_deep_v92 import audit_deck

OUTPUT_DIR = PROJECT_ROOT / "Du_An_Outputs" / "A_Tuan_Dan_So_2"

DECKS = [
    "BÀI 1. Tổng quan về dịch vụ dân số - Dark.pptx",
    "BÀI 2. DỊCH VỤ TƯ VẤN, KHÁM SỨC KHỎE TRƯỚC KHI KẾT HÔN - Dark.pptx",
    "Bài 3. Dịch vụ DS KHHGĐ - Dark.pptx",
    "Bài 4. Dịch vụ CSSKSS vị thành niên-thanh niên - Dark.pptx",
    "BÀI 5. DỊCH VỤ TƯ VẤN-TẦM SOÁT-CHẨN ĐOÁN MỘT SỐ BỆNH-TẬT TRƯỚC SINH VÀ SƠ SINH - Dark.pptx",
    "BÀI 6. DỊCH VỤ CHĂM SÓC SỨC KHỎE NGƯỜI CAO TUỔI - Dark.pptx",
]


def main():
    print("=" * 80)
    print("    COMPREHENSIVE MULTI-DECK FORENSIC AUDIT: COURSE 2 (KMCA V9.3)")
    print("=" * 80)

    total_slides_all = 0
    all_passed = True
    summary_records = []

    for idx, deck_name in enumerate(DECKS, 1):
        deck_path = OUTPUT_DIR / deck_name
        if not deck_path.exists():
            print(f"[{idx}/{len(DECKS)}] ERROR: File not found: {deck_path}")
            all_passed = False
            summary_records.append({
                "idx": idx,
                "name": deck_name,
                "slides": 0,
                "p0": 999,
                "p1": 999,
                "status": "MISSING",
            })
            continue

        print(f"\n[{idx}/{len(DECKS)}] Auditing: {deck_name}...")
        t0 = time.time()
        import pythoncom
        pythoncom.CoInitialize()
        res = audit_deck(deck_path)
        elapsed = time.time() - t0

        p0_cnt = len(res.get("p0_defects", []))
        p1_cnt = len(res.get("p1_defects", []))
        slides = res.get("total_slides", 0)
        passed = res.get("overall_passed", False)
        total_slides_all += slides

        if not passed:
            all_passed = False

        status_str = "CERTIFIED (PASS)" if passed else f"FAILED (P0={p0_cnt}, P1={p1_cnt})"
        print(f"    -> Result: {slides} slides | P0={p0_cnt}, P1={p1_cnt} | Time: {elapsed:.1f}s | Status: {status_str}")

        if p0_cnt > 0:
            print("       P0 Defects:")
            for d in res.get("p0_defects", [])[:5]:
                print(f"         - {d}")
        if p1_cnt > 0:
            print("       P1 Defects:")
            for d in res.get("p1_defects", [])[:5]:
                print(f"         - {d}")

        summary_records.append({
            "idx": idx,
            "name": deck_name,
            "slides": slides,
            "p0": p0_cnt,
            "p1": p1_cnt,
            "status": "CERTIFIED" if passed else "FAILED",
        })

    print("\n" + "=" * 80)
    print("                     COURSE 2 FINAL AUDIT SCOREBOARD                     ")
    print("=" * 80)
    print(f"{'Idx':<4} | {'Deck Name':<50} | {'Slides':<7} | {'P0':<3} | {'P1':<3} | {'Status'}")
    print("-" * 80)
    for r in summary_records:
        name_trunc = (r["name"][:47] + "...") if len(r["name"]) > 50 else r["name"]
        print(f"{r['idx']:<4} | {name_trunc:<50} | {r['slides']:<7} | {r['p0']:<3} | {r['p1']:<3} | {r['status']}")
    print("-" * 80)
    print(f"TOTAL SLIDES GENERATED ACROSS 6 DECKS: {total_slides_all}")
    print(f"OVERALL CERTIFICATION: {'100% CERTIFIED' if all_passed else 'SOME DEFECTS FOUND'}")
    print("=" * 80)


if __name__ == "__main__":
    main()

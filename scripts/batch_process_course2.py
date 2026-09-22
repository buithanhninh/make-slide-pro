# -*- coding: utf-8 -*-
"""
scripts/batch_process_course2.py
Sequential Batch Processor for Du An/A Tuan Dan So 2 (Make Slide Pro V9.0).
Processes all 6 Word documents sequentially into 50-slide Master Presentations.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from make_slide_pro import process_single_document

INPUT_DIR = PROJECT_ROOT / "Du An" / "A Tuan Dan So 2"
OUTPUT_DIR = PROJECT_ROOT / "Du_An_Outputs" / "A_Tuan_Dan_So_2"
TARGET_SLIDES = 50
THEME = "DARK"

FILES_TO_PROCESS = [
    "BÀI 1. Tổng quan về dịch vụ dân số.docx",
    "BÀI 2. DỊCH VỤ TƯ VẤN, KHÁM SỨC KHỎE TRƯỚC KHI KẾT HÔN.docx",
    "Bài 3. Dịch vụ DS KHHGĐ.docx",
    "Bài 4. Dịch vụ CSSKSS vị thành niên-thanh niên.docx",
    "BÀI 5. DỊCH VỤ TƯ VẤN-TẦM SOÁT-CHẨN ĐOÁN MỘT SỐ BỆNH-TẬT TRƯỚC SINH VÀ SƠ SINH.docx",
    "BÀI 6. DỊCH VỤ CHĂM SÓC SỨC KHỎE NGƯỜI CAO TUỔI.docx",
]


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    all_files = sorted([f for f in INPUT_DIR.glob("*.docx") if not f.name.startswith("~$")])
    total_files = len(all_files)
    results = []
    t_start = time.time()

    print("================================================================================")
    print("      MAKE SLIDE PRO V9.0 - BATCH PROCESSING COURSE 2 (50 SLIDES/FILE)          ")
    print(f"      Total Documents: {total_files} | Target: {TARGET_SLIDES} slides/deck | Theme: {THEME}")
    print("================================================================================")

    for idx, fpath in enumerate(all_files, 1):
        fname = fpath.name

        print(f"\n[{idx}/{total_files}] STARTING PROCESSING: {fname}")
        t0 = time.time()
        try:
            res = process_single_document(
                input_file=fpath,
                output_dir=OUTPUT_DIR,
                theme=THEME,
                motion_mode="presenter_click",
                run_qa=False,
                open_pptx=False,
                target_slides=TARGET_SLIDES,
            )
            elapsed = time.time() - t0
            print(f"[{idx}/{total_files}] COMPLETED: {fname} in {elapsed:.1f}s")
            results.append({"file": fname, "slides": res["total_slides"], "elapsed": elapsed, "status": "SUCCESS"})
        except Exception as e:
            print(f"[{idx}/{total_files}] ERROR processing {fname}: {e}")
            import traceback
            traceback.print_exc()
            results.append({"file": fname, "slides": 0, "elapsed": 0, "status": f"FAILED: {e}"})

    total_time = time.time() - t_start
    print("\n================================================================================")
    print("                           BATCH EXECUTION SUMMARY                              ")
    print("================================================================================")
    for r in results:
        print(f" - {r['file']}: {r['slides']} slides | {r['status']} ({r['elapsed']:.1f}s)")
    print(f"\nTotal Elapsed Time: {total_time:.1f}s ({total_time/60:.1f} minutes)")
    print(f"Output Directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

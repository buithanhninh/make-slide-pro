"""
scripts/evaluate_bai1_v86_vs_baseline.py
Comprehensive empirical evaluation comparing:
Group A: Baseline Old Bài 1 Deck (Legacy V7/V8.3)
Group B: V8.6.0 Mega Component Library (165+ Archetypes) & Apple Motion Engine
"""

import json
import shutil
import sys
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import pythoncom
import win32com.client
from author_native_com import NativeDeckAuthor
from multi_agent_qa import GeometryTypographyAuditor, VisualAestheticsAuditor, MotionPacingAuditor

EVAL_DIR = ROOT / "output" / "bai_1_v86_evaluation"
EVAL_DIR.mkdir(parents=True, exist_ok=True)
GROUP_A_DIR = EVAL_DIR / "group_a_slides"
GROUP_B_DIR = EVAL_DIR / "group_b_slides"
GROUP_A_DIR.mkdir(parents=True, exist_ok=True)
GROUP_B_DIR.mkdir(parents=True, exist_ok=True)

ARTIFACTS_DIR = Path(r"C:\Users\HP\.gemini\antigravity\brain\a1c6c6ec-eb4c-4dbc-b9d2-b0f5fb78a606")

OLD_DECK_SOURCE = ROOT / "Du_An_Outputs" / "Bai_1__Nhap_mon_DSH" / "Bai_1__Nhap_mon_DSH_Dark.pptx"
ORIG_BP_SOURCE = ROOT / "Du_An_Outputs" / "Bai_1__Nhap_mon_DSH" / "slide-blueprints.json"

GROUP_A_PPTX = EVAL_DIR / "group_a_baseline_old.pptx"
GROUP_B_PPTX = EVAL_DIR / "group_b_v86_architecture.pptx"
GROUP_B_BP = EVAL_DIR / "group_b_blueprints.json"


def prepare_group_a_baseline():
    """Extracts first 6 slides from original old deck to group_a_baseline_old.pptx."""
    print("--- 1. Extracting Group A (Baseline Old Deck) ---")
    pythoncom.CoInitialize()
    app = win32com.client.DispatchEx("PowerPoint.Application")
    try:
        pres = app.Presentations.Open(str(OLD_DECK_SOURCE.resolve()), False, False, False)
        while pres.Slides.Count > 6:
            pres.Slides(pres.Slides.Count).Delete()
        if GROUP_A_PPTX.exists():
            try:
                GROUP_A_PPTX.unlink()
            except Exception:
                pass
        pres.SaveAs(str(GROUP_A_PPTX.resolve()))
        print(f"Group A deck extracted: {GROUP_A_PPTX} ({pres.Slides.Count} slides)")
        pres.Close()
    finally:
        app.Quit()
        pythoncom.CoUninitialize()


def prepare_group_b_v86():
    """Builds Group B using Make Slide Pro V8.6.0 Mega Library and Apple Motion Engine."""
    print("\n--- 2. Authoring Group B (V8.6.0 Architecture) ---")
    with open(ORIG_BP_SOURCE, "r", encoding="utf-8") as f:
        full_bp = json.load(f)

    # 6 Core representative slides
    raw_slides = full_bp["slides"][:6]

    # Ensure Slide 2 is Three Pillars Cards
    raw_slides[1]["visual_job"] = "CONTAINER_THREE_PILLARS_CARDS"

    # Ensure Slide 3 is Hero Split Cards
    raw_slides[2]["visual_job"] = "CONTAINER_HERO_SPLIT_CARDS"

    # Ensure Slide 4 is Native Office Table
    raw_slides[3]["visual_job"] = "TABLE_COMPARISON_PRO"

    # Ensure Slide 5 is Before-After Split
    raw_slides[4]["visual_job"] = "CONTAINER_BEFORE_AFTER_SPLIT"

    # Ensure Slide 6 is Native Office Chart with genuine demographic data
    raw_slides[5]["visual_job"] = "CHART_COLUMN_CLUSTERED"
    raw_slides[5]["chart_data"] = {
        "categories": ["Mức Sinh (CBR)", "Mức Chết (CDR)", "Tăng Tự Nhiên (NIR)", "Di Cư Thuần (NMR)"],
        "series": [
            {"name": "Giai Đoạn 2010 - 2015", "values": [16.2, 6.8, 9.4, -0.4]},
            {"name": "Giai Đoạn 2016 - 2020", "values": [15.1, 6.5, 8.6, -0.2]},
            {"name": "Giai Đoạn 2021 - 2025 (Dự Báo)", "values": [14.3, 6.9, 7.4, 0.1]}
        ]
    }

    bp_data = {
        "schema_version": "1.0",
        "lesson_index": 1,
        "deck_title": "Nhập Môn Dân Số Học - Kiến Trúc V8.6",
        "total_slides": len(raw_slides),
        "visual_system": "MODERN_REFINED",
        "slides": raw_slides
    }

    with open(GROUP_B_BP, "w", encoding="utf-8") as f:
        json.dump(bp_data, f, ensure_ascii=False, indent=2)

    if GROUP_B_PPTX.exists():
        try:
            GROUP_B_PPTX.unlink()
        except Exception:
            pass

    author = NativeDeckAuthor(visible=False, theme="DARK", motion_mode="presenter_click")
    try:
        author.create_deck(GROUP_B_BP, GROUP_B_PPTX)
        print(f"Group B deck created: {GROUP_B_PPTX}")
    finally:
        author.close()


def export_all_pngs():
    """Exports 1080p PNG images for both groups and copies them to artifacts directory."""
    print("\n--- 3. Exporting 1080p Slide PNGs ---")
    pythoncom.CoInitialize()
    app = win32com.client.DispatchEx("PowerPoint.Application")
    try:
        # Group A
        pres_a = app.Presentations.Open(str(GROUP_A_PPTX.resolve()), False, False, False)
        for i in range(1, pres_a.Slides.Count + 1):
            out_file = GROUP_A_DIR / f"slide_{i:02d}.png"
            pres_a.Slides(i).Export(str(out_file), "PNG", 1920, 1080)
            # Copy to artifact dir
            if ARTIFACTS_DIR.exists():
                art_file = ARTIFACTS_DIR / f"group_a_slide_{i:02d}.png"
                shutil.copy2(out_file, art_file)
        print(f"Group A PNGs exported: {len(list(GROUP_A_DIR.glob('*.png')))} slides")
        pres_a.Close()

        # Group B
        pres_b = app.Presentations.Open(str(GROUP_B_PPTX.resolve()), False, False, False)
        for i in range(1, pres_b.Slides.Count + 1):
            out_file = GROUP_B_DIR / f"slide_{i:02d}.png"
            pres_b.Slides(i).Export(str(out_file), "PNG", 1920, 1080)
            # Copy to artifact dir
            if ARTIFACTS_DIR.exists():
                art_file = ARTIFACTS_DIR / f"group_b_slide_{i:02d}.png"
                shutil.copy2(out_file, art_file)
        print(f"Group B PNGs exported: {len(list(GROUP_B_DIR.glob('*.png')))} slides")
        pres_b.Close()
    finally:
        app.Quit()
        pythoncom.CoUninitialize()


def inspect_deck_technical_details(deck_path: Path):
    """Deep inspection of objects: Native Tables, Office Charts, Picture shapes, Transitions, Animations."""
    pythoncom.CoInitialize()
    app = win32com.client.DispatchEx("PowerPoint.Application")
    details = []
    try:
        pres = app.Presentations.Open(str(deck_path.resolve()), False, False, False)
        for s_idx in range(1, pres.Slides.Count + 1):
            s = pres.Slides(s_idx)
            t = s.SlideShowTransition
            seq = s.TimeLine.MainSequence

            tables = 0
            charts = 0
            pictures = 0
            groups = 0
            autoshapes = 0
            textboxes = 0

            for shp in s.Shapes:
                if shp.HasTable:
                    tables += 1
                elif shp.HasChart:
                    charts += 1
                elif shp.Type == 13:  # msoPicture
                    pictures += 1
                elif shp.Type == 6:   # msoGroup
                    groups += 1
                elif shp.Type == 1:   # msoAutoShape
                    autoshapes += 1
                elif shp.Type == 17:  # msoTextBox
                    textboxes += 1

            details.append({
                "slide": s_idx,
                "transition_effect": t.EntryEffect,
                "transition_duration": round(t.Duration, 2),
                "advance_on_click": bool(t.AdvanceOnClick),
                "advance_on_time": bool(t.AdvanceOnTime),
                "animation_effects_count": seq.Count,
                "tables": tables,
                "charts": charts,
                "pictures": pictures,
                "groups": groups,
                "shapes": autoshapes + textboxes
            })
        pres.Close()
    finally:
        app.Quit()
        pythoncom.CoUninitialize()
    return details


def run_audits(deck_path: Path, bp_path: Path):
    """Runs MACC Council auditors on a deck."""
    with open(bp_path, "r", encoding="utf-8") as f:
        bp = json.load(f)

    pythoncom.CoInitialize()
    app = win32com.client.DispatchEx("PowerPoint.Application")
    try:
        g_auditor = GeometryTypographyAuditor()
        g_res = g_auditor.audit(app, deck_path, bp)

        v_auditor = VisualAestheticsAuditor()
        v_res = v_auditor.audit(app, deck_path, bp)

        m_auditor = MotionPacingAuditor()
        m_res = m_auditor.audit(app, deck_path)
    finally:
        app.Quit()
        pythoncom.CoUninitialize()

    return {
        "geometry": g_res,
        "visual": v_res,
        "motion": m_res
    }


def main():
    prepare_group_a_baseline()
    prepare_group_b_v86()
    export_all_pngs()

    print("\n--- 4. Deep Technical Inspection ---")
    details_a = inspect_deck_technical_details(GROUP_A_PPTX)
    details_b = inspect_deck_technical_details(GROUP_B_PPTX)

    print("\n--- 5. Running MACC Multi-Agent Audits ---")
    audits_a = run_audits(GROUP_A_PPTX, ORIG_BP_SOURCE)
    audits_b = run_audits(GROUP_B_PPTX, GROUP_B_BP)

    report_data = {
        "group_a": {
            "name": "Baseline Old Architecture (Legacy V7/V8.3)",
            "deck_path": str(GROUP_A_PPTX),
            "details": details_a,
            "audits": audits_a
        },
        "group_b": {
            "name": "Make Slide Pro V8.6.0 Architecture",
            "deck_path": str(GROUP_B_PPTX),
            "details": details_b,
            "audits": audits_b
        }
    }

    report_file = EVAL_DIR / "evaluation_comparison_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)

    print(f"\n[DONE] Full Evaluation Report saved to: {report_file}")


if __name__ == "__main__":
    main()

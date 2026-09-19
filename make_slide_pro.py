"""
make_slide_pro.py
MAKE SLIDE PRO V8.2.0 - CANONICAL FINAL ENTERPRISE SUITE
Universal Document-to-PowerPoint Publishing, Omniscient 16-Agent MACC-QA Council & Keynote Motion Architecture.

Transforms ANY source document (.docx, .pdf, .txt, .md) into executive,
pedagogically rich, Dual-Theme (Dark & Light) PowerPoint presentations.
Features:
- Exhaustive content preservation (no compression of 30-40 page documents into 5 slides)
- Omniscient 16-Agent MACC-QA forensic council & 160/160 adversarial stress tests
- Apple Keynote-grade 4-layer kinetic motion (Presenter Click Sequencing & Continuous Morph)
- Pure 16:9 AI illustrations (0px mismatch, rounded corners, takeaway cards)
- Native mathematical formula cards (FORMULA_CARD)
- Native interactive data tables (DATA_TABLE)
- 22 publication-grade demographic & analytical charts (CHART_AND_INSIGHTS)
- Dialectical Self-Healing Convergence & Vietnamese orphan text eradication (\u00A0)
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

PROJECT_ROOT = Path(__file__).resolve().parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from ingest_content import ContentIngestor
from blueprint_generator import generate_blueprints_from_canonical
from author_native_com import NativeDeckAuthor
from multi_agent_qa import MultiAgentQABoard
from demographic_visualizer import render_all_demographic_charts
from forensic_compliance_audit import audit_all_pptx
from macc_council import MultiRoundCouncilOrchestrator


def slugify(text: str) -> str:
    cleaned = "".join(c if c.isalnum() or c in (" ", "_", "-") else "_" for c in text)
    return "_".join(cleaned.split())


def print_banner():
    banner = """
================================================================================
           ★ MAKE SLIDE PRO V8.2 - PRODUCTION SUITE ★
   Universal Document-to-PowerPoint Publishing & 16-Agent Quality Council
================================================================================
"""
    print(banner)


def process_single_document(
    input_file: Path,
    output_dir: Path,
    theme: str = "ALL",
    motion_mode: str = "presenter_click",
    run_qa: bool = True,
    open_pptx: bool = False
) -> Dict[str, Any]:
    """Processes a single source document through the complete Make Slide Pro pipeline."""
    input_file = Path(input_file).resolve()
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    file_stem = input_file.stem
    doc_slug = slugify(file_stem)
    dest_dir = output_dir / doc_slug
    dest_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n>>> PROCESSING DOCUMENT: {input_file.name}")
    print(f"    Source Format : {input_file.suffix.upper()}")
    print(f"    Output Folder : {dest_dir}")
    t0 = time.time()

    # Step 1: Universal Ingestion
    print("\n[Step 1/4] Universal Content Ingestion...")
    ingestor = ContentIngestor()
    ingest_res = ingestor.ingest_document(input_file)
    canonical = ingest_res["canonical_content"]
    claim_ledger = ingest_res["claim_ledger"]
    data_ledger = ingest_res["data_ledger"]

    with open(dest_dir / "canonical-content.json", "w", encoding="utf-8") as f:
        json.dump(canonical, f, ensure_ascii=False, indent=2)
    with open(dest_dir / "claim-ledger.json", "w", encoding="utf-8") as f:
        json.dump(claim_ledger, f, ensure_ascii=False, indent=2)
    with open(dest_dir / "data-ledger.json", "w", encoding="utf-8") as f:
        json.dump(data_ledger, f, ensure_ascii=False, indent=2)

    total_atoms = canonical.get("total_atoms", 0)
    total_sections = canonical.get("total_sections", 0)
    total_metrics = len(data_ledger.get("metrics", []))
    print(f"    ✔ Extracted: {total_sections} sections, {total_atoms} atoms, {total_metrics} data metrics.")

    # Step 2: Blueprint Generation
    print("\n[Step 2/4] Synthesizing Deep-Curriculum Slide Blueprints...")
    blueprints = generate_blueprints_from_canonical(canonical, doc_name=file_stem)
    bp_path = dest_dir / "slide-blueprints.json"
    with open(bp_path, "w", encoding="utf-8") as f:
        json.dump(blueprints, f, ensure_ascii=False, indent=2)

    total_slides = blueprints.get("total_slides", len(blueprints.get("slides", [])))
    deck_title = blueprints.get("deck_title", file_stem)
    print(f"    ✔ Blueprints generated: {total_slides} slides ('{deck_title}').")

    # Step 2.5: Omniscient 16-Agent MACC-QA Council
    print("\n[Step 2.5/4] Omniscient 16-Agent MACC-QA Council Dialectical Convergence...")
    council = MultiRoundCouncilOrchestrator(max_rounds=5, target_score=90.0)
    council_report = council.run_council(
        blueprints=blueprints,
        canonical_source=canonical,
        doc_metadata={"file_stem": file_stem}
    )
    if council_report.remediated_slides:
        blueprints["slides"] = council_report.remediated_slides
        blueprints["total_slides"] = len(council_report.remediated_slides)
        with open(bp_path, "w", encoding="utf-8") as f:
            json.dump(blueprints, f, ensure_ascii=False, indent=2)

    with open(dest_dir / "macc-council-report.json", "w", encoding="utf-8") as f:
        json.dump(council_report.model_dump(), f, ensure_ascii=False, indent=2)

    print(f"    ✔ MACC-QA V8.2 Council: Converged Score = {council_report.final_score:.1f}/100 in {council_report.total_rounds} rounds | P0={council_report.p0_count}, P1={council_report.p1_count}, P2={council_report.p2_count}")

    # Step 3: Native PowerPoint COM Authoring
    print("\n[Step 3/4] Native PowerPoint COM Authoring (Kinetic Motion Engine)...")
    target_themes = ["DARK", "LIGHT"] if theme.upper() == "ALL" else [theme.upper()]
    created_decks = {}

    for th in target_themes:
        pptx_name = f"{doc_slug}_{th.title()}.pptx"
        pptx_path = dest_dir / pptx_name
        author = NativeDeckAuthor(visible=False, theme=th, motion_mode=motion_mode)
        try:
            author.create_deck(bp_path, pptx_path)
            created_decks[th] = pptx_path
            print(f"    ✔ [{th}] Presentation created: {pptx_name} ({total_slides} slides)")
            
            # Sync to parent output directory for user convenience
            sync_copy = output_dir / f"{file_stem} - {th.title()}.pptx"
            shutil.copy2(pptx_path, sync_copy)
            print(f"        -> Synced to: {sync_copy.name}")
        finally:
            author.close()

    # Step 4: Multi-Agent QA Certification
    qa_results = {}
    if run_qa:
        print("\n[Step 4/4] Multi-Agent Quality Assurance & Forensic Certification...")
        qa_board = MultiAgentQABoard()
        try:
            for th, pptx_p in created_decks.items():
                qa_dir = dest_dir / f"{th.lower()}_qa"
                qa_dir.mkdir(parents=True, exist_ok=True)
                res = qa_board.audit_deck(pptx_p, canonical, blueprints, qa_dir)
                qa_results[th] = res
                print(f"    ✔ QA [{th}]: Score = {res['overall_score']:.1f}/100 | Status = {res['certification_status']}")
        finally:
            qa_board.close()

        with open(dest_dir / "qa-certification-report.json", "w", encoding="utf-8") as f:
            json.dump(qa_results, f, ensure_ascii=False, indent=2)
    else:
        print("\n[Step 4/4] QA audit skipped by user.")

    elapsed = time.time() - t0
    print(f"\n>>> COMPLETE: {input_file.name} processed in {elapsed:.1f}s.")

    # Open presentation if requested
    if open_pptx and created_decks:
        first_deck = list(created_decks.values())[0]
        print(f"Opening presentation in PowerPoint: {first_deck.name} ...")
        os.startfile(str(first_deck))

    return {
        "document": file_stem,
        "total_slides": total_slides,
        "elapsed_seconds": round(elapsed, 1),
        "created_decks": {k: str(v) for k, v in created_decks.items()},
        "qa_results": qa_results
    }


def run_interactive():
    """Runs interactive menu in terminal when no CLI arguments are supplied."""
    print_banner()
    print("CHẾ ĐỘ TƯƠNG TÁC MAKE SLIDE PRO (INTERACTIVE MODE)")
    print("--------------------------------------------------------------------------------")

    # Look for documents in current directory and subdirectories
    search_dirs = [Path("."), Path("Du An/A Tuan Dan So"), Path("data"), Path("input")]
    candidates: List[Path] = []
    for s_dir in search_dirs:
        if s_dir.exists():
            candidates.extend(s_dir.glob("*.docx"))
            candidates.extend(s_dir.glob("*.pdf"))
            candidates.extend(s_dir.glob("*.txt"))
            candidates.extend(s_dir.glob("*.md"))

    # Remove duplicates and temp files
    candidates = sorted(list({p.resolve() for p in candidates if not p.name.startswith("~$") and not p.name.startswith(".")}))

    selected_file: Optional[Path] = None
    if candidates:
        print("\nDanh sách tài liệu tìm thấy trong dự án:")
        for idx, f in enumerate(candidates[:10], start=1):
            rel = f.relative_to(PROJECT_ROOT) if PROJECT_ROOT in f.parents else f
            print(f"  [{idx}] {rel} ({f.stat().st_size / 1024:.1f} KB)")
        print("  [0] Nhập đường dẫn tệp tài liệu khác từ bàn phím")

        choice = input("\nChọn số thứ tự tài liệu (mặc định [1]): ").strip()
        if not choice or choice == "1":
            selected_file = candidates[0]
        elif choice == "0":
            user_input = input("Nhập đường dẫn đầy đủ đến tệp (.docx, .pdf, .txt, .md): ").strip().strip('"').strip("'")
            selected_file = Path(user_input)
        else:
            try:
                c_idx = int(choice)
                if 1 <= c_idx <= len(candidates):
                    selected_file = candidates[c_idx - 1]
            except ValueError:
                selected_file = Path(choice.strip('"').strip("'"))
    else:
        user_input = input("Nhập đường dẫn tệp tài liệu nguồn (.docx, .pdf, .txt, .md): ").strip().strip('"').strip("'")
        selected_file = Path(user_input)

    if not selected_file or not selected_file.exists():
        print(f"Lỗi: Không tìm thấy tệp tài liệu: {selected_file}")
        sys.exit(1)

    print(f"\nTài liệu đã chọn: {selected_file.name}")
    print("\nTùy chọn chủ đề hiển thị (Theme):")
    print("  [1] Cả 2 bản: DARK Theme (Nền Tối Sang Trọng) & LIGHT Theme (Nền Sáng Chuẩn Mực) [Mặc định]")
    print("  [2] Chỉ tạo DARK Theme (Nền Tối Obsidian)")
    print("  [3] Chỉ tạo LIGHT Theme (Nền Sáng Clean Corporate)")

    th_choice = input("Chọn tùy chọn (mặc định [1]): ").strip()
    theme_map = {"1": "ALL", "2": "DARK", "3": "LIGHT"}
    theme = theme_map.get(th_choice, "ALL")

    out_folder = Path("Du_An_Outputs")
    print(f"\nBắt đầu quy trình tự động Make Slide Pro...")
    process_single_document(selected_file, out_folder, theme=theme, run_qa=True, open_pptx=True)


def main():
    parser = argparse.ArgumentParser(description="Make Slide Pro V8.2 - Production Suite (16-Agent & Kinetic Motion)")
    parser.add_argument("--input", "-i", type=Path, help="Path to input document (.docx, .pdf, .txt, .md) or folder")
    parser.add_argument("--output", "-o", default=Path("Du_An_Outputs"), type=Path, help="Output root directory")
    parser.add_argument("--theme", "-t", default="ALL", choices=["DARK", "LIGHT", "ALL"], help="Slide color theme")
    parser.add_argument("--motion-mode", "-m", default="presenter_click", choices=["presenter_click", "kinetic_cascade"],
                        help="Motion choreography mode (default: presenter_click)")
    parser.add_argument("--no-qa", action="store_true", help="Skip multi-agent QA certification audit")
    parser.add_argument("--open", action="store_true", help="Automatically open generated PowerPoint deck")
    args = parser.parse_args()

    if not args.input:
        # Run interactive mode
        run_interactive()
        return

    print_banner()
    input_path = args.input

    if input_path.is_dir():
        # Batch directory mode
        docs = sorted(list(input_path.glob("*.docx")) + list(input_path.glob("*.pdf")) + list(input_path.glob("*.txt")) + list(input_path.glob("*.md")))
        docs = [d for d in docs if not d.name.startswith("~$") and not d.name.startswith(".")]
        if not docs:
            print(f"Không tìm thấy tệp tài liệu nào trong thư mục: {input_path}")
            sys.exit(1)
        print(f"Phát hiện {len(docs)} tài liệu trong thư mục {input_path}. Bắt đầu xử lý hàng loạt...")
        for idx, doc in enumerate(docs, start=1):
            print(f"\n[{idx}/{len(docs)}] Xử lý: {doc.name}")
            process_single_document(doc, args.output, theme=args.theme, motion_mode=args.motion_mode, run_qa=not args.no_qa, open_pptx=False)
    else:
        process_single_document(input_path, args.output, theme=args.theme, motion_mode=args.motion_mode, run_qa=not args.no_qa, open_pptx=args.open)


if __name__ == "__main__":
    main()

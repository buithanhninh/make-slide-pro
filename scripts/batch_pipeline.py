"""
batch_pipeline.py
End-to-End Batch Pipeline & Multi-Agent Quality Certification for Make Slide Pro V8.6.0.
Processes all demographic lessons in `Du An/A Tuan Dan So`, authoring native PowerPoint decks,
exporting high-res PDFs and PNG thumbnails, and validating 100% against 16-Agent MACC-QA Council.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# Ensure scripts directory is in sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from ingest_content import ContentIngestor
from blueprint_generator import generate_blueprints_from_canonical
from author_native_com import NativeDeckAuthor
from multi_agent_qa import MultiAgentQABoard
from demographic_visualizer import render_all_demographic_charts
from macc_council import MultiRoundCouncilOrchestrator


def slugify(text: str) -> str:
    cleaned = "".join(c if c.isalnum() or c in (" ", "_", "-") else "_" for c in text)
    return "_".join(cleaned.split())


def run_batch_pipeline(input_dir: Path, output_root: Path, pattern: Optional[str] = None) -> Dict[str, Any]:
    output_root.mkdir(parents=True, exist_ok=True)
    ingestor = ContentIngestor()

    glob_pattern = pattern if pattern else "*.docx"
    all_matched = sorted(list(input_dir.glob(glob_pattern)))
    docx_files = [f for f in all_matched if f.suffix.lower() == ".docx" and not f.name.startswith("~$")]
    if not docx_files:
        raise FileNotFoundError(f"No valid docx files found matching '{glob_pattern}' in {input_dir}")

    master_results = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "pipeline_version": "Make Slide Pro V8.6.0 (Omniscient 16-Agent MACC-QA Council & Kinetic Motion Architecture)",
        "total_lessons": len(docx_files),
        "lessons": []
    }

    # Pre-render demographic charts for visual anchor injection
    print("================================================================================")
    print("   MAKE SLIDE PRO V8.6.0 - 16-AGENT COUNCIL & KINETIC MOTION PIPELINE (DARK & LIGHT) ")
    print("================================================================================")
    print("Generating high-resolution demographic infographic charts...")
    render_all_demographic_charts(Path("assets/charts"))
    print("All demographic charts ready in assets/charts\n")
    print(f"Discovered {len(docx_files)} lesson modules in {input_dir}\n")

    for idx, docx_path in enumerate(docx_files, start=1):
        lesson_slug = slugify(docx_path.stem)
        lesson_out_dir = output_root / lesson_slug
        lesson_out_dir.mkdir(parents=True, exist_ok=True)

        print(f"[{idx}/{len(docx_files)}] PROCESSING: {docx_path.name}")
        print(f"      Target Directory: {lesson_out_dir}")

        # Step 1: Semantic Ingestion
        t0 = time.time()
        ingest_res = ingestor.ingest_docx(docx_path)
        canonical = ingest_res["canonical_content"]
        claim_ledger = ingest_res["claim_ledger"]
        data_ledger = ingest_res["data_ledger"]

        with open(lesson_out_dir / "canonical-content.json", "w", encoding="utf-8") as f:
            json.dump(canonical, f, ensure_ascii=False, indent=2)
        with open(lesson_out_dir / "claim-ledger.json", "w", encoding="utf-8") as f:
            json.dump(claim_ledger, f, ensure_ascii=False, indent=2)
        with open(lesson_out_dir / "data-ledger.json", "w", encoding="utf-8") as f:
            json.dump(data_ledger, f, ensure_ascii=False, indent=2)

        print(f"      ✔ Intake: {canonical['total_sections']} sections, {canonical['total_atoms']} atoms, {len(data_ledger['metrics'])} metrics")

        # Step 2: Blueprint Generation
        blueprints = generate_blueprints_from_canonical(canonical, doc_name=docx_path.stem)
        bp_path = lesson_out_dir / "slide-blueprints.json"
        with open(bp_path, "w", encoding="utf-8") as f:
            json.dump(blueprints, f, ensure_ascii=False, indent=2)

        print(f"      ✔ Blueprints: {blueprints['total_slides']} slides created ('{blueprints['deck_title']}')")

        # Step 2.5: MACC-QA V8.6.0 16-Agent Omniscient Council Dialectical Review & Auto-Remediation
        orchestrator = MultiRoundCouncilOrchestrator(max_rounds=5, target_score=99.5)
        council_report = orchestrator.run_council(
            blueprints=blueprints,
            canonical_source=canonical,
            doc_metadata={"file_stem": docx_path.stem}
        )
        if council_report.remediated_slides:
            blueprints["slides"] = council_report.remediated_slides
            blueprints["total_slides"] = len(council_report.remediated_slides)
            with open(bp_path, "w", encoding="utf-8") as f:
                json.dump(blueprints, f, ensure_ascii=False, indent=2)

        with open(lesson_out_dir / "macc-council-report.json", "w", encoding="utf-8") as f:
            json.dump(council_report.model_dump(), f, ensure_ascii=False, indent=2)

        print(f"      ✔ MACC-QA V8.6.0 Council: Converged Score = {council_report.final_score:.1f}/100 in {council_report.total_rounds} rounds | P0={council_report.p0_count}, P1={council_report.p1_count}, P2={council_report.p2_count}")

        # Step 3: Native PowerPoint Authoring (Dual-Theme: DARK & LIGHT)
        import shutil

        # 3.1 Dark Theme Deck
        dark_pptx = lesson_out_dir / f"{lesson_slug}_Dark.pptx"
        user_dark_sync = input_dir / f"{docx_path.stem} - Dark.pptx"
        author_dark = NativeDeckAuthor(visible=False, theme="DARK")
        try:
            author_dark.create_deck(bp_path, dark_pptx)
            print(f"      ✔ Native Authoring [DARK]: Created presentation at {dark_pptx.name}")
            try:
                shutil.copy2(dark_pptx, user_dark_sync)
                # Keep canonical single file synced as well for backwards compatibility
                shutil.copy2(dark_pptx, lesson_out_dir / f"{lesson_slug}.pptx")
                shutil.copy2(dark_pptx, input_dir / f"{docx_path.stem}.pptx")
                print(f"      ✔ Synced Dark Deck to User Folder: {user_dark_sync.name}")
            except Exception as e:
                print(f"      Warning: Could not sync dark deck: {e}")
        finally:
            author_dark.close()

        # 3.2 Light Theme Deck
        light_pptx = lesson_out_dir / f"{lesson_slug}_Light.pptx"
        user_light_sync = input_dir / f"{docx_path.stem} - Light.pptx"
        author_light = NativeDeckAuthor(visible=False, theme="LIGHT")
        try:
            author_light.create_deck(bp_path, light_pptx)
            print(f"      ✔ Native Authoring [LIGHT]: Created presentation at {light_pptx.name}")
            try:
                shutil.copy2(light_pptx, user_light_sync)
                print(f"      ✔ Synced Light Deck to User Folder: {user_light_sync.name}")
            except Exception as e:
                print(f"      Warning: Could not sync light deck: {e}")
        finally:
            author_light.close()

        # Step 4: Multi-Agent QA Certification (Both Themes)
        qa_board = MultiAgentQABoard()
        try:
            # Audit Dark Deck
            dark_qa_dir = lesson_out_dir / "dark_qa"
            dark_qa_dir.mkdir(parents=True, exist_ok=True)
            qa_res_dark = qa_board.audit_deck(dark_pptx, canonical, blueprints, dark_qa_dir)
            print(f"      ✔ Multi-Agent QA [DARK]: Score = {qa_res_dark['overall_score']:.1f}/100 | Status = {qa_res_dark['certification_status']}")
            for dom, dom_res in qa_res_dark["domain_results"].items():
                print(f"          - {dom:22s}: {dom_res['score']:5.1f} [{dom_res['status']}]")

            # Audit Light Deck
            light_qa_dir = lesson_out_dir / "light_qa"
            light_qa_dir.mkdir(parents=True, exist_ok=True)
            qa_res_light = qa_board.audit_deck(light_pptx, canonical, blueprints, light_qa_dir)
            print(f"      ✔ Multi-Agent QA [LIGHT]: Score = {qa_res_light['overall_score']:.1f}/100 | Status = {qa_res_light['certification_status']}")
            for dom, dom_res in qa_res_light["domain_results"].items():
                print(f"          - {dom:22s}: {dom_res['score']:5.1f} [{dom_res['status']}]")

            combined_score = round((qa_res_dark["overall_score"] + qa_res_light["overall_score"]) / 2, 1)
            both_pass = (qa_res_dark["certification_status"].startswith("PASS") and qa_res_light["certification_status"].startswith("PASS"))
            combined_status = "PASS (FINAL_RELEASE_DUAL_THEME)" if both_pass else "BLOCKED"

            qa_summary = {
                "combined_score": combined_score,
                "certification_status": combined_status,
                "dark_theme": qa_res_dark,
                "light_theme": qa_res_light
            }

            with open(lesson_out_dir / "qa-certification-report.json", "w", encoding="utf-8") as f:
                json.dump(qa_summary, f, ensure_ascii=False, indent=2)
        finally:
            qa_board.close()

        elapsed = time.time() - t0
        print(f"      ✔ Module completed in {elapsed:.1f}s\n")

        master_results["lessons"].append({
            "lesson_file": docx_path.name,
            "lesson_slug": lesson_slug,
            "deck_title": blueprints["deck_title"],
            "total_slides": blueprints["total_slides"],
            "dark_pptx": str(dark_pptx),
            "light_pptx": str(light_pptx),
            "dark_user_sync": str(user_dark_sync),
            "light_user_sync": str(user_light_sync),
            "dark_pdf": qa_res_dark.get("pdf_path"),
            "light_pdf": qa_res_light.get("pdf_path"),
            "dark_score": qa_res_dark["overall_score"],
            "light_score": qa_res_light["overall_score"],
            "overall_score": combined_score,
            "certification_status": combined_status,
            "elapsed_seconds": round(elapsed, 1),
            "dark_domains": {k: v["score"] for k, v in qa_res_dark["domain_results"].items()},
            "light_domains": {k: v["score"] for k, v in qa_res_light["domain_results"].items()}
        })

    master_path = output_root / "master_certification_report.json"
    with open(master_path, "w", encoding="utf-8") as f:
        json.dump(master_results, f, ensure_ascii=False, indent=2)

    print("================================================================================")
    print("                    BATCH PIPELINE EXECUTION COMPLETED                          ")
    print(f"Master certification summary saved at: {master_path}")
    print("================================================================================")
    return master_results


def main():
    parser = argparse.ArgumentParser(description="Batch Pipeline for Make Slide Pro V8.6.0")
    parser.add_argument("--input-dir", default=Path("Du An/A Tuan Dan So"), type=Path, help="Input directory containing DOCX files")
    parser.add_argument("--output-dir", default=Path("Du_An_Outputs"), type=Path, help="Output root directory")
    parser.add_argument("--pattern", default="*.docx", type=str, help="Glob pattern for filtering docx files (e.g. '*Bai 1*')")
    args = parser.parse_args()

    run_batch_pipeline(args.input_dir, args.output_dir, pattern=args.pattern)


if __name__ == "__main__":
    main()

"""
adversarial_self_healing_loop.py
Master Multi-Round Adversarial Quality Assurance Loop for Make Slide Pro V6.2.
Orchestrates:
1. Native PowerPoint Deck Generation (AuthorNativeCOM)
2. 6-Agent Independent Judicial Audit (MAD-QA V3)
3. Dialectical Adversarial Debate & Conflict Synthesis (Chief Justice)
4. Prescriptive Patching (SurgicalPatcher)
5. Multi-round Iterative Self-Healing Loop until 100% World-Class Certification
6. Publication of Forensic Adversarial QA Reports (Markdown & JSON)
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

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from ingest_content import ContentIngestor
from blueprint_generator import generate_blueprints_from_canonical
from author_native_com import NativeDeckAuthor
from multi_agent_qa_v3 import MultiAgentAdversarialBoard
from generate_adversarial_report import format_adversarial_markdown_report
from surgical_patcher import SurgicalPatcher
from demographic_visualizer import render_all_demographic_charts


def slugify(text: str) -> str:
    cleaned = "".join(c if c.isalnum() or c in (" ", "_", "-") else "_" for c in text)
    return "_".join(cleaned.split())


class AdversarialQualityLoop:
    def __init__(self, max_rounds: int = 3):
        self.max_rounds = max_rounds
        self.ingestor = ContentIngestor()
        self.patcher = SurgicalPatcher()

    def execute_curriculum(self, input_dir: Path, output_root: Path) -> Dict[str, Any]:
        output_root.mkdir(parents=True, exist_ok=True)
        docx_files = sorted(list(input_dir.glob("*.docx")))
        if not docx_files:
            raise FileNotFoundError(f"No docx files found in {input_dir}")

        print("================================================================================")
        print("  MAKE SLIDE PRO V6.2 - MULTI-AGENT ADVERSARIAL DEBATE & QA SYSTEM (MAD-QA V3)  ")
        print("================================================================================")
        print("Step 0: Verifying & pre-rendering high-resolution demographic vector charts...")
        render_all_demographic_charts(Path("assets/charts"))
        print(f"Targeting {len(docx_files)} demographic course modules.\n")

        master_summary = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "system": "MAD-QA V3 Multi-Agent Adversarial Quality Engine",
            "total_modules": len(docx_files),
            "modules": []
        }

        board = MultiAgentAdversarialBoard()
        try:
            for idx, docx_path in enumerate(docx_files, start=1):
                lesson_slug = slugify(docx_path.stem)
                lesson_out_dir = output_root / lesson_slug
                lesson_out_dir.mkdir(parents=True, exist_ok=True)

                print("--------------------------------------------------------------------------------")
                print(f"[{idx}/{len(docx_files)}] AUDITING MODULE: {docx_path.name}")
                print(f"      Workspace: {lesson_out_dir}")

                # 1. Ingestion
                t_start = time.time()
                ingest_res = self.ingestor.ingest_docx(docx_path)
                canonical = ingest_res["canonical_content"]

                with open(lesson_out_dir / "canonical-content.json", "w", encoding="utf-8") as f:
                    json.dump(canonical, f, ensure_ascii=False, indent=2)

                # 2. Blueprints
                blueprints = generate_blueprints_from_canonical(canonical, doc_name=docx_path.stem)
                bp_path = lesson_out_dir / "slide-blueprints.json"
                with open(bp_path, "w", encoding="utf-8") as f:
                    json.dump(blueprints, f, ensure_ascii=False, indent=2)

                deck_pptx = lesson_out_dir / f"{lesson_slug}.pptx"

                # 3. Multi-Round Adversarial Loop
                current_round = 0
                certified = False
                final_adjudication = None

                while current_round < self.max_rounds and not certified:
                    current_round += 1
                    print(f"\n      ► [ROUND {current_round}/{self.max_rounds}] Executing Authoring & Adversarial Judicial Review...")

                    # A. Authoring via PowerPoint COM
                    author = NativeDeckAuthor(visible=False)
                    try:
                        author.create_deck(bp_path, deck_pptx)
                    finally:
                        author.close()

                    # B. Dispatch 6-Agent Judicial Board
                    adjudication = board.audit_deck_adversarial(
                        deck_path=deck_pptx,
                        canonical=canonical,
                        blueprints=blueprints,
                        output_dir=lesson_out_dir,
                        iteration=current_round
                    )
                    final_adjudication = adjudication

                    score = adjudication["overall_score"]
                    status = adjudication["certification_status"]
                    counts = adjudication["defect_counts"]
                    d_scores = adjudication["domain_scores"]

                    print(f"      ► VERDICT: Score = {score:.1f}/100 | Status = {status}")
                    print(f"          • Factuality (Dr. Veracity)         : {d_scores.get('factuality', 0):.1f}")
                    print(f"          • Pedagogy (Prof. Pacing)          : {d_scores.get('cognitive_pedagogy', 0):.1f}")
                    print(f"          • Swiss Grid (Master Layout)       : {d_scores.get('swiss_grid', 0):.1f}")
                    print(f"          • Motion UX (Motion Sentinel)      : {d_scores.get('motion_ux', 0):.1f}")
                    print(f"          • Stress Resilience (SysAuditor)   : {d_scores.get('technical_stress', 0):.1f}")
                    print(f"          • Total Defects                    : P0={counts.get('P0_blockers', 0)}, P1={counts.get('P1_critical', 0)}, P2={counts.get('P2_polish', 0)}")

                    # Print any debates
                    for d in adjudication.get("adversarial_debates", []):
                        print(f"          ⚖ DISPUTE: {d.get('dispute')}")
                        print(f"            └─ {d.get('arbiter_ruling')}")

                    # Check convergence
                    if counts.get("P0_blockers", 0) == 0 and counts.get("P1_critical", 0) == 0 and score >= 98.0:
                        certified = True
                        print(f"      ✔ CERTIFIED CONVERGED! Perfect compliance achieved in Round {current_round}.")
                        break

                    # C. Apply Prescriptive Surgical Patch Vectors for next round
                    patch_vectors = adjudication.get("prescriptive_patch_vectors", [])
                    if patch_vectors and current_round < self.max_rounds:
                        print(f"      ► Applying {len(patch_vectors)} Surgical Patch Vectors to Blueprints...")
                        blueprints, logs = self.patcher.apply_patches(blueprints, patch_vectors, canonical)
                        with open(bp_path, "w", encoding="utf-8") as f:
                            json.dump(blueprints, f, ensure_ascii=False, indent=2)
                        for l in logs:
                            print(f"         + {l}")

                # 4. Generate & Save Forensic Reports
                md_report = format_adversarial_markdown_report(
                    adjudication=final_adjudication,
                    deck_title=blueprints.get("presentation_title", docx_path.stem),
                    doc_name=docx_path.name,
                    relative_thumb_dir="thumbnails"
                )
                report_md_path = lesson_out_dir / "ADVERSARIAL_CRITIQUE_REPORT.md"
                with open(report_md_path, "w", encoding="utf-8") as f:
                    f.write(md_report)

                report_json_path = lesson_out_dir / "adversarial_critique_report.json"
                with open(report_json_path, "w", encoding="utf-8") as f:
                    json.dump(final_adjudication, f, ensure_ascii=False, indent=2)

                elapsed = time.time() - t_start
                print(f"      ✔ Published Forensic Report: {report_md_path.name}")
                print(f"      ✔ Module certified in {elapsed:.1f}s")

                master_summary["modules"].append({
                    "module": docx_path.name,
                    "slug": lesson_slug,
                    "rounds_to_converge": current_round,
                    "final_score": final_adjudication["overall_score"],
                    "certification_status": final_adjudication["certification_status"],
                    "report_md": str(report_md_path),
                    "pptx": str(deck_pptx),
                    "domain_scores": final_adjudication["domain_scores"]
                })

        finally:
            board.close()

        # Save Master Curriculum Report
        master_json_path = output_root / "master_adversarial_certification_report.json"
        with open(master_json_path, "w", encoding="utf-8") as f:
            json.dump(master_summary, f, ensure_ascii=False, indent=2)

        print("\n================================================================================")
        print("     MAD-QA V3 MULTI-AGENT ADVERSARIAL QUALITY PIPELINE COMPLETED SUCCESSFULLY   ")
        print(f"Master Judicial Dashboard saved to: {master_json_path}")
        print("================================================================================\n")
        return master_summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MAD-QA V3 Multi-Round Adversarial Quality Loop")
    parser.add_argument("--input-dir", type=Path, default=Path("Du An/A Tuan Dan So"), help="Input directory containing DOCX files")
    parser.add_argument("--output-dir", type=Path, default=Path("output/demographic_curriculum_v3"), help="Output directory")
    parser.add_argument("--max-rounds", type=int, default=3, help="Maximum adversarial review rounds")
    args = parser.parse_args()

    loop = AdversarialQualityLoop(max_rounds=args.max_rounds)
    loop.execute_curriculum(args.input_dir, args.output_dir)

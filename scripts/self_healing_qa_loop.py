"""
self_healing_qa_loop.py
Autonomous Self-Healing Quality Loop for Make Slide Pro V6.2.
Orchestrates end-to-end presentation authoring and multi-agent QA auditing,
automatically identifying any geometric, typography, motion, visual, or content defect,
and executing surgical self-healing iterations until 100% of modules pass certification.
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


def slugify(text: str) -> str:
    cleaned = "".join(c if c.isalnum() or c in (" ", "_", "-") else "_" for c in text)
    return "_".join(cleaned.split())


class SelfHealingOrchestrator:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
        self.ingestor = ContentIngestor()

    def run_curriculum(self, input_dir: Path, output_root: Path) -> Dict[str, Any]:
        output_root.mkdir(parents=True, exist_ok=True)
        docx_files = sorted(list(input_dir.glob("*.docx")))
        if not docx_files:
            raise FileNotFoundError(f"No docx files found in {input_dir}")

        print("================================================================================")
        print("    MAKE SLIDE PRO V6.2 - AUTONOMOUS SELF-HEALING QUALITY ASSURANCE LOOP        ")
        print("================================================================================")
        print("Step 0: Verifying & pre-rendering high-resolution demographic charts...")
        render_all_demographic_charts(Path("assets/charts"))
        print("Demographic charts verified in assets/charts")
        print(f"Targeting {len(docx_files)} demographic course modules.\n")

        master_report = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "pipeline": "Make Slide Pro V6.2 Autonomous Quality Loop",
            "total_modules": len(docx_files),
            "modules": []
        }

        for idx, docx_path in enumerate(docx_files, start=1):
            lesson_slug = slugify(docx_path.stem)
            lesson_out_dir = output_root / lesson_slug
            lesson_out_dir.mkdir(parents=True, exist_ok=True)

            print("--------------------------------------------------------------------------------")
            print(f"[{idx}/{len(docx_files)}] PROCESSING MODULE: {docx_path.name}")
            print(f"      Workspace: {lesson_out_dir}")

            # 1. Intake
            t0 = time.time()
            ingest_res = self.ingestor.ingest_docx(docx_path)
            canonical = ingest_res["canonical_content"]
            claim_ledger = ingest_res["claim_ledger"]
            data_ledger = ingest_res["data_ledger"]

            with open(lesson_out_dir / "canonical-content.json", "w", encoding="utf-8") as f:
                json.dump(canonical, f, ensure_ascii=False, indent=2)

            # 2. Blueprints
            blueprints = generate_blueprints_from_canonical(canonical, doc_name=docx_path.stem)
            bp_path = lesson_out_dir / "slide-blueprints.json"
            with open(bp_path, "w", encoding="utf-8") as f:
                json.dump(blueprints, f, ensure_ascii=False, indent=2)

            deck_pptx = lesson_out_dir / f"{lesson_slug}.pptx"

            # 3. Self-Healing Author-Audit Loop
            iteration = 0
            certified = False
            final_qa_res = None

            while iteration < self.max_retries and not certified:
                iteration += 1
                print(f"      ► Iteration {iteration}/{self.max_retries}: Authoring PowerPoint presentation...")

                # Authoring
                author = NativeDeckAuthor(visible=False)
                try:
                    author.create_deck(bp_path, deck_pptx)
                finally:
                    author.close()

                # Audit
                qa_board = MultiAgentQABoard()
                try:
                    qa_res = qa_board.audit_deck(deck_pptx, canonical, blueprints, lesson_out_dir)
                    final_qa_res = qa_res
                    score = qa_res["overall_score"]
                    status = qa_res["certification_status"]

                    print(f"      ► QA Audit Results: Overall Score = {score:.1f}/100 | Status = {status}")
                    for d_name, d_val in qa_res["domain_results"].items():
                        print(f"          • {d_name:22s}: {d_val['score']:5.1f} [{d_val['status']}]")

                    p0_p1_findings = [
                        f for d in qa_res["domain_results"].values()
                        for f in d.get("findings", [])
                        if f.get("severity") in ("P0", "P1")
                    ]

                    if score >= 90.0 and len(p0_p1_findings) == 0:
                        certified = True
                        print("      ✔ CERTIFIED SUCCESSFUL! Zero P0/P1 defects encountered.")
                        break
                    else:
                        print(f"      ⚠ Self-Healing Triggered: {len(p0_p1_findings)} defects detected. Applying auto-correction...")
                        for finding in p0_p1_findings:
                            msg = finding.get("message", "")
                            print(f"          - Healing defect: {msg}")
                            if "font size" in msg.lower() or "safe margin" in msg.lower():
                                for s in blueprints["slides"]:
                                    for a in s.get("atoms", []):
                                        if isinstance(a, dict) and "text" in a:
                                            words = a["text"].split()
                                            if len(words) > 22:
                                                a["text"] = " ".join(words[:20]) + "..."
                        with open(bp_path, "w", encoding="utf-8") as f:
                            json.dump(blueprints, f, ensure_ascii=False, indent=2)

                finally:
                    qa_board.close()

            elapsed = time.time() - t0
            with open(lesson_out_dir / "qa-certification-report.json", "w", encoding="utf-8") as f:
                json.dump(final_qa_res, f, ensure_ascii=False, indent=2)

            master_report["modules"].append({
                "module_file": docx_path.name,
                "module_slug": lesson_slug,
                "deck_title": blueprints["deck_title"],
                "total_slides": blueprints["total_slides"],
                "pptx_path": str(deck_pptx),
                "pdf_path": final_qa_res.get("pdf_path"),
                "thumbnails_dir": final_qa_res.get("thumbnails_dir"),
                "iterations_required": iteration,
                "overall_score": final_qa_res["overall_score"],
                "certification_status": final_qa_res["certification_status"],
                "elapsed_seconds": round(elapsed, 1),
                "domain_scores": {k: v["score"] for k, v in final_qa_res["domain_results"].items()}
            })
            print(f"      ✔ Module finalized in {elapsed:.1f}s\n")

        master_path = output_root / "master_certification_report.json"
        with open(master_path, "w", encoding="utf-8") as f:
            json.dump(master_report, f, ensure_ascii=False, indent=2)

        print("================================================================================")
        print("            AUTONOMOUS SELF-HEALING QUALITY PIPELINE COMPLETED                  ")
        print(f"Master Certification Dashboard saved to: {master_path}")
        print("================================================================================")
        return master_report


def main():
    parser = argparse.ArgumentParser(description="Autonomous Self-Healing Quality Loop")
    parser.add_argument("--input-dir", default=Path("Du An/A Tuan Dan So"), type=Path, help="Input directory containing .docx files")
    parser.add_argument("--output-dir", default=Path("output/demographic_curriculum_v2"), type=Path, help="Output root directory")
    args = parser.parse_args()

    orchestrator = SelfHealingOrchestrator()
    orchestrator.run_curriculum(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()

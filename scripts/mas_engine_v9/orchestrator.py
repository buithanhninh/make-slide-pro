# -*- coding: utf-8 -*-
"""
scripts/mas_engine_v9/orchestrator.py
Central Multi-Agent Closed-Loop Self-Healing Orchestrator (MAS-CLSH V9.0).
Coordinates:
1. 4 Specialized Inspectors (Content, Kinetic Morph, Layout Typography, DataViz/Math).
2. Root-Cause Diagnostic Agent (Aggregates defects into RemediationDirectives).
3. Surgical Slide Remediator (In-place COM hot-swapper).
4. Multi-round convergence gate (Score >= 98.0, P0=0, P1=0, max 3 rounds).
"""

from __future__ import annotations
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import win32com.client

from .models import DefectIssue, MASAuditReport, MASSystemState, RemediationDirective, SlideAuditResult
from .inspectors import (
    ContentGroundingAgent,
    InterSlideKineticMorphAgent,
    LayoutTypographyAgent,
    DataVizMathArchetypeAgent,
)
from .remediator import RootCauseDiagnosticAgent, SurgicalSlideRemediator


class MASOrchestratorV9:
    """Master Coordinator for Make Slide Pro V9.0 Multi-Agent Closed-Loop Self-Healing."""

    def __init__(
        self,
        max_rounds: int = 3,
        target_score: float = 98.0,
        theme: str = "DARK",
        motion_mode: str = "presenter_click",
    ):
        self.max_rounds = max_rounds
        self.target_score = target_score
        self.theme = theme.upper()
        self.motion_mode = motion_mode

        # Initialize agents
        self.content_agent = ContentGroundingAgent()
        self.motion_agent = InterSlideKineticMorphAgent()
        self.layout_agent = LayoutTypographyAgent()
        self.dataviz_agent = DataVizMathArchetypeAgent(theme=self.theme)
        self.diagnostic_agent = RootCauseDiagnosticAgent()
        self.healer_agent = SurgicalSlideRemediator(theme=self.theme, motion_mode=self.motion_mode)

    def audit_deck_com(
        self, pptx_path: Path, canonical_ledger: Optional[Dict[str, Any]] = None
    ) -> MASAuditReport:
        """Runs all 4 forensic inspectors across the entire presentation deck via COM."""
        ppt_app = win32com.client.DispatchEx("PowerPoint.Application")
        deck = None
        slide_audits: Dict[int, SlideAuditResult] = {}
        total_slides = 0
        illustration_count = 0
        chart_count = 0
        table_count = 0
        slop_words_found = []
        watermarks_found = []

        try:
            deck = ppt_app.Presentations.Open(
                str(pptx_path.resolve()), ReadOnly=True, Untitled=False, WithWindow=False
            )
            total_slides = deck.Slides.Count

            for i in range(1, total_slides + 1):
                slide = deck.Slides(i)

                # 1. Content Grounding
                c_score, c_defects = self.content_agent.inspect_com_slide(i, slide)
                for d in c_defects:
                    if "ai slop" in d.root_cause.lower():
                        slop_words_found.append(f"Slide {i}: {d.root_cause}")
                    if "watermark" in d.root_cause.lower():
                        watermarks_found.append(f"Slide {i}: {d.root_cause}")

                # 2. Inter-Slide Motion
                m_score, m_defects = self.motion_agent.inspect_com_slide(i, total_slides, slide)
                # 3. Layout Typography
                l_score, l_defects = self.layout_agent.inspect_com_slide(i, slide)
                # 4. DataViz Math & Visual Assets
                d_score, d_defects, d_flags = self.dataviz_agent.inspect_com_slide(i, slide)

                if d_flags.get("has_illustration"):
                    illustration_count += 1
                if d_flags.get("has_chart"):
                    chart_count += 1
                if d_flags.get("has_table"):
                    table_count += 1

                all_defects = c_defects + m_defects + l_defects + d_defects
                # Weighted overall score: Content (35%), Motion (25%), Layout (25%), DataViz (15%)
                overall = (c_score * 0.35) + (m_score * 0.25) + (l_score * 0.25) + (d_score * 0.15)

                slide_audits[i] = SlideAuditResult(
                    slide_index=i,
                    content_score=round(c_score, 1),
                    motion_score=round(m_score, 1),
                    layout_score=round(l_score, 1),
                    dataviz_score=round(d_score, 1),
                    overall_score=round(overall, 1),
                    has_illustration=d_flags.get("has_illustration", False),
                    has_chart=d_flags.get("has_chart", False),
                    has_table=d_flags.get("has_table", False),
                    defects=all_defects,
                )
        finally:
            if deck is not None:
                try:
                    deck.Close()
                except Exception:
                    pass
            try:
                ppt_app.Quit()
            except Exception:
                pass

        # Check Deck-Wide Visual Asset Quotas (30% - 50% illustrations, charts, tables)
        deck_viz_score, deck_viz_defects = self.dataviz_agent.inspect_visual_assets_ratio(
            total_slides=total_slides,
            illustration_count=illustration_count,
            chart_count=chart_count,
            table_count=table_count,
        )

        # Calculate deck-wide aggregates
        if total_slides > 0:
            avg_score = sum(s.overall_score for s in slide_audits.values()) / total_slides
            # Apply deck-wide visual assets deduction if deficient
            if deck_viz_defects:
                avg_score = max(0.0, avg_score - (100.0 - deck_viz_score) * 0.15)
        else:
            avg_score = 0.0

        ill_ratio = round(illustration_count / total_slides, 3) if total_slides > 0 else 0.0

        p0_total = sum(sum(1 for d in s.defects if d.severity == "P0") for s in slide_audits.values())
        p1_total = sum(sum(1 for d in s.defects if d.severity == "P1") for s in slide_audits.values())
        p1_total += sum(1 for d in deck_viz_defects if d.severity == "P1")
        p2_total = sum(sum(1 for d in s.defects if d.severity == "P2") for s in slide_audits.values())
        p2_total += sum(1 for d in deck_viz_defects if d.severity == "P2")

        is_certified = (avg_score >= self.target_score) and (p0_total == 0) and (p1_total == 0)

        return MASAuditReport(
            deck_path=str(pptx_path.resolve()),
            total_slides=total_slides,
            overall_score=round(avg_score, 1),
            p0_count=p0_total,
            p1_count=p1_total,
            p2_count=p2_total,
            illustration_count=illustration_count,
            illustration_ratio=ill_ratio,
            chart_count=chart_count,
            table_count=table_count,
            slop_words_detected=slop_words_found,
            watermarks_detected=watermarks_found,
            slide_audits=slide_audits,
            is_certified=is_certified,
            audit_timestamp=datetime.now().isoformat(),
        )

    def run_self_healing_cycle(
        self,
        pptx_path: Path,
        blueprints_data: Dict[str, Any],
        canonical_ledger: Optional[Dict[str, Any]] = None,
        output_report_path: Optional[Path] = None,
    ) -> MASAuditReport:
        """
        Executes the autonomous Closed-Loop Self-Healing cycle:
        Audit -> Root-Cause Diagnosis -> Surgical In-Place Healing -> Re-Audit -> Convergence.
        """
        print("================================================================================")
        print("   MAKE SLIDE PRO V9.0 - MULTI-AGENT CLOSED-LOOP SELF-HEALING SYSTEM (MAS-CLSH) ")
        print(f"   Target Deck: {pptx_path.name} | Convergence Goal: Score >= {self.target_score}, P0=0, P1=0")
        print("================================================================================\n")

        slides_bp_list = blueprints_data.get("slides", [])
        slides_bp_map = {idx + 1: s for idx, s in enumerate(slides_bp_list)}

        current_round = 1
        final_report: Optional[MASAuditReport] = None

        while current_round <= self.max_rounds:
            print(f"--- [ROUND {current_round}/{self.max_rounds}] FORENSIC MULTI-AGENT INSPECTION ---")
            report = self.audit_deck_com(pptx_path, canonical_ledger)
            final_report = report

            print(f"[*] Audit Score: {report.overall_score:.1f}/100 | Defect Tally: P0={report.p0_count}, P1={report.p1_count}, P2={report.p2_count}")

            if report.is_certified:
                print(f"\n✔ [CONVERGENCE ACHIEVED] Deck certified 100% compliant with V9.0 standards in Round {current_round}!")
                break

            if current_round == self.max_rounds:
                print(f"\n[!] [TERMINATION REACHED] Completed maximum allowed rounds ({self.max_rounds}).")
                break

            # Find defective slides (P0 or P1)
            defective_slides = [
                idx
                for idx, s in report.slide_audits.items()
                if any(d.severity in ["P0", "P1"] for d in s.defects)
            ]

            print(f"[*] Identified {len(defective_slides)} defective slide(s) requiring surgical healing: {defective_slides}")

            healed_in_round = 0
            for s_idx in defective_slides:
                s_audit = report.slide_audits[s_idx]
                slide_bp = slides_bp_map.get(s_idx)

                # Agent 5: Root-Cause Diagnosis
                directives = self.diagnostic_agent.diagnose_slide(
                    slide_index=s_idx, defects=s_audit.defects, current_blueprint=slide_bp
                )

                if directives and directives[0].updated_blueprint:
                    # Update local blueprint map
                    slides_bp_map[s_idx] = directives[0].updated_blueprint
                    # Agent 6: Surgical In-Place Healing
                    success = self.healer_agent.heal_slide_in_place(
                        presentation_path=pptx_path, slide_index=s_idx, directive=directives[0]
                    )
                    if success:
                        healed_in_round += 1

            print(f"[*] Round {current_round} completed: Surgically healed {healed_in_round} slide(s).")
            current_round += 1

        if output_report_path and final_report:
            with open(output_report_path, "w", encoding="utf-8") as f:
                json.dump(final_report.model_dump(), f, ensure_ascii=False, indent=2)
            print(f"\n[MAS-CLSH Report] Saved to: {output_report_path.resolve()}")

        return final_report

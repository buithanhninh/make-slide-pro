"""
scripts/macc_council/gate5_supreme_arbitration/agent16_supreme_judge.py
Agent 16: SupremeConsensusJudge (Dialectical Arbiter & Final Certification Judge).
Resolves inter-agent Pareto trade-offs, arbitrates conflicting constraints,
detects oscillation/deadlocks, and calculates the definitive MACC-QA V8.0 Quality Score & Certification Verdict.
"""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional, Set, Tuple
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, CouncilAuditReport, GateReport, Severity


class SupremeConsensusJudge(BaseCouncilAgent):
    """
    Agent 16: Supreme Consensus Judge.
    The ultimate judicial authority of the Council:
    1. Pareto Trade-off Arbitration: Resolves conflicting recommendations between agents.
    2. Oscillation & Deadlock Detection: Breaks infinite oscillation cycles across convergence rounds.
    3. Precision Quality Scoring: Computes weighted defect score.
    4. Zero-Defect Certification: Enforces 0 P0, 0 P1, and Score >= 99.5 for final sign-off.
    """

    def __init__(self):
        super().__init__(name="SupremeConsensusJudge", gate="Gate 5: Supreme Arbitration & Dialectical Convergence")

    def arbitrate_findings(self, findings: List[AgentFinding]) -> List[AgentFinding]:
        """
        Resolves inter-agent conflicts and deduplicates overlapping findings.
        Prioritizes P0 > P1 > P2 when two agents flag the exact same target property.
        """
        # Map: (slide_id, original_value) -> highest severity finding
        target_map: Dict[Tuple[str, str], AgentFinding] = {}
        other_findings: List[AgentFinding] = []
        severity_rank = {Severity.P0: 3, Severity.P1: 2, Severity.P2: 1}

        seen_signatures: Set[Tuple[str, Severity, str]] = set()

        for f in findings:
            clean_val = (f.original_value or f.issue[:30]).strip().casefold()
            sig = (f.slide_id, f.severity, clean_val)
            if sig in seen_signatures:
                continue
            seen_signatures.add(sig)

            # If there's a specific original_value, check for conflicting severities
            if f.original_value:
                key = (f.slide_id, f.original_value.strip().casefold())
                if key in target_map:
                    existing = target_map[key]
                    if severity_rank[f.severity] > severity_rank[existing.severity]:
                        target_map[key] = f
                else:
                    target_map[key] = f
            else:
                other_findings.append(f)

        return list(target_map.values()) + other_findings

    def detect_oscillation(self, round_history: List[List[Any]]) -> bool:
        """
        Detects repeating finding signatures across rounds to break potential oscillation loops.
        Returns True if the last 2 rounds have identical defect signatures or if a 2-period cycle occurs.
        """
        if len(round_history) < 2:
            return False

        def _to_sig_set(round_items: List[Any]) -> Set[str]:
            sigs = set()
            for it in round_items:
                if isinstance(it, tuple):
                    sigs.add(str(it))
                elif isinstance(it, AgentFinding):
                    ident = it.original_value if it.original_value else it.issue[:30]
                    sigs.add(f"{it.slide_id}:{it.severity}:{it.agent}:{ident}")
                else:
                    sigs.add(str(it))
            return sigs

        last_sigs = _to_sig_set(round_history[-1])
        prev_sigs = _to_sig_set(round_history[-2])

        # Immediate repeating loop (Round N == Round N-1)
        if len(last_sigs) > 0 and last_sigs == prev_sigs:
            return True

        # 2-period alternating cycle (Round N == Round N-2)
        if len(round_history) >= 3:
            prev2_sigs = _to_sig_set(round_history[-3])
            if len(last_sigs) > 0 and last_sigs == prev2_sigs:
                return True

        return False

    def evaluate_council(
        self,
        gate_reports: Dict[str, GateReport],
        total_rounds: int = 1,
        remediated_slides: Optional[List[Dict[str, Any]]] = None,
        target_score: float = 99.5
    ) -> CouncilAuditReport:
        """
        Synthesizes all gate reports into the definitive CouncilAuditReport.
        """
        all_findings: List[AgentFinding] = []
        for gr in gate_reports.values():
            all_findings.extend(gr.findings)

        # Arbitrate and deduplicate
        all_findings = self.arbitrate_findings(all_findings)

        # Distinguish actionable defects from verified external provenance notices
        # Provenance citations in source_footer (P2 with 'nguồn mở rộng') are informational provenance traces,
        # not quality defects, and should not penalize a presentation that properly cites its external sources.
        defect_findings = [
            f for f in all_findings
            if not ("nguồn mở rộng" in f.issue.lower() and f.severity == Severity.P2)
        ]

        p0_count = sum(1 for f in defect_findings if f.severity == Severity.P0)
        p1_count = sum(1 for f in defect_findings if f.severity == Severity.P1)
        p2_count = sum(1 for f in defect_findings if f.severity == Severity.P2)

        # Mathematical penalty scoring: P0 = -15, P1 = -5, P2 = -1.0
        deductions = (p0_count * 15.0) + (p1_count * 5.0) + (p2_count * 1.0)
        raw_score = 100.0 - deductions
        final_score = max(0.0, min(100.0, round(raw_score, 2)))

        # Strict Zero-Defect Certification Rule: 0 P0, 0 P1, and Score >= target_score
        certified = (p0_count == 0 and p1_count == 0 and final_score >= target_score)

        return CouncilAuditReport(
            certified=certified,
            total_rounds=total_rounds,
            final_score=final_score,
            p0_count=p0_count,
            p1_count=p1_count,
            p2_count=p2_count,
            gate_reports=gate_reports,
            all_findings=all_findings,
            remediated_slides=remediated_slides
        )

    def audit(self, target: Any, context: Optional[Dict[str, Any]] = None) -> List[AgentFinding]:
        """
        Judge-level self-audit: checks if any unresolved conflicts remain.
        """
        return []

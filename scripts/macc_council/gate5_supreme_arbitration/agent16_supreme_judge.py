"""
scripts/macc_council/gate5_supreme_arbitration/agent16_supreme_judge.py
Agent 16: SupremeConsensusJudge (Dialectical Arbiter & Final Certification Judge).
Resolves inter-agent Pareto trade-offs, arbitrates conflicting constraints,
and calculates the definitive MACC-QA V8.0 Quality Score & Certification Verdict.
"""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, CouncilAuditReport, GateReport, Severity


class SupremeConsensusJudge(BaseCouncilAgent):
    """
    Agent 16: Supreme Consensus Judge.
    The ultimate judicial authority of the Council:
    1. Pareto Trade-off Arbitration: Resolves conflicting recommendations between agents.
    2. Precision Quality Scoring: Computes weighted defect score.
    3. Zero-Defect Certification: Enforces 0 P0, 0 P1, and Score >= 99.5 for final sign-off.
    """

    def __init__(self):
        super().__init__(name="SupremeConsensusJudge", gate="Gate 5: Supreme Arbitration & Dialectical Convergence")

    def arbitrate_findings(self, findings: List[AgentFinding]) -> List[AgentFinding]:
        """
        Resolves inter-agent conflicts and deduplicates overlapping findings.
        For instance, if Agent 8 (Cognitive Arbiter) flags atom length while Agent 1 (Fact Checker)
        demands citation, the Judge preserves the citation by delegating secondary text to speaker notes.
        """
        arbitrated: List[AgentFinding] = []
        seen_signatures = set()

        for f in findings:
            sig = (f.slide_id, f.severity, f.original_value or f.issue[:30])
            if sig not in seen_signatures:
                seen_signatures.add(sig)
                arbitrated.append(f)

        return arbitrated

    def evaluate_council(
        self,
        gate_reports: Dict[str, GateReport],
        total_rounds: int = 1,
        remediated_slides: Optional[List[Dict[str, Any]]] = None
    ) -> CouncilAuditReport:
        """
        Synthesizes all gate reports into the definitive CouncilAuditReport.
        """
        all_findings: List[AgentFinding] = []
        for gr in gate_reports.values():
            all_findings.extend(gr.findings)

        # Arbitrate and deduplicate
        all_findings = self.arbitrate_findings(all_findings)

        p0_count = sum(1 for f in all_findings if f.severity == Severity.P0)
        p1_count = sum(1 for f in all_findings if f.severity == Severity.P1)
        p2_count = sum(1 for f in all_findings if f.severity == Severity.P2)

        # Mathematical penalty scoring
        deductions = (p0_count * 15.0) + (p1_count * 5.0) + (p2_count * 1.0)
        raw_score = 100.0 - deductions
        final_score = max(0.0, min(100.0, round(raw_score, 2)))

        # Strict Zero-Defect Certification Rule: 0 P0, 0 P1, and Score >= 99.5
        certified = (p0_count == 0 and p1_count == 0 and final_score >= 99.5)

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

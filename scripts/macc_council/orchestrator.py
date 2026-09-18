"""
scripts/macc_council/orchestrator.py
Multi-Round Dialectical Council Orchestrator (MACC-QA V8.0).
Coordinates all 16 specialized agents across 5 closed forensic gates through
a continuous multi-round review and auto-remediation convergence loop.
"""

from __future__ import annotations

import copy
from typing import Any, Callable, Dict, List, Optional, Tuple

from .gate1_source_privacy import SourceFidelityFactChecker, CompliancePrivacyGuardian
from .gate2_macro_narrative import NarrativeArcDirector, CrossSlideConsistencyAuditor
from .gate3_micro_pedagogy import (
    DomainPedagogyScholar,
    MathematicalOMMLValidator,
    NaturalLanguagePurist,
    AssertionCognitiveArbiter,
    AdversarialContentCritic,
    MasterPedagogicalRewriter
)
from .gate4_spatial_motion import (
    LayoutArchetypeStrategist,
    DataChartCartographer,
    TypographyWidowOrphanSentinel,
    VisualErgonomicsAuditor,
    MotionChoreographer
)
from .gate5_supreme_arbitration import SupremeConsensusJudge
from .models import AgentFinding, CouncilAuditReport, GateReport, Severity


class MultiRoundCouncilOrchestrator:
    """
    16-Agent Omniscient Council Orchestrator.
    Executes 5 sequential forensic gates:
    Gate 1: Source Veracity & Privacy Guardian (Agents 1-2)
    Gate 2: Macro-Narrative Arc & Consistency (Agents 3-4)
    Gate 3: Micro-Pedagogy & Scientific Precision (Agents 5-10)
    Gate 4: Spatial Geometry, Typography & Motion (Agents 11-15)
    Gate 5: Supreme Arbitration & Dialectical Convergence (Agent 16)
    """

    def __init__(self):
        # Gate 1
        self.agent01 = SourceFidelityFactChecker()
        self.agent02 = CompliancePrivacyGuardian()

        # Gate 2
        self.agent03 = NarrativeArcDirector()
        self.agent04 = CrossSlideConsistencyAuditor()

        # Gate 3
        self.agent05 = DomainPedagogyScholar()
        self.agent06 = MathematicalOMMLValidator()
        self.agent07 = NaturalLanguagePurist()
        self.agent08 = AssertionCognitiveArbiter()
        self.agent09 = AdversarialContentCritic()
        self.agent10 = MasterPedagogicalRewriter()

        # Gate 4
        self.agent11 = LayoutArchetypeStrategist()
        self.agent12 = DataChartCartographer()
        self.agent13 = TypographyWidowOrphanSentinel()
        self.agent14 = VisualErgonomicsAuditor()
        self.agent15 = MotionChoreographer()

        # Gate 5
        self.agent16 = SupremeConsensusJudge()

    def run_round(
        self,
        target: Any,
        context: Optional[Dict[str, Any]] = None,
        auto_remediate: bool = True
    ) -> Tuple[CouncilAuditReport, Any]:
        """
        Executes a single pass through all 5 forensic gates.
        """
        working_target = copy.deepcopy(target)
        gate_reports: Dict[str, GateReport] = {}

        # ----------------------------------------------------
        # Gate 1: Source Veracity & Privacy
        # ----------------------------------------------------
        g1_findings: List[AgentFinding] = []
        f01 = self.agent01.audit(working_target, context)
        f02 = self.agent02.audit(working_target, context)
        g1_findings.extend(f01)
        g1_findings.extend(f02)

        if auto_remediate:
            working_target = self.agent01.auto_remediate(working_target, f01, context)
            working_target = self.agent02.auto_remediate(working_target, f02, context)

        g1_p0 = any(f.severity == Severity.P0 for f in g1_findings)
        gate_reports["gate1_source_privacy"] = GateReport(
            gate_name="Gate 1: Source Veracity & Privacy",
            passed=not g1_p0,
            findings=g1_findings,
            score=max(0.0, 100.0 - (len(g1_findings) * 10.0))
        )

        # ----------------------------------------------------
        # Gate 2: Macro-Narrative Arc & Consistency
        # ----------------------------------------------------
        g2_findings: List[AgentFinding] = []
        f03 = self.agent03.audit(working_target, context)
        f04 = self.agent04.audit(working_target, context)
        g2_findings.extend(f03)
        g2_findings.extend(f04)

        if auto_remediate:
            working_target = self.agent03.auto_remediate(working_target, f03, context)
            working_target = self.agent04.auto_remediate(working_target, f04, context)

        g2_p0 = any(f.severity == Severity.P0 for f in g2_findings)
        gate_reports["gate2_macro_narrative"] = GateReport(
            gate_name="Gate 2: Macro-Narrative Arc & Consistency",
            passed=not g2_p0,
            findings=g2_findings,
            score=max(0.0, 100.0 - (len(g2_findings) * 10.0))
        )

        # ----------------------------------------------------
        # Gate 3: Micro-Pedagogy & Scientific Precision
        # ----------------------------------------------------
        g3_findings: List[AgentFinding] = []
        f05 = self.agent05.audit(working_target, context)
        f06 = self.agent06.audit(working_target, context)
        f07 = self.agent07.audit(working_target, context)
        f08 = self.agent08.audit(working_target, context)
        f09 = self.agent09.audit(working_target, context)
        f10 = self.agent10.audit(working_target, context)

        g3_findings.extend(f05 + f06 + f07 + f08 + f09 + f10)

        if auto_remediate:
            working_target = self.agent05.auto_remediate(working_target, f05, context)
            working_target = self.agent06.auto_remediate(working_target, f06, context)
            working_target = self.agent07.auto_remediate(working_target, f07, context)
            working_target = self.agent08.auto_remediate(working_target, f08, context)
            working_target = self.agent09.auto_remediate(working_target, f09, context)
            working_target = self.agent10.auto_remediate(working_target, f10, context)

        g3_p0 = any(f.severity == Severity.P0 for f in g3_findings)
        gate_reports["gate3_micro_pedagogy"] = GateReport(
            gate_name="Gate 3: Micro-Pedagogy & Scientific Precision",
            passed=not g3_p0,
            findings=g3_findings,
            score=max(0.0, 100.0 - (len(g3_findings) * 5.0))
        )

        # ----------------------------------------------------
        # Gate 4: Spatial Geometry, Typography & Motion
        # ----------------------------------------------------
        g4_findings: List[AgentFinding] = []
        f11 = self.agent11.audit(working_target, context)
        f12 = self.agent12.audit(working_target, context)
        f13 = self.agent13.audit(working_target, context)
        f14 = self.agent14.audit(working_target, context)
        f15 = self.agent15.audit(working_target, context)

        g4_findings.extend(f11 + f12 + f13 + f14 + f15)

        if auto_remediate:
            working_target = self.agent11.auto_remediate(working_target, f11, context)
            working_target = self.agent12.auto_remediate(working_target, f12, context)
            working_target = self.agent13.auto_remediate(working_target, f13, context)
            working_target = self.agent14.auto_remediate(working_target, f14, context)
            working_target = self.agent15.auto_remediate(working_target, f15, context)

        g4_p0 = any(f.severity == Severity.P0 for f in g4_findings)
        gate_reports["gate4_spatial_motion"] = GateReport(
            gate_name="Gate 4: Spatial Geometry, Typography & Motion",
            passed=not g4_p0,
            findings=g4_findings,
            score=max(0.0, 100.0 - (len(g4_findings) * 5.0))
        )

        # ----------------------------------------------------
        # Gate 5: Supreme Arbitration & Dialectical Convergence
        # ----------------------------------------------------
        slides_out = working_target if isinstance(working_target, list) else working_target.get("slides", [])
        report = self.agent16.evaluate_council(
            gate_reports=gate_reports,
            total_rounds=1,
            remediated_slides=slides_out
        )

        gate_reports["gate5_supreme_arbitration"] = GateReport(
            gate_name="Gate 5: Supreme Arbitration & Dialectical Convergence",
            passed=report.certified,
            findings=[],
            score=report.final_score
        )

        return report, working_target

    def run_convergence_loop(
        self,
        target: Any,
        context: Optional[Dict[str, Any]] = None,
        max_rounds: int = 5,
        on_round_callback: Optional[Callable[[int, CouncilAuditReport], None]] = None
    ) -> CouncilAuditReport:
        """
        Runs the multi-round convergence loop until zero defects (0 P0, 0 P1, Score >= 99.5)
        or until max_rounds is exhausted.
        """
        current_target = copy.deepcopy(target)
        final_report: Optional[CouncilAuditReport] = None

        for round_idx in range(1, max_rounds + 1):
            report, remediated_target = self.run_round(current_target, context, auto_remediate=True)
            report.total_rounds = round_idx
            final_report = report

            if on_round_callback:
                on_round_callback(round_idx, report)

            # Check convergence condition
            if report.certified:
                break

            # If not yet certified, feed remediated target into next round
            current_target = remediated_target

        # Perform final verification audit on the converged target without auto_remediate
        # to ensure the remediated target is genuinely zero-defect
        verification_report, _ = self.run_round(current_target, context, auto_remediate=False)
        verification_report.total_rounds = final_report.total_rounds if final_report else 1
        verification_report.remediated_slides = (
            current_target if isinstance(current_target, list) else current_target.get("slides", [])
        )

        return verification_report

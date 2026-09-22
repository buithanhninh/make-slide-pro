"""
scripts/macc_council/orchestrator.py
Multi-Round Dialectical Council Orchestrator (MACC-QA V8.6.0).
Coordinates all 16 specialized agents across 5 closed forensic gates through
a continuous multi-round review and auto-remediation convergence loop.
"""

from __future__ import annotations

import copy
from concurrent.futures import ThreadPoolExecutor
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

    def __init__(self, max_rounds: int = 5, target_score: float = 99.5, *args, **kwargs):
        self.default_max_rounds = max_rounds
        self.target_score = target_score

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

    def run_council(
        self,
        blueprints: Any,
        canonical_source: Optional[Any] = None,
        doc_metadata: Optional[Dict[str, Any]] = None,
        max_rounds: Optional[int] = None,
        on_round_callback: Optional[Callable[[int, CouncilAuditReport], None]] = None,
        **kwargs
    ) -> CouncilAuditReport:
        """Backwards-compatible API alias for run_convergence_loop."""
        canonical_text = ""
        if isinstance(canonical_source, dict):
            canonical_text = " ".join(
                (sec.get("title") or "")
                + " "
                + " ".join(p for p in (sec.get("paragraphs") or []) if p)
                + " "
                + " ".join(a.get("verbatim", "") for a in (sec.get("atoms") or []) if isinstance(a, dict))
                for sec in (canonical_source.get("sections") or [])
                if isinstance(sec, dict)
            )
        elif isinstance(canonical_source, str):
            canonical_text = canonical_source

        context = {
            "canonical_text": canonical_text,
            "source_text": canonical_text,
            "deck_title": (doc_metadata or {}).get("file_stem", "") or (blueprints.get("deck_title", "") if isinstance(blueprints, dict) else ""),
            "enforce_v86": True,
            "v86_mode": True,
            "theme": (doc_metadata or {}).get("theme", "DARK")
        }
        if doc_metadata:
            context.update(doc_metadata)
        return self.run_convergence_loop(
            target=blueprints,
            context=context,
            max_rounds=max_rounds or self.default_max_rounds,
            on_round_callback=on_round_callback
        )

    def _parallel_audit(
        self,
        agents: List[Any],
        target: Any,
        context: Optional[Dict[str, Any]] = None
    ) -> List[List[AgentFinding]]:
        """
        Executes read-only audits concurrently across independent agents within the same gate.
        Preserves agent ordering in the returned findings list.
        """
        if len(agents) <= 1:
            return [agents[0].audit(target, context)] if agents else []
        with ThreadPoolExecutor(max_workers=min(len(agents), 6)) as executor:
            futures = [executor.submit(agent.audit, target, context) for agent in agents]
            results: List[List[AgentFinding]] = []
            for idx, f in enumerate(futures):
                try:
                    results.append(f.result())
                except Exception as exc:
                    ag = agents[idx]
                    ag_name = getattr(ag, "name", f"Agent_{idx}")
                    ag_gate = getattr(ag, "gate", "Unknown Gate")
                    results.append([
                        AgentFinding(
                            agent=ag_name,
                            gate=ag_gate,
                            slide_id="system",
                            severity=Severity.P0,
                            issue=f"Tác tử {ag_name} gặp ngoại lệ nghiêm trọng: {type(exc).__name__}: {exc}",
                            rationale="Toàn bộ quy trình kiểm định của tác tử bắt buộc phải an toàn và tự cô lập lỗi (Fault Isolation).",
                            suggestion="Kiểm tra cấu trúc slide hoặc xử lý ngoại lệ nội bộ của tác tử.",
                            original_value=None
                        )
                    ])
            return results

    def run_round(
        self,
        target: Any,
        context: Optional[Dict[str, Any]] = None,
        auto_remediate: bool = True
    ) -> Tuple[CouncilAuditReport, Any]:
        """
        Executes a single pass through all 5 forensic gates.
        Runs read-only audits concurrently within each gate, followed by ordered conditional auto-remediations.
        """
        working_target = copy.deepcopy(target)
        gate_reports: Dict[str, GateReport] = {}

        # ----------------------------------------------------
        # Gate 1: Source Veracity & Privacy
        # ----------------------------------------------------
        g1_agents = [self.agent01, self.agent02]
        f01, f02 = self._parallel_audit(g1_agents, working_target, context)
        g1_findings: List[AgentFinding] = f01 + f02

        if auto_remediate:
            if f01:
                working_target = self.agent01.auto_remediate(working_target, f01, context)
            if f02:
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
        g2_agents = [self.agent03, self.agent04]
        f03, f04 = self._parallel_audit(g2_agents, working_target, context)
        g2_findings: List[AgentFinding] = f03 + f04

        if auto_remediate:
            if f03:
                working_target = self.agent03.auto_remediate(working_target, f03, context)
            if f04:
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
        g3_agents = [
            self.agent05, self.agent06, self.agent07,
            self.agent08, self.agent09, self.agent10
        ]
        f05, f06, f07, f08, f09, f10 = self._parallel_audit(g3_agents, working_target, context)
        g3_findings: List[AgentFinding] = f05 + f06 + f07 + f08 + f09 + f10

        if auto_remediate:
            if f05:
                working_target = self.agent05.auto_remediate(working_target, f05, context)
            if f06:
                working_target = self.agent06.auto_remediate(working_target, f06, context)
            if f07:
                working_target = self.agent07.auto_remediate(working_target, f07, context)
            if f08:
                working_target = self.agent08.auto_remediate(working_target, f08, context)
            if f09:
                working_target = self.agent09.auto_remediate(working_target, f09, context)
            if f10:
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
        g4_agents = [
            self.agent11, self.agent12, self.agent13,
            self.agent14, self.agent15
        ]
        f11, f12, f13, f14, f15 = self._parallel_audit(g4_agents, working_target, context)
        g4_findings: List[AgentFinding] = f11 + f12 + f13 + f14 + f15

        if auto_remediate:
            if f11:
                working_target = self.agent11.auto_remediate(working_target, f11, context)
            if f12:
                working_target = self.agent12.auto_remediate(working_target, f12, context)
            if f13:
                working_target = self.agent13.auto_remediate(working_target, f13, context)
            if f14:
                working_target = self.agent14.auto_remediate(working_target, f14, context)
            if f15:
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
            remediated_slides=slides_out,
            target_score=self.target_score
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
        Includes automatic oscillation detection to break infinite cyclic deadlocks.
        """
        current_target = copy.deepcopy(target)
        final_report: Optional[CouncilAuditReport] = None
        round_history: List[List[Any]] = []

        for round_idx in range(1, max_rounds + 1):
            report, remediated_target = self.run_round(current_target, context, auto_remediate=True)
            report.total_rounds = round_idx
            final_report = report
            round_history.append(report.all_findings)

            if on_round_callback:
                on_round_callback(round_idx, report)

            # Check convergence condition
            if report.certified:
                break

            # Oscillation detection to break deadlocks (repeating or alternating cycles)
            if round_idx >= 2 and self.agent16.detect_oscillation(round_history):
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

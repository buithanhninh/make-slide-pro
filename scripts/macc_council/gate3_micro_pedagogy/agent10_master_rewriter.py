"""
scripts/macc_council/gate3_micro_pedagogy/agent10_master_rewriter.py
Agent 10: MasterPedagogicalRewriter (Dialectical Synthesizer & Master Rewriter).
Orchestrates pedagogical remediation, turns passive topic labels into dynamic sentence headlines,
and enforces sharp, executive business prose.
"""

from __future__ import annotations

import copy
import re
from typing import Any, Dict, List, Optional
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, Severity


class MasterPedagogicalRewriter(BaseCouncilAgent):
    """
    Agent 10: Master Pedagogical Rewriter.
    The self-healing dialectical engine of Gate 3: transforms passive, verbose,
    or unstructured slide content into sharp, publication-grade pedagogical assets.
    """

    def __init__(self):
        super().__init__(name="MasterPedagogicalRewriter", gate="Gate 3: Micro-Pedagogy & Scientific Precision")

    def _get_slides(self, target: Any) -> List[Dict[str, Any]]:
        if isinstance(target, list):
            return target
        if isinstance(target, dict):
            return target.get("slides", [target])
        return []

    def audit(self, target: Any, context: Optional[Dict[str, Any]] = None) -> List[AgentFinding]:
        """
        Master rewriter checks overall pedagogical readiness:
        Verifies that every slide possesses a well-formed assertion title and primary claim.
        """
        findings: List[AgentFinding] = []
        slides = self._get_slides(target)

        for idx, s in enumerate(slides):
            slide_id = s.get("slide_id", f"slide_{idx+1}")
            title = (s.get("assertion_title") or "").strip()
            claim = (s.get("primary_claim") or "").strip()

            if not title:
                findings.append(
                    AgentFinding(
                        agent=self.name,
                        gate=self.gate,
                        slide_id=slide_id,
                        severity=Severity.P0,
                        issue="Slide thiếu assertion_title hoàn toàn",
                        rationale="Mọi slide bắt buộc phải có tiêu đề khẳng định để người xem nắm bắt thông điệp cốt lõi trong 3 giây đầu.",
                        suggestion="Bổ sung assertion_title theo cấu trúc khẳng định.",
                        evidence="assertion_title is empty"
                    )
                )

            if not claim and s.get("archetype") not in ["title_hero", "quote_callout"]:
                findings.append(
                    AgentFinding(
                        agent=self.name,
                        gate=self.gate,
                        slide_id=slide_id,
                        severity=Severity.P2,
                        issue="Slide thiếu primary_claim (luận điểm bổ trợ)",
                        rationale="Primary claim đóng vai trò cầu nối giải thích cho assertion title trước khi đi vào các atom chi tiết.",
                        suggestion="Bổ sung primary_claim 1 câu súc tích.",
                        evidence="primary_claim is empty"
                    )
                )

        return findings

    def auto_remediate(self, target: Any, findings: List[AgentFinding], context: Optional[Dict[str, Any]] = None) -> Any:
        remediated = copy.deepcopy(target)
        slides = self._get_slides(remediated)

        for idx, s in enumerate(slides):
            title = (s.get("assertion_title") or "").strip()
            claim = (s.get("primary_claim") or "").strip()
            atoms = s.get("atoms", [])

            # 1. Transform bare topic label into active sentence headline
            if not title or len(title.split()) <= 3:
                first_atom_title = atoms[0].get("title", "") if (atoms and isinstance(atoms[0], dict)) else ""
                section = s.get("section", "Nội dung")
                if claim:
                    s["assertion_title"] = claim
                elif first_atom_title:
                    s["assertion_title"] = f"Chiến lược {section}: Tập trung {first_atom_title.lower()}"
                else:
                    s["assertion_title"] = f"Phân tích chuyên sâu và định hướng phát triển {section.lower()}"

            # 2. Fill missing primary claim
            if not s.get("primary_claim") and s.get("archetype") not in ["title_hero", "quote_callout"]:
                if atoms and isinstance(atoms[0], dict) and atoms[0].get("text"):
                    s["primary_claim"] = atoms[0].get("text")[:100]
                else:
                    s["primary_claim"] = "Tập trung giải quyết các thách thức then chốt nhằm tối ưu hóa kết quả thực thi."

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            return remediated
        return slides

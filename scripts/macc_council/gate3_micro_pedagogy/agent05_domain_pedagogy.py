"""
scripts/macc_council/gate3_micro_pedagogy/agent05_domain_pedagogy.py
Agent 5: DomainPedagogyScholar (Domain Pedagogy & Scientific Factuality).
Audits domain accuracy, concept rigor, and professional technical jargon definitions.
"""

from __future__ import annotations

import copy
import re
from typing import Any, Dict, List, Optional
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, Severity


class DomainPedagogyScholar(BaseCouncilAgent):
    """
    Agent 05: Domain Pedagogy Scholar.
    Ensures pedagogical clarity, scientific/economic rigor, and domain-appropriate terminology.
    Prevents false technical equivalences and misattributed domain concepts.
    """

    DOMAIN_CONFUSIONS = [
        # Concept pairs that are frequently confused
        (
            re.compile(r"\b(gdp\s+bình\s+quân\s+đầu\s+người)\s*[:=–-]?\s*(\d+(?:[.,]\d+)?\s*tỷ\s*usd)", re.IGNORECASE),
            "GDP bình quân đầu người không thể tính bằng đơn vị hàng tỷ USD (thường là USD/người/năm, ví dụ 4.500 USD).",
            "USD/người"
        ),
        (
            re.compile(r"\b(tỷ\s+suất\s+sinh\s+thay\s+thế)\s*[:=–-]?\s*(\d+[.,]\d+|\d+)\s*%", re.IGNORECASE),
            "Tỷ suất sinh thay thế (TFR) đo bằng số con/phụ nữ (chuẩn 2,1 con/phụ nữ), không đo bằng phần trăm (%).",
            "con/phụ nữ"
        ),
        (
            re.compile(r"\b(tuổi\s+thọ\s+trung\s+bình)\s*[:=–-]?\s*(\d+(?:[.,]\d+)?)\s*%", re.IGNORECASE),
            "Tuổi thọ trung bình đo bằng số năm (tuổi), không đo bằng phần trăm (%).",
            "tuổi"
        )
    ]

    def __init__(self):
        super().__init__(name="DomainPedagogyScholar", gate="Gate 3: Micro-Pedagogy & Scientific Precision")

    def _get_slides(self, target: Any) -> List[Dict[str, Any]]:
        if isinstance(target, list):
            return target
        if isinstance(target, dict):
            return target.get("slides", [target])
        return []

    def audit(self, target: Any, context: Optional[Dict[str, Any]] = None) -> List[AgentFinding]:
        findings: List[AgentFinding] = []
        slides = self._get_slides(target)

        for s in slides:
            slide_id = s.get("slide_id", "unknown_slide")
            slide_text = self.extract_slide_text(s)

            for pattern, reason, correct_unit in self.DOMAIN_CONFUSIONS:
                match = pattern.search(slide_text)
                if match:
                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=slide_id,
                            severity=Severity.P1,
                            issue=f"Sai lệch khái niệm / đơn vị chuyên ngành: '{match.group(1)}'",
                            rationale=reason,
                            suggestion=f"Hiệu chỉnh đơn vị đo lường của '{match.group(1)}' sang '{correct_unit}'.",
                            evidence=match.group(0),
                            original_value=match.group(0),
                            suggested_value=match.group(1) + f": chuẩn ({correct_unit})"
                        )
                    )

        return findings

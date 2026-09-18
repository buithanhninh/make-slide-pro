"""
scripts/macc_council/gate3_micro_pedagogy/agent10_master_rewriter.py
Agent 10: MasterPedagogicalRewriter (Dialectical Synthesizer & Master Rewriter).
Orchestrates pedagogical remediation, turns passive topic labels into dynamic sentence headlines,
enforces sharp, executive business prose, and synchronizes cross-schema titles and claims.
Hardened with schema-agnostic extraction, typography hygiene, and self-healing synthesis.
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

    EXEMPT_ARCHETYPES = {"title_hero", "quote_callout", "cover", "hero_cover", "section_divider"}

    def __init__(self):
        super().__init__(name="MasterPedagogicalRewriter", gate="Gate 3: Micro-Pedagogy & Scientific Precision")

    def _get_slides(self, target: Any) -> List[Dict[str, Any]]:
        if isinstance(target, list):
            return target
        if isinstance(target, dict):
            return target.get("slides", [target])
        return []

    def _get_title(self, s: Dict[str, Any]) -> str:
        return (s.get("assertion_title") or s.get("title") or s.get("headline") or "").strip()

    def _get_claim(self, s: Dict[str, Any]) -> str:
        return (s.get("primary_claim") or s.get("subtitle") or "").strip()

    def audit(self, target: Any, context: Optional[Dict[str, Any]] = None) -> List[AgentFinding]:
        """
        Master rewriter checks overall pedagogical readiness:
        Verifies that every slide possesses a well-formed assertion title, typography hygiene,
        and primary claim bridge.
        """
        findings: List[AgentFinding] = []
        slides = self._get_slides(target)

        for idx, s in enumerate(slides):
            slide_id = s.get("slide_id", f"slide_{idx+1}")
            archetype = s.get("archetype", "")
            title = self._get_title(s)
            claim = self._get_claim(s)

            # 1. Title Presence (P0)
            if not title:
                findings.append(
                    AgentFinding(
                        agent=self.name,
                        gate=self.gate,
                        slide_id=slide_id,
                        severity=Severity.P0,
                        issue="Slide thiếu tiêu đề (assertion_title / title) hoàn toàn",
                        rationale="Mọi slide bắt buộc phải có tiêu đề khẳng định để người xem nắm bắt thông điệp cốt lõi trong 3 giây đầu.",
                        suggestion="Bổ sung assertion_title theo cấu trúc khẳng định có thông điệp hành động.",
                        evidence="title / assertion_title is empty"
                    )
                )
            else:
                # 2. Title Typography Hygiene (P2): No trailing period in titles
                if title.endswith("."):
                    clean_title = re.sub(r"\.+$", "", title).strip()
                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=slide_id,
                            severity=Severity.P2,
                            issue=f"Tiêu đề slide kết thúc bằng dấu chấm không đúng quy chuẩn trình chiếu: '{title}'",
                            rationale="Quy chuẩn thiết kế bài thuyết trình chuyên nghiệp quy định tiêu đề không bao giờ đặt dấu chấm ở cuối.",
                            suggestion=f"Loại bỏ dấu chấm cuối tiêu đề: '{clean_title}'.",
                            evidence=f"Title: '{title}'",
                            original_value=title,
                            suggested_value=clean_title
                        )
                    )

            # 3. Primary Claim Bridge (P2)
            if not claim and archetype not in self.EXEMPT_ARCHETYPES:
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
            archetype = s.get("archetype", "")
            title = self._get_title(s)
            claim = self._get_claim(s)

            # Get primary items
            items = s.get("atoms") or s.get("cards") or s.get("content_items") or []

            # 1. Synthesize title if missing or very short
            if not title or len(title.split()) <= 3:
                section = s.get("section", "Nội dung")
                first_item_title = ""
                if items and isinstance(items[0], dict):
                    first_item_title = items[0].get("title") or items[0].get("headline") or ""

                if claim:
                    title = claim
                elif first_item_title:
                    title = f"Chiến lược {section}: Tập trung {first_item_title.lower()}"
                else:
                    title = f"Phân tích chuyên sâu và định hướng phát triển {section.lower()}"

            # 2. Clean trailing period from title
            title = re.sub(r"\.+$", "", title).strip()

            # Synchronize both title fields for complete cross-schema compatibility
            s["assertion_title"] = title
            s["title"] = title

            # 3. Synthesize primary claim if missing
            if not claim and archetype not in self.EXEMPT_ARCHETYPES:
                if items and isinstance(items[0], dict):
                    first_text = items[0].get("text") or items[0].get("body") or items[0].get("description") or ""
                    if first_text:
                        s["primary_claim"] = first_text[:120].strip()
                        if not s["primary_claim"].endswith("."):
                            s["primary_claim"] += "."
                    else:
                        s["primary_claim"] = "Tập trung giải quyết các thách thức then chốt nhằm tối ưu hóa kết quả thực thi."
                else:
                    s["primary_claim"] = "Tập trung giải quyết các thách thức then chốt nhằm tối ưu hóa kết quả thực thi."

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            return remediated
        return slides

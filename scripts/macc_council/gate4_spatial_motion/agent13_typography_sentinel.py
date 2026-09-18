"""
scripts/macc_council/gate4_spatial_motion/agent13_typography_sentinel.py
Agent 13: TypographyWidowOrphanSentinel (Vietnamese Orphan Word & Typography Sentinel).
Detects and eliminates single-syllable orphan words at line ends by binding them
with non-breaking spaces (\\u00A0 / &nbsp;).
Hardened with comprehensive orphan catalogs, punctuation preservation, and schema-agnostic traversal.
"""

from __future__ import annotations

import copy
import re
from typing import Any, Dict, List, Optional
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, Severity


class TypographyWidowOrphanSentinel(BaseCouncilAgent):
    """
    Agent 13: Typography Widow & Orphan Sentinel.
    Eliminates the single-syllable Vietnamese orphan word defect (từ mồ côi rớt dòng).
    Automatically binds terminal single words/numbers/units to the preceding word using non-breaking spaces.
    """

    ORPHAN_WORDS = {
        # Prepositions and conjunctions
        "và", "là", "trong", "của", "đã", "sẽ", "cho", "với", "từ", "ở", "tại",
        "theo", "đến", "các", "những", "hoặc", "để", "do", "bởi", "vào", "ra", "lên", "xuống",
        # Units and time indicators
        "năm", "tháng", "quý", "tỷ", "tỉ", "triệu", "nghìn", "đồng", "usd", "vnđ",
        # Verb fragments
        "tăng", "giảm", "đạt"
    }

    def __init__(self):
        super().__init__(name="TypographyWidowOrphanSentinel", gate="Gate 4: Spatial Geometry, Typography & Motion")

    def _get_slides(self, target: Any) -> List[Dict[str, Any]]:
        if isinstance(target, list):
            return target
        if isinstance(target, dict):
            return target.get("slides", [target])
        return []

    def _check_string_for_orphan(self, text: str) -> Optional[str]:
        if not text or not isinstance(text, str):
            return None
        # If the last word is already bound with a non-breaking space, it is not an orphan!
        if re.search(r"\u00A0\S+[.,;!?:]*$", text):
            return None
        # Clean trailing punctuation for checking
        cleaned = re.sub(r"[.,;!?:]+$", "", text).strip()
        # Split strictly by ASCII space so \u00A0-bound tokens stay together
        words = cleaned.split(" ")
        if len(words) >= 2:
            last_word = words[-1].lower()
            # If last word is in ORPHAN_WORDS or is a short percentage/number
            if last_word in self.ORPHAN_WORDS or re.match(r"^\d+(?:[.,]\d+)?%?$", last_word):
                return words[-1]
        return None

    def _bind_non_breaking_space(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return text
        if re.search(r"\u00A0\S+[.,;!?:]*$", text):
            return text
        # Replace the last regular ASCII space before the last word with non-breaking space \u00A0
        match = re.search(r"( +)(\S+)([.,;!?:]*)$", text)
        if match:
            pre_space, last_word, punct = match.groups()
            return text[:match.start(1)] + "\u00A0" + last_word + punct
        return text

    def audit(self, target: Any, context: Optional[Dict[str, Any]] = None) -> List[AgentFinding]:
        findings: List[AgentFinding] = []
        slides = self._get_slides(target)

        for s in slides:
            slide_id = s.get("slide_id", "unknown_slide")

            # Check title fields (assertion_title, title, headline)
            for tk in ["assertion_title", "title", "headline"]:
                if tk in s and isinstance(s[tk], str) and s[tk]:
                    title_val = s[tk]
                    orphan = self._check_string_for_orphan(title_val)
                    if orphan:
                        findings.append(
                            AgentFinding(
                                agent=self.name,
                                gate=self.gate,
                                slide_id=slide_id,
                                severity=Severity.P2,
                                issue=f"Từ mồ côi rớt dòng cuối tiêu đề ({tk}): '{orphan}'",
                                rationale="Từ đơn hoặc số liệu đứng lẻ loi ở cuối câu tiêu đề gây ngắt dòng mất thẩm mỹ khi trình chiếu ở các độ phân giải khác nhau.",
                                suggestion="Sử dụng khoảng trắng không ngắt dòng (non-breaking space \\u00A0) để liên kết từ này với từ liền trước.",
                                evidence=f"{tk} ends with: '{orphan}'",
                                original_value=title_val,
                                suggested_value=self._bind_non_breaking_space(title_val)
                            )
                        )
                        break

            # Check atoms
            for aidx, atom in enumerate(s.get("atoms", [])):
                if isinstance(atom, dict):
                    for ak in ["text", "body", "title"]:
                        if ak in atom and isinstance(atom[ak], str) and atom[ak]:
                            orphan = self._check_string_for_orphan(atom[ak])
                            if orphan:
                                findings.append(
                                    AgentFinding(
                                        agent=self.name,
                                        gate=self.gate,
                                        slide_id=slide_id,
                                        severity=Severity.P2,
                                        issue=f"Từ mồ côi rớt dòng tại atom {aidx+1} ({ak}): '{orphan}'",
                                        rationale="Từ lẻ ở cuối thẻ nội dung làm giảm tính chuyên nghiệp của bản thiết kế.",
                                        suggestion="Gắn non-breaking space \\u00A0 vào từ cuối cùng.",
                                        evidence=f"Atom {aidx+1} ({ak}) ends with: '{orphan}'",
                                        original_value=atom[ak],
                                        suggested_value=self._bind_non_breaking_space(atom[ak])
                                    )
                                )

            # Check generic cards / content_items / boxes
            for cidx, item in enumerate(s.get("cards", []) + s.get("content_items", []) + s.get("boxes", [])):
                if isinstance(item, dict):
                    for ik in ["description", "body", "text", "headline", "title"]:
                        if ik in item and isinstance(item[ik], str) and item[ik]:
                            orphan = self._check_string_for_orphan(item[ik])
                            if orphan:
                                findings.append(
                                    AgentFinding(
                                        agent=self.name,
                                        gate=self.gate,
                                        slide_id=slide_id,
                                        severity=Severity.P2,
                                        issue=f"Từ mồ côi rớt dòng tại thẻ nội dung {cidx+1} ({ik}): '{orphan}'",
                                        rationale="Từ lẻ ở cuối thẻ nội dung làm giảm tính chuyên nghiệp của bản thiết kế.",
                                        suggestion="Gắn non-breaking space \\u00A0 vào từ cuối cùng.",
                                        evidence=f"Item {cidx+1} ({ik}) ends with: '{orphan}'",
                                        original_value=item[ik],
                                        suggested_value=self._bind_non_breaking_space(item[ik])
                                    )
                                )

        return findings

    def auto_remediate(self, target: Any, findings: List[AgentFinding], context: Optional[Dict[str, Any]] = None) -> Any:
        remediated = copy.deepcopy(target)
        slides = self._get_slides(remediated)

        for s in slides:
            for tk in ["assertion_title", "title", "headline", "primary_claim"]:
                if tk in s and isinstance(s[tk], str):
                    if self._check_string_for_orphan(s[tk]):
                        s[tk] = self._bind_non_breaking_space(s[tk])

            for atom in s.get("atoms", []):
                if isinstance(atom, dict):
                    for ak in ["text", "body", "title"]:
                        if ak in atom and isinstance(atom[ak], str):
                            if self._check_string_for_orphan(atom[ak]):
                                atom[ak] = self._bind_non_breaking_space(atom[ak])

            for item in s.get("cards", []) + s.get("content_items", []) + s.get("boxes", []):
                if isinstance(item, dict):
                    for ik in ["description", "body", "text", "headline", "title"]:
                        if ik in item and isinstance(item[ik], str):
                            if self._check_string_for_orphan(item[ik]):
                                item[ik] = self._bind_non_breaking_space(item[ik])

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            return remediated
        return slides

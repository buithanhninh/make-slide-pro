"""
scripts/macc_council/gate3_micro_pedagogy/agent09_adversarial_critic.py
Agent 9: AdversarialContentCritic (Red Teaming & Unsubstantiated Superlative Critic).
Identifies hyperbolic superlatives, unverified claims, and subjective marketing bluster.
Hardened with multi-lingual red-teaming catalogs, empirical citation verification, and defensible corporate remediation.
"""

from __future__ import annotations

import copy
import re
from typing import Any, Dict, List, Optional, Tuple
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, Severity


class AdversarialContentCritic(BaseCouncilAgent):
    """
    Agent 09: Adversarial Content Critic.
    Acts as a ruthless red-teamer challenging unsubstantiated marketing hype,
    absolute guarantees, and claims lacking empirical benchmark backing across Vietnamese and English.
    """

    UNSUBSTANTIATED_SUPERLATIVES = [
        # --- Vietnamese Superlatives ---
        (
            re.compile(r"\b(tốt\s+nhất\s+thị\s+trường|số\s+1\s+thị\s+trường|số\s+một\s+thế\s+giới|hàng\s+đầu\s+thế\s+giới)\b", re.IGNORECASE),
            "Khẳng định 'số 1 / tốt nhất' thiếu kiểm chứng độc lập",
            "vị thế tiên phong"
        ),
        (
            re.compile(r"\b(tuyệt\s+đối\s+an\s+toàn|bảo\s+mật\s+tuyệt\s+đối|chính\s+xác\s+tuyệt\s+đối|chính\s+xác\s+100%|ngăn\s+chặn\s+100%)\b", re.IGNORECASE),
            "Tuyên bố 'tuyệt đối / 100%' phản khoa học / rủi ro pháp lý",
            "bảo mật đa lớp tiêu chuẩn cao"
        ),
        (
            re.compile(r"\b(100%\s+khách\s+hàng\s+hài\s+lòng|100%\s+người\s+dùng\s+tin\s+tưởng|100%\s+đối\s+tác\s+tin\s+cậy)\b", re.IGNORECASE),
            "Chỉ số hoàn hảo 100% phi thực tế",
            "đại đa số khách hàng đánh giá cao"
        ),
        (
            re.compile(r"\b(dẫn\s+đầu\s+tuyệt\s+đối|vô\s+đối|không\s+thể\s+bị\s+đánh\s+bại)\b", re.IGNORECASE),
            "Từ ngữ tự phụ thiếu bằng chứng cạnh tranh",
            "giữ vị thế dẫn đầu"
        ),

        # --- English Superlatives ---
        (
            re.compile(r"\b(100%\s+secure|absolute\s+security|zero\s+risk|100%\s+accurate)\b", re.IGNORECASE),
            "English absolute guarantee (100% secure / zero risk)",
            "enterprise-grade secure"
        ),
        (
            re.compile(r"\b(undisputed(?:\s+market)?\s+leader|#1\s+in\s+the\s+market|number\s+one\s+in\s+the\s+world)\b", re.IGNORECASE),
            "English unverified market dominance claim",
            "leading industry provider"
        ),
        (
            re.compile(r"\b(100%\s+customer\s+satisfaction|100%\s+client\s+satisfaction)\b", re.IGNORECASE),
            "English unrealistic 100% satisfaction claim",
            "high customer satisfaction"
        )
    ]

    CITATION_KEYWORDS = [
        "theo", "nguồn:", "source:", "gartner", "idc", "forrester", "gso",
        "tổng cục thống kê", "ngân hàng thế giới", "world bank", "báo cáo",
        "magic quadrant", "bloomberg", "reuters", "statista", "iso", "soc 2"
    ]

    def __init__(self):
        super().__init__(name="AdversarialContentCritic", gate="Gate 3: Micro-Pedagogy & Scientific Precision")

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
            has_citation = any(k in slide_text.lower() for k in self.CITATION_KEYWORDS)

            for pattern, issue_label, replacement in self.UNSUBSTANTIATED_SUPERLATIVES:
                for match in pattern.finditer(slide_text):
                    phrase = match.group(0)
                    if not has_citation:
                        findings.append(
                            AgentFinding(
                                agent=self.name,
                                gate=self.gate,
                                slide_id=slide_id,
                                severity=Severity.P1,
                                issue=f"Tuyên bố chủ quan thiếu kiểm chứng: '{phrase}' ({issue_label})",
                                rationale="Các khẳng định mang tính tuyệt đối hoặc khẳng định vị thế số 1 mà không trích dẫn nguồn uy tín sẽ làm suy giảm độ tin cậy của bài thuyết trình trước hội đồng/khách hàng.",
                                suggestion=f"Thay thế '{phrase}' bằng tuyên bố khách quan có thể chứng minh được ('{replacement}') hoặc bổ sung nguồn trích dẫn dữ liệu.",
                                evidence=phrase,
                                original_value=phrase,
                                suggested_value=replacement
                            )
                        )

        return findings

    def auto_remediate(self, target: Any, findings: List[AgentFinding], context: Optional[Dict[str, Any]] = None) -> Any:
        remediated = copy.deepcopy(target)
        slides = self._get_slides(remediated)

        replacements = [
            (re.compile(r"\btốt\s+nhất\s+thị\s+trường\b", re.IGNORECASE), "thuộc nhóm tối ưu trên thị trường"),
            (re.compile(r"\bsố\s+1\s+thị\s+trường|số\s+một\s+thế\s+giới|hàng\s+đầu\s+thế\s+giới\b", re.IGNORECASE), "vị thế tiên phong"),
            (re.compile(r"\btuyệt\s+đối\s+an\s+toàn|bảo\s+mật\s+tuyệt\s+đối\b", re.IGNORECASE), "bảo mật đa lớp tiêu chuẩn cao"),
            (re.compile(r"\bchính\s+xác\s+tuyệt\s+đối|chính\s+xác\s+100%\b", re.IGNORECASE), "độ chính xác cao"),
            (re.compile(r"\bngăn\s+chặn\s+100%\b", re.IGNORECASE), "ngăn chặn tối đa"),
            (re.compile(r"\b100%\s+khách\s+hàng\s+hài\s+lòng\b", re.IGNORECASE), "đại đa số khách hàng đánh giá cao"),
            (re.compile(r"\bdẫn\s+đầu\s+tuyệt\s+đối\b", re.IGNORECASE), "giữ vị thế dẫn đầu"),
            (re.compile(r"\b100%\s+secure\b", re.IGNORECASE), "enterprise-grade secure"),
            (re.compile(r"\bzero\s+risk\b", re.IGNORECASE), "minimized operational risk"),
            (re.compile(r"\bundisputed(?:\s+market)?\s+leader\b", re.IGNORECASE), "leading industry provider"),
            (re.compile(r"\b100%\s+customer\s+satisfaction\b", re.IGNORECASE), "high customer satisfaction")
        ]

        for s in slides:
            def _temper_text(text: str) -> str:
                if not isinstance(text, str):
                    return text
                clean = text
                for pat, rep in replacements:
                    clean = pat.sub(rep, clean)
                return clean

            for k in ["assertion_title", "title", "headline", "primary_claim", "subtitle", "speaker_notes"]:
                if k in s:
                    s[k] = _temper_text(s[k])

            for atom in s.get("atoms", []):
                if isinstance(atom, dict):
                    for ak in ["title", "text", "body", "mechanism", "kicker"]:
                        if ak in atom:
                            atom[ak] = _temper_text(atom[ak])

            for item in s.get("content_items", []) + s.get("cards", []) + s.get("boxes", []):
                if isinstance(item, dict):
                    for ik in ["title", "text", "body", "headline", "description"]:
                        if ik in item:
                            item[ik] = _temper_text(item[ik])

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            return remediated
        return slides

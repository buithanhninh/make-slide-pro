"""
scripts/macc_council/gate3_micro_pedagogy/agent09_adversarial_critic.py
Agent 9: AdversarialContentCritic (Red Teaming & Unsubstantiated Superlative Critic).
Identifies hyperbolic superlatives, unverified claims, and subjective marketing bluster.
"""

from __future__ import annotations

import copy
import re
from typing import Any, Dict, List, Optional
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, Severity


class AdversarialContentCritic(BaseCouncilAgent):
    """
    Agent 09: Adversarial Content Critic.
    Acts as a ruthless red-teamer challenging unsubstantiated marketing hype,
    absolute guarantees, and claims lacking empirical benchmark backing.
    """

    UNSUBSTANTIATED_SUPERLATIVES = [
        (re.compile(r"\b(tốt\s+nhất\s+thị\s+trường|số\s+1\s+thị\s+trường|số\s+một\s+thế\s+giới)\b", re.IGNORECASE), "Khẳng định 'số 1 / tốt nhất' thiếu kiểm chứng độc lập"),
        (re.compile(r"\b(tuyệt\s+đối\s+an\s+toàn|bảo\s+mật\s+tuyệt\s+đối|chính\s+xác\s+tuyệt\s+đối)\b", re.IGNORECASE), "Tuyên bố 'tuyệt đối' phản khoa học / rủi ro pháp lý"),
        (re.compile(r"\b(100%\s+khách\s+hàng\s+hài\s+lòng|100%\s+người\s+dùng\s+tin\s+tưởng)\b", re.IGNORECASE), "Chỉ số hoàn hảo 100% phi thực tế"),
        (re.compile(r"\b(dẫn\s+đầu\s+tuyệt\s+đối|vô\s+đối|không\s+thể\s+bị\s+đánh\s+bại)\b", re.IGNORECASE), "Từ ngữ tự phụ thiếu bằng chứng cạnh tranh")
    ]

    CITATION_KEYWORDS = ["theo", "nguồn:", "source:", "gartner", "idc", "forrester", "gso", "ngân hàng thế giới", "world bank", "báo cáo"]

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

            for pattern, issue_label in self.UNSUBSTANTIATED_SUPERLATIVES:
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
                                suggestion=f"Thay thế '{phrase}' bằng tuyên bố khách quan có thể chứng minh được hoặc bổ sung nguồn trích dẫn dữ liệu.",
                                evidence=phrase,
                                original_value=phrase
                            )
                        )

        return findings

    def auto_remediate(self, target: Any, findings: List[AgentFinding], context: Optional[Dict[str, Any]] = None) -> Any:
        remediated = copy.deepcopy(target)
        slides = self._get_slides(remediated)

        replacements = [
            (re.compile(r"\btốt\s+nhất\s+thị\s+trường\b", re.IGNORECASE), "thuộc nhóm tối ưu trên thị trường"),
            (re.compile(r"\bsố\s+1\s+thị\s+trường|số\s+một\s+thế\s+giới\b", re.IGNORECASE), "vị thế tiên phong"),
            (re.compile(r"\btuyệt\s+đối\s+an\s+toàn|bảo\s+mật\s+tuyệt\s+đối\b", re.IGNORECASE), "bảo mật đa lớp tiêu chuẩn cao"),
            (re.compile(r"\bchính\s+xác\s+tuyệt\s+đối\b", re.IGNORECASE), "độ chính xác cao"),
            (re.compile(r"\b100%\s+khách\s+hàng\s+hài\s+lòng\b", re.IGNORECASE), "đại đa số khách hàng đánh giá cao"),
            (re.compile(r"\bdẫn\s+đầu\s+tuyệt\s+đối\b", re.IGNORECASE), "giữ vị thế dẫn đầu")
        ]

        for s in slides:
            for k in ["assertion_title", "primary_claim", "speaker_notes"]:
                if k in s and isinstance(s[k], str):
                    for pat, rep in replacements:
                        s[k] = pat.sub(rep, s[k]).strip()
            for atom in s.get("atoms", []):
                if isinstance(atom, dict):
                    for ak in ["title", "text", "mechanism", "kicker"]:
                        if ak in atom and isinstance(atom[ak], str):
                            for pat, rep in replacements:
                                atom[ak] = pat.sub(rep, atom[ak]).strip()

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            return remediated
        return slides

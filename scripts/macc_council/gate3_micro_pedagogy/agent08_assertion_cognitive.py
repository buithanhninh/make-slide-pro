"""
scripts/macc_council/gate3_micro_pedagogy/agent08_assertion_cognitive.py
Agent 8: AssertionCognitiveArbiter (Sentence Headline Rule & Cognitive Load Arbiter).
Enforces the Assertion-Evidence Framework: complete sentence headline claims,
strict card count limits (<= 4 atoms), and concise bullet density.
"""

from __future__ import annotations

import copy
import re
from typing import Any, Dict, List, Optional
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, Severity


class AssertionCognitiveArbiter(BaseCouncilAgent):
    """
    Agent 08: Assertion & Cognitive Load Arbiter.
    Strictly enforces:
    1. Sentence Headline Rule: Titles must be complete active claims, not lazy topic labels.
    2. Cognitive Limits: Max 4 atoms/cards per slide.
    3. Density Controls: Max 40 words per atom to prevent wall-of-text fatigue.
    """

    LAZY_TOPIC_LABELS = [
        "tổng quan", "giới thiệu", "thực trạng", "báo cáo", "các giải pháp",
        "giải pháp", "kết quả", "biểu đồ", "phân tích", "chi phí", "doanh thu",
        "thị trường", "overview", "introduction", "market analysis", "solutions"
    ]

    def __init__(self):
        super().__init__(name="AssertionCognitiveArbiter", gate="Gate 3: Micro-Pedagogy & Scientific Precision")

    def _get_slides(self, target: Any) -> List[Dict[str, Any]]:
        if isinstance(target, list):
            return target
        if isinstance(target, dict):
            return target.get("slides", [target])
        return []

    def audit(self, target: Any, context: Optional[Dict[str, Any]] = None) -> List[AgentFinding]:
        findings: List[AgentFinding] = []
        slides = self._get_slides(target)

        for idx, s in enumerate(slides):
            slide_id = s.get("slide_id", f"slide_{idx+1}")
            title = (s.get("assertion_title") or "").strip()
            archetype = s.get("archetype", "")

            # Ignore slide 1 if it is title_hero
            if idx == 0 and archetype == "title_hero":
                pass
            else:
                # 1. Sentence Headline Rule Verification
                clean_title = title.lower().strip()
                # If title is very short (<= 3 words) or matches generic topic labels exactly
                words = clean_title.split()
                if len(words) <= 3 or clean_title in self.LAZY_TOPIC_LABELS:
                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=slide_id,
                            severity=Severity.P1,
                            issue=f"Tiêu đề dạng nhãn chủ đề thụ động (Lazy Topic Label): '{title}'",
                            rationale="Quy tắc Sentence Headline (Assertion-Evidence Model) yêu cầu tiêu đề slide phải là một câu khẳng định có chủ ngữ - vị ngữ - thông điệp cốt lõi, thay vì chỉ là tên chủ đề chung chung.",
                            suggestion="Viết lại tiêu đề thành câu hoàn chỉnh nêu rõ kết quả, xu hướng hoặc hành động (ví dụ: thay 'Giải pháp' bằng 'Triển khai 3 nhóm giải pháp trọng tâm nhằm nâng cao hiệu suất').",
                            evidence=f"Title: '{title}'",
                            original_value=title
                        )
                    )

            # 2. Cognitive Load: Max 4 Atoms
            atoms = s.get("atoms", [])
            if len(atoms) > 4:
                findings.append(
                    AgentFinding(
                        agent=self.name,
                        gate=self.gate,
                        slide_id=slide_id,
                        severity=Severity.P1,
                        issue=f"Quá tải nhận thức (Cognitive Overload): Slide có {len(atoms)} thẻ nội dung (Vượt mức trần 4 thẻ)",
                        rationale="Theo tâm lý học nhận thức, khán giả chỉ có thể ghi nhớ tối đa 4 cụm thông tin trên một slide thuyết trình. Việc nhồi nhét quá nhiều thẻ làm loãng thông điệp.",
                        suggestion="Gom cụm các điểm tương đồng hoặc tách slide thành 2 slide độc lập theo mạch logic.",
                        evidence=f"Atoms count: {len(atoms)}"
                    )
                )

            # 3. Density Control: Max 40 words per atom
            for aidx, atom in enumerate(atoms):
                if isinstance(atom, dict):
                    text = atom.get("text", "")
                    word_count = len(text.split())
                    if word_count > 40:
                        findings.append(
                            AgentFinding(
                                agent=self.name,
                                gate=self.gate,
                                slide_id=slide_id,
                                severity=Severity.P2,
                                issue=f"Thẻ atom {aidx+1} quá dài ({word_count} từ > 40 từ)",
                                rationale="Đoạn văn bản quá dài biến slide thành tài liệu đọc (docupresentation), làm phân tán sự lắng nghe của người xem.",
                                suggestion="Rút gọn văn bản, đưa dữ liệu phụ vào speaker_notes.",
                                evidence=f"Atom {aidx+1} word count: {word_count}"
                            )
                        )

        return findings

    def auto_remediate(self, target: Any, findings: List[AgentFinding], context: Optional[Dict[str, Any]] = None) -> Any:
        remediated = copy.deepcopy(target)
        slides = self._get_slides(remediated)

        for s in slides:
            # If atoms > 4, keep top 4 and move rest to speaker_notes
            atoms = s.get("atoms", [])
            if len(atoms) > 4:
                overflow_atoms = atoms[4:]
                s["atoms"] = atoms[:4]
                overflow_text = " | ".join(f"{a.get('title', '')}: {a.get('text', '')}" for a in overflow_atoms if isinstance(a, dict))
                cur_notes = s.get("speaker_notes", "")
                s["speaker_notes"] = (cur_notes + "\n[Bổ sung thêm]: " + overflow_text).strip()

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            return remediated
        return slides

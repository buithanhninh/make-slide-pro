"""
scripts/macc_council/gate2_macro_narrative/agent03_narrative_arc.py
Agent 3: NarrativeArcDirector (Macro-Narrative Arc & Storyline Flow).
Ensures presentations adhere to Minto Pyramid structure, clear situation-complication-resolution flow,
and non-abrupt endings with robust Call-to-Actions (CTA).
"""

from __future__ import annotations

import copy
import re
from typing import Any, Dict, List, Optional
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, Severity


class NarrativeArcDirector(BaseCouncilAgent):
    """
    Agent 03: Narrative Arc Director.
    Validates presentation narrative spine, Minto Pyramid hierarchy,
    logical section progression, and Call-To-Action (CTA) closure.
    """

    CONCLUSION_KEYWORDS = [
        "kết luận", "tổng kết", "khuyến nghị", "hành động", "lộ trình",
        "kế hoạch", "triển khai", "next step", "call to action", "liên hệ",
        "hướng phát triển", "bước tiếp theo", "tóm tắt", "kiến nghị", "summary"
    ]

    AGENDA_KEYWORDS = [
        "mục lục", "nội dung", "chương trình", "tổng quan", "agenda",
        "khung nội dung", "outline", "các phần chính", "cấu trúc bài"
    ]

    def __init__(self):
        super().__init__(name="NarrativeArcDirector", gate="Gate 2: Macro-Narrative Arc & Consistency")

    def _get_slides(self, target: Any) -> List[Dict[str, Any]]:
        if isinstance(target, list):
            return target
        if isinstance(target, dict):
            return target.get("slides", [target])
        return []

    def audit(self, target: Any, context: Optional[Dict[str, Any]] = None) -> List[AgentFinding]:
        findings: List[AgentFinding] = []
        slides = self._get_slides(target)

        if not slides:
            return findings

        total_slides = len(slides)

        # 1. Deck Length & Opening Verification (Title / Thesis / Agenda)
        if total_slides >= 1:
            first_slide = slides[0]
            first_text = self.extract_slide_text(first_slide).lower()
            first_archetype = first_slide.get("archetype", "")

            # If the first slide is an analytical data table or complex comparison without title context
            if first_archetype in ["table_dense", "data_matrix", "quadrant_matrix"] and not any(
                k in first_text for k in ["báo cáo", "tổng quan", "nghiên cứu", "chiến lược", "kế hoạch"]
            ):
                findings.append(
                    AgentFinding(
                        agent=self.name,
                        gate=self.gate,
                        slide_id=first_slide.get("slide_id", "slide_1"),
                        severity=Severity.P1,
                        issue="Thiếu slide Mở đầu / Bối cảnh chuẩn Minto Pyramid",
                        rationale="Bài thuyết trình mở đầu đột ngột bằng ma trận dữ liệu phức tạp mà chưa nêu rõ luận điểm trung tâm.",
                        suggestion="Bổ sung slide Mở đầu / Bối cảnh (Title / Context / Thesis) định hướng người xem trước khi đi vào chi tiết.",
                        evidence=f"Slide 1 archetype='{first_archetype}'"
                    )
                )

        # For long decks (>= 6 slides), check if Agenda / Executive Summary exists in the first 3 slides
        if total_slides >= 6:
            has_agenda = False
            for s in slides[:3]:
                stext = self.extract_slide_text(s).lower()
                sarchetype = s.get("archetype", "")
                if sarchetype in ["agenda_list", "timeline_horizontal"] or any(k in stext for k in self.AGENDA_KEYWORDS):
                    has_agenda = True
                    break

            if not has_agenda:
                findings.append(
                    AgentFinding(
                        agent=self.name,
                        gate=self.gate,
                        slide_id="deck_macro",
                        severity=Severity.P2,
                        issue="Thiếu slide Mục lục / Lộ trình nội dung (Executive Agenda)",
                        rationale=f"Bộ slide có {total_slides} slides nhưng không có slide Mục lục / Tổng quan trong 3 slide đầu tiên.",
                        suggestion="Thêm 1 slide Agenda ở vị trí slide 2 để định hình bức tranh tổng thể cho khán giả.",
                        evidence=f"Total slides: {total_slides}, no agenda in first 3 slides."
                    )
                )

        # 2. Conclusion & Call to Action (CTA) Verification
        if total_slides >= 3:
            last_slide = slides[-1]
            last_text = self.extract_slide_text(last_slide).lower()
            last_archetype = last_slide.get("archetype", "")

            is_conclusion = (
                last_archetype in ["conclusion_cta", "quote_callout", "timeline_roadmap"]
                or any(k in last_text for k in self.CONCLUSION_KEYWORDS)
            )

            if not is_conclusion:
                findings.append(
                    AgentFinding(
                        agent=self.name,
                        gate=self.gate,
                        slide_id=last_slide.get("slide_id", f"slide_{total_slides}"),
                        severity=Severity.P1,
                        issue="Thiếu slide Kết luận / Kêu gọi hành động (Call to Action / Next Steps)",
                        rationale="Bài thuyết trình kết thúc đột ngột ở một slide phân tích/số liệu kỹ thuật mà không có thông điệp chốt hoặc bước triển khai tiếp theo.",
                        suggestion="Bổ sung slide Tổng kết & Khuyến nghị hành động (Conclusion / Action Plan) để khép lại vòng lặp nhận thức.",
                        evidence=f"Last slide title: '{last_slide.get('assertion_title', '')}'"
                    )
                )

        # 3. Section Progression & MECE Consistency (No bouncing between disjointed sections)
        sections_order: List[str] = []
        for idx, s in enumerate(slides):
            sec = (s.get("section") or "").strip()
            if sec:
                if not sections_order or sections_order[-1] != sec:
                    if sec in sections_order:
                        # Re-entering an old section that was already closed!
                        findings.append(
                            AgentFinding(
                                agent=self.name,
                                gate=self.gate,
                                slide_id=s.get("slide_id", f"slide_{idx+1}"),
                                severity=Severity.P1,
                                issue=f"Cấu trúc nội dung bị phân mảnh / nhảy cóc (non-MECE section jumping): Phần '{sec}' xuất hiện rời rạc",
                                rationale=f"Chủ đề '{sec}' đã được trình bày trước đó và đã chuyển qua chủ đề khác, nhưng lại đột ngột xuất hiện lại ở slide {idx+1}.",
                                suggestion=f"Gom nhóm toàn bộ các slide thuộc phần '{sec}' vào cùng một khối liền mạch theo nguyên lý MECE.",
                                evidence=f"Section order: {' -> '.join(sections_order + [sec])}"
                            )
                        )
                    sections_order.append(sec)

        return findings

    def auto_remediate(self, target: Any, findings: List[AgentFinding], context: Optional[Dict[str, Any]] = None) -> Any:
        """
        Auto-remediates missing conclusion by creating a structured conclusion slide if requested.
        """
        remediated = copy.deepcopy(target)
        slides = self._get_slides(remediated)

        # Check if missing conclusion finding exists
        needs_conclusion = any(f.issue.startswith("Thiếu slide Kết luận") for f in findings)
        if needs_conclusion and slides:
            # Synthesize a clean conclusion slide
            last_num = len(slides) + 1
            conclusion_slide = {
                "slide_id": f"slide_{last_num:02d}",
                "section": "Kết luận & Hành động",
                "assertion_title": "Tổng kết định hướng và các bước triển khai trọng tâm",
                "primary_claim": "Thực hiện đồng bộ các giải pháp chiến lược nhằm tối ưu hóa hiệu quả thực thi.",
                "archetype": "conclusion_cta",
                "atoms": [
                    {
                        "kicker": "BƯỚC 1",
                        "title": "Hoàn thiện thể chế & chính sách",
                        "text": "Ban hành khung hướng dẫn tiêu chuẩn và quy chuẩn vận hành đồng bộ.",
                        "tag": "Khẩn cấp"
                    },
                    {
                        "kicker": "BƯỚC 2",
                        "title": "Phát triển hạ tầng & nhân lực",
                        "text": "Đầu tư nguồn lực trọng điểm và đào tạo kỹ năng chuyên sâu.",
                        "tag": "Trung hạn"
                    },
                    {
                        "kicker": "BƯỚC 3",
                        "title": "Giám sát & Đánh giá định kỳ",
                        "text": "Ứng dụng công nghệ số đo lường hiệu quả (KPIs) liên tục theo thời gian thực.",
                        "tag": "Dài hạn"
                    }
                ],
                "speaker_notes": "Tóm tắt các phát hiện chính và khuyến nghị lộ trình 3 giai đoạn rõ ràng cho ban lãnh đạo."
            }
            slides.append(conclusion_slide)

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            return remediated
        return slides

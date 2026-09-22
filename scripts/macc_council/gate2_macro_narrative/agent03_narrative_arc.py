"""
scripts/macc_council/gate2_macro_narrative/agent03_narrative_arc.py
Agent 3: NarrativeArcDirector (Macro-Narrative Arc & Storyline Flow V8.0).
Ensures presentations adhere to Minto Pyramid structure, clear situation-complication-resolution flow,
non-abrupt endings with robust Call-to-Actions (CTA), and executive agendas for deep decks.
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
    Validates presentation narrative spine, Minto Pyramid hierarchy (SCQA),
    logical section progression, and Call-To-Action (CTA) closure.
    """

    CONCLUSION_KEYWORDS = [
        "kết luận", "tổng kết", "khuyến nghị", "hành động", "lộ trình",
        "kế hoạch", "triển khai", "next step", "call to action", "liên hệ",
        "hướng phát triển", "bước tiếp theo", "tóm tắt", "kiến nghị", "summary"
    ]

    AGENDA_KEYWORDS = [
        "mục lục", "nội dung", "chương trình", "tổng quan", "agenda",
        "khung nội dung", "outline", "các phần chính", "cấu trúc bài",
        "mục tiêu", "mục tiêu bài học", "chuẩn đầu ra", "trọng tâm bài học", "nội dung cốt lõi"
    ]

    PROBLEM_KEYWORDS = [
        "thực trạng", "bối cảnh", "thách thức", "khủng hoảng", "khó khăn",
        "vấn đề", "điểm nghẽn", "rủi ro", "hạn chế", "tồn tại", "nguyên nhân"
    ]

    SOLUTION_KEYWORDS = [
        "giải pháp", "đề xuất", "phương án", "chiến lược", "hành động",
        "triển khai", "ứng dụng", "công nghệ", "kiến trúc", "mô hình"
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

        # ----------------------------------------------------
        # 1. Deck Opening & Title Verification
        # ----------------------------------------------------
        first_slide = slides[0]
        first_text = self.extract_slide_text(first_slide).lower()
        first_archetype = first_slide.get("archetype", "")

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

        # ----------------------------------------------------
        # 2. Executive Agenda Verification for Long Decks (>= 6 slides)
        # ----------------------------------------------------
        if total_slides >= 6:
            has_agenda = False
            for s in slides[:3]:
                stext = self.extract_slide_text(s).lower()
                sarchetype = s.get("archetype") or s.get("visual_job", "")
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

        # ----------------------------------------------------
        # 3. SCQA Balance (Situation - Complication - Question - Answer)
        # ----------------------------------------------------
        if total_slides >= 4:
            has_problem_context = False
            has_solution_resolution = False

            for s in slides[1:-1]:
                stext = self.extract_slide_text(s).lower()
                s_sec = (s.get("section") or "").lower()
                full_s_context = f"{stext} {s_sec}"

                if any(p in full_s_context for p in self.PROBLEM_KEYWORDS):
                    has_problem_context = True
                if any(sol in full_s_context for sol in self.SOLUTION_KEYWORDS):
                    has_solution_resolution = True

            # If presentation describes solutions with zero problem context
            if has_solution_resolution and not has_problem_context:
                findings.append(
                    AgentFinding(
                        agent=self.name,
                        gate=self.gate,
                        slide_id=slides[1].get("slide_id", "slide_2"),
                        severity=Severity.P1,
                        issue="Thiếu bối cảnh / vấn đề cần giải quyết (Minto SCQA: Missing Problem/Context)",
                        rationale="Bài thuyết trình đi thẳng vào giải pháp kỹ thuật mà không thiết lập bối cảnh thực trạng và lý do vì sao cần hành động.",
                        suggestion="Bổ sung 1 slide Bối cảnh / Thách thức trước khi bước vào chi tiết các giải pháp.",
                        evidence="Slides 2..N-1 contain solutions but 0 problem context."
                    )
                )

            # If presentation describes only problems with zero solution
            if has_problem_context and not has_solution_resolution:
                findings.append(
                    AgentFinding(
                        agent=self.name,
                        gate=self.gate,
                        slide_id=slides[-1].get("slide_id", f"slide_{total_slides}"),
                        severity=Severity.P1,
                        issue="Thiếu giải pháp giải quyết vấn đề (Minto SCQA: Missing Resolution)",
                        rationale="Bài thuyết trình chỉ liệt kê các khó khăn/thách thức mà không đưa ra hướng giải quyết.",
                        suggestion="Bổ sung các giải pháp và đề xuất hành động cụ thể.",
                        evidence="Presentation is problem-heavy with zero resolution."
                    )
                )

        # ----------------------------------------------------
        # 4. Conclusion & Call to Action (CTA) Closure
        # ----------------------------------------------------
        if total_slides >= 2:
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

        # ----------------------------------------------------
        # 5. Section Progression & MECE Consistency
        # ----------------------------------------------------
        sections_order: List[str] = []
        for idx, s in enumerate(slides):
            sec = (s.get("section") or "").strip()
            if sec:
                if not sections_order or sections_order[-1] != sec:
                    if sec in sections_order:
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
        remediated = copy.deepcopy(target)
        slides = self._get_slides(remediated)

        # 1. Remediate missing agenda in long decks (>= 6 slides)
        needs_agenda = any("Mục lục" in f.issue or "Agenda" in f.issue for f in findings)
        if needs_agenda and len(slides) >= 6:
            # Extract unique sections for agenda atoms
            unique_sections = []
            for s in slides:
                sec = s.get("section")
                if sec and sec not in unique_sections and sec.lower() not in ["mở đầu", "giới thiệu"]:
                    unique_sections.append(sec)
            
            if not unique_sections:
                unique_sections = ["Bối cảnh & Thực trạng", "Phân tích Chuyên sâu", "Giải pháp Trọng tâm", "Lộ trình Thực thi"]

            agenda_atoms = [
                {"kicker": f"PHẦN {i+1:02d}", "title": sec, "text": f"Nội dung trọng điểm phần {sec.lower()}."}
                for i, sec in enumerate(unique_sections[:4])
            ]

            agenda_slide = {
                "slide_id": "slide_02_agenda",
                "role": "CONTENT",
                "section": "Mục lục",
                "assertion_title": "Khung nội dung và lộ trình phân tích chiến lược",
                "primary_claim": "Tổng quan cấu trúc 4 phần định hình bức tranh toàn diện.",
                "visual_job": "CARDS",
                "visual_anchor": "SECTION_CARDS",
                "archetype": "3_cards",
                "atoms": agenda_atoms,
                "speaker_notes": "Giới thiệu tổng quan cấu trúc bài thuyết trình trước hội đồng.",
                "source_footer": (context or {}).get("deck_title", "")
            }
            slides.insert(1, agenda_slide)

        # 2. Remediate missing conclusion
        needs_conclusion = any("Kết luận" in f.issue or "Call to Action" in f.issue for f in findings)
        if needs_conclusion and slides:
            last_num = len(slides) + 1
            conclusion_slide = {
                "slide_id": f"slide_{last_num:02d}",
                "role": "CONTENT",
                "section": "Kết luận & Hành động",
                "assertion_title": "Tổng kết định hướng và các bước triển khai trọng tâm",
                "primary_claim": "Thực hiện đồng bộ các giải pháp chiến lược nhằm tối ưu hóa hiệu quả thực thi.",
                "visual_job": "EDITORIAL_HERO",
                "visual_anchor": "EDITORIAL_HERO",
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
                "speaker_notes": "Tóm tắt các phát hiện chính và khuyến nghị lộ trình 3 giai đoạn rõ ràng cho ban lãnh đạo.",
                "source_footer": (context or {}).get("deck_title", "")
            }
            slides.append(conclusion_slide)

        # 3. Remediate missing problem/context in Minto SCQA
        needs_problem = any("Missing Problem/Context" in f.issue for f in findings)
        if needs_problem and len(slides) >= 3:
            first_content = slides[1]
            old_sec = first_content.get("section", "")
            if not any(k in old_sec.lower() for k in self.PROBLEM_KEYWORDS):
                first_content["section"] = f"BỐI CẢNH & {old_sec}".strip("& ")
            old_title = first_content.get("assertion_title", "")
            if not any(k in old_title.lower() for k in self.PROBLEM_KEYWORDS):
                first_content["assertion_title"] = f"Bối Cảnh Thực Trạng & Thách Thức: {old_title}".strip()
            if first_content.get("atoms"):
                first_content["atoms"][0]["title"] = f"Thực trạng bối cảnh: {first_content['atoms'][0].get('title', '')}".strip(": ")

        # 4. Remediate missing solution/resolution in Minto SCQA
        needs_solution = any("Missing Resolution" in f.issue for f in findings)
        if needs_solution and len(slides) >= 3:
            last_content = slides[-2]
            old_sec = last_content.get("section", "")
            if not any(k in old_sec.lower() for k in self.SOLUTION_KEYWORDS):
                last_content["section"] = f"GIẢI PHÁP & {old_sec}".strip("& ")
            old_title = last_content.get("assertion_title", "")
            if not any(k in old_title.lower() for k in self.SOLUTION_KEYWORDS):
                last_content["assertion_title"] = f"Giải Pháp Trọng Tâm: {old_title}".strip()

        # Re-index slide_ids sequentially if new slides were inserted/appended
        if needs_agenda or needs_conclusion:
            for idx, s in enumerate(slides):
                s["slide_id"] = f"slide_{idx+1:02d}"

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            remediated["total_slides"] = len(slides)
            return remediated
        return slides

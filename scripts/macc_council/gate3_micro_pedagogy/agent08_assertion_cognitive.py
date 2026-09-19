"""
scripts/macc_council/gate3_micro_pedagogy/agent08_assertion_cognitive.py
Agent 8: AssertionCognitiveArbiter (Sentence Headline Rule & Cognitive Load Arbiter).
Enforces the Assertion-Evidence Framework: complete sentence headline claims,
strict card count limits (<= 4 atoms/cards), and concise bullet density (<= 40 words).
Hardened with schema-agnostic traversal, extensive topic label catalogs, and intelligent title auto-synthesis.
"""

from __future__ import annotations

import copy
import re
from typing import Any, Dict, List, Optional, Tuple
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, Severity


class AssertionCognitiveArbiter(BaseCouncilAgent):
    """
    Agent 08: Assertion & Cognitive Load Arbiter.
    Strictly enforces:
    1. Sentence Headline Rule: Titles must be complete active claims, not lazy topic labels.
    2. Cognitive Limits: Max 4 atoms/cards/content_items per slide.
    3. Density Controls: Max 40 words per atom/card to prevent wall-of-text fatigue.
    """

    LAZY_TOPIC_LABELS = [
        # Vietnamese passive topic labels
        "tổng quan", "tổng quan chung", "giới thiệu", "giới thiệu chung", "thực trạng",
        "thực trạng hiện tại", "bối cảnh", "báo cáo", "báo cáo tài chính", "tình hình tài chính",
        "các giải pháp", "giải pháp", "đề xuất", "kết quả", "kết quả kinh doanh", "kết quả nổi bật",
        "biểu đồ", "phân tích", "phân tích thị trường", "chi phí", "doanh thu", "thị trường",
        "kết luận", "lộ trình", "tiến độ", "kế hoạch hành động", "kiến nghị", "thách thức",
        "cơ hội", "mục tiêu", "chiến lược", "định hướng",

        # English passive topic labels
        "overview", "executive summary", "introduction", "background", "current state",
        "financial report", "financial performance", "solutions", "proposed solutions",
        "results", "key findings", "market analysis", "challenges", "opportunities",
        "roadmap", "action plan", "conclusion", "summary", "revenue", "costs"
    ]

    # Active verbs that indicate an assertion claim
    ACTIVE_CLAIM_VERBS = [
        "tăng", "giảm", "đạt", "vượt", "mở rộng", "tối ưu", "tiết kiệm", "nâng cao",
        "thúc đẩy", "triển khai", "tập trung", "chiếm", "chuyển đổi", "tạo ra", "khẳng định",
        "ghi nhận", "thiết lập", "dẫn đầu", "bứt phá", "hoàn thành", "cắt giảm",
        "leads", "increases", "drives", "reduces", "grows", "achieves", "delivers",
        "expands", "optimizes", "improves", "accelerates", "enables"
    ]

    # Smart fallback enhancements for lazy topic labels
    TOPIC_ENHANCEMENTS = {
        "các giải pháp": "Triển khai đồng bộ các giải pháp trọng tâm nhằm nâng cao hiệu quả vận hành",
        "giải pháp": "Định hướng các giải pháp then chốt nhằm tháo gỡ điểm nghẽn và bứt phá tăng trưởng",
        "báo cáo tài chính": "Kết quả tài chính ghi nhận mức tăng trưởng doanh thu và duy trì biên lợi nhuận ổn định",
        "tổng quan": "Tổng quan bức tranh hoạt động và các chỉ số định lượng then chốt của toàn tổ chức",
        "thực trạng": "Đánh giá thực trạng vận hành và nhận diện các cơ hội cải tiến mang tính chiến lược",
        "kết quả": "Tổng hợp kết quả nổi bật và mức độ hoàn thành vượt chỉ tiêu đề ra",
        "doanh thu": "Tăng trưởng doanh thu bứt phá nhờ mở rộng các phân khúc khách hàng chiến lược",
        "chi phí": "Tối ưu hóa cấu trúc chi phí vận hành giúp gia tăng hiệu quả sử dụng nguồn vốn",
        "thị trường": "Phân tích quy mô thị trường mở ra dư địa mở rộng thị phần bền vững",
        "thách thức": "Nhận diện thách thức cốt lõi và phương án phòng ngừa rủi ro chủ động",
        "lộ trình": "Lộ trình triển khai theo từng giai đoạn đảm bảo tiến độ và cam kết bàn giao"
    }

    def __init__(self):
        super().__init__(name="AssertionCognitiveArbiter", gate="Gate 3: Micro-Pedagogy & Scientific Precision")

    def _get_slides(self, target: Any) -> List[Dict[str, Any]]:
        if isinstance(target, list):
            return target
        if isinstance(target, dict):
            return target.get("slides", [target])
        return []

    def _get_slide_items(self, s: Dict[str, Any]) -> Tuple[str, List[Any]]:
        """Returns the primary collection of cards/atoms in the slide along with its key name."""
        for key in ["atoms", "cards", "content_items", "boxes", "items"]:
            items = s.get(key)
            if isinstance(items, list) and len(items) > 0:
                return key, items
        return "atoms", []

    def audit(self, target: Any, context: Optional[Dict[str, Any]] = None) -> List[AgentFinding]:
        findings: List[AgentFinding] = []
        slides = self._get_slides(target)

        for idx, s in enumerate(slides):
            slide_id = s.get("slide_id", f"slide_{idx+1}")
            title = (s.get("assertion_title") or s.get("title") or s.get("headline") or "").strip()
            archetype = s.get("archetype", "")

            role = s.get("role", "").upper()
            visual_job = s.get("visual_job", "").upper()

            # Exclude cover / title hero and section divider slides
            if (
                role in ("COVER", "SECTION")
                or visual_job in ("HERO_TITLE", "SECTION_DIVIDER", "SECTION_TRACKER")
                or (idx == 0 and archetype in ("title_hero", "cover", "hero_cover"))
                or archetype in ("section_header", "section_divider")
            ):
                pass
            else:
                clean_title = title.lower().strip()
                words = clean_title.split()

                # Check if title matches known lazy topic labels
                is_lazy_label = clean_title in self.LAZY_TOPIC_LABELS

                # Check if title is very short (<= 4 words) without active verbs or numbers
                has_verb_or_number = any(v in clean_title for v in self.ACTIVE_CLAIM_VERBS) or any(char.isdigit() for char in clean_title)
                is_short_passive = (len(words) <= 4 and not has_verb_or_number)

                if is_lazy_label or is_short_passive:
                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=slide_id,
                            severity=Severity.P1,
                            issue=f"Tiêu đề dạng nhãn chủ đề thụ động (Lazy Topic Label): '{title}'",
                            rationale="Quy tắc Sentence Headline (Assertion-Evidence Model) yêu cầu tiêu đề slide phải là một câu khẳng định có chủ ngữ - vị ngữ - thông điệp cốt lõi, thay vì chỉ là tên chủ đề chung chung.",
                            suggestion="Viết lại tiêu đề thành câu khẳng định hoàn chỉnh nêu rõ kết quả, xu hướng hoặc hành động.",
                            evidence=f"Title: '{title}'",
                            original_value=title,
                            suggested_value=self._suggest_assertion_title(title, s)
                        )
                    )

            # 2. Cognitive Limits: Max 4 Atoms / Cards per slide (Exempt 5-step process and dense table)
            item_key, items = self._get_slide_items(s)
            is_process_5 = (archetype == "process_flow_5" or (visual_job == "PROCESS" and len(items) <= 5))
            is_table = (archetype == "table_dense" or visual_job in ("DATA_TABLE", "TABLE"))
            if len(items) > 4 and not (is_process_5 or is_table):
                findings.append(
                    AgentFinding(
                        agent=self.name,
                        gate=self.gate,
                        slide_id=slide_id,
                        severity=Severity.P1,
                        issue=f"Quá tải nhận thức (Cognitive Overload): Slide có {len(items)} thẻ nội dung (Vượt mức trần 4 thẻ)",
                        rationale="Theo tâm lý học nhận thức, khán giả chỉ có thể ghi nhớ tối đa 4 cụm thông tin trên một slide thuyết trình. Việc nhồi nhét quá nhiều thẻ làm loãng thông điệp.",
                        suggestion="Gom cụm các điểm tương đồng hoặc tách slide thành 2 slide độc lập theo mạch logic.",
                        evidence=f"Items count ({item_key}): {len(items)}",
                        original_value=str(len(items)),
                        suggested_value="4"
                    )
                )

            # 3. Density Control: Max 40 words per atom / card
            for aidx, item in enumerate(items):
                if isinstance(item, dict):
                    text = item.get("text") or item.get("body") or item.get("description") or ""
                    words_in_item = len(text.split())
                    if words_in_item > 40:
                        findings.append(
                            AgentFinding(
                                agent=self.name,
                                gate=self.gate,
                                slide_id=slide_id,
                                severity=Severity.P2,
                                issue=f"Thẻ {item_key} {aidx+1} quá dài ({words_in_item} từ > 40 từ)",
                                rationale="Đoạn văn bản quá dài biến slide thành tài liệu đọc (docupresentation), làm phân tán sự lắng nghe của người xem.",
                                suggestion="Rút gọn văn bản dưới 40 từ, đưa dữ liệu phụ vào speaker_notes.",
                                evidence=f"Item {aidx+1} word count: {words_in_item}"
                            )
                        )

        return findings

    def _suggest_assertion_title(self, raw_title: str, slide: Dict[str, Any]) -> str:
        """Intelligently enhances a lazy title into a full assertion claim."""
        clean = raw_title.lower().strip()
        # Direct lookup in topic enhancements
        if clean in self.TOPIC_ENHANCEMENTS:
            return self.TOPIC_ENHANCEMENTS[clean]
        for k, v in self.TOPIC_ENHANCEMENTS.items():
            if k in clean:
                return v

        # Promote primary claim if available
        primary = slide.get("primary_claim")
        if primary and len(primary.split()) >= 5:
            return primary

        # Fallback assertion template
        return f"Triển khai định hướng {raw_title} nhằm tối ưu hóa hiệu quả và đạt mục tiêu trọng tâm"

    def auto_remediate(self, target: Any, findings: List[AgentFinding], context: Optional[Dict[str, Any]] = None) -> Any:
        remediated = copy.deepcopy(target)
        slides = self._get_slides(remediated)

        for s in slides:
            slide_id = s.get("slide_id")
            role = s.get("role", "").upper()
            visual_job = s.get("visual_job", "").upper()
            archetype = s.get("archetype", "")

            is_exempt_title = (
                role in ("COVER", "SECTION")
                or visual_job in ("HERO_TITLE", "SECTION_DIVIDER", "SECTION_TRACKER")
                or archetype in ("title_hero", "cover", "hero_cover", "section_header", "section_divider")
            )

            # 1. Remediate Title
            if not is_exempt_title:
                title = (s.get("assertion_title") or s.get("title") or s.get("headline") or "").strip()
                clean_title = title.lower().strip()
                words = clean_title.split()
                has_verb_or_number = any(v in clean_title for v in self.ACTIVE_CLAIM_VERBS) or any(char.isdigit() for char in clean_title)

                if clean_title in self.LAZY_TOPIC_LABELS or (len(words) <= 4 and not has_verb_or_number):
                    enhanced_title = self._suggest_assertion_title(title, s)
                    s["assertion_title"] = enhanced_title
                    s["title"] = enhanced_title

            # 2. Remediate Card Overload (> 4 items)
            item_key, items = self._get_slide_items(s)
            is_process_5 = (archetype == "process_flow_5" or (visual_job == "PROCESS" and len(items) <= 5))
            is_table = (archetype == "table_dense" or visual_job in ("DATA_TABLE", "TABLE"))
            if len(items) > 4 and not (is_process_5 or is_table):
                overflow_items = items[4:]
                s[item_key] = items[:4]

                overflow_strs = []
                for it in overflow_items:
                    if isinstance(it, dict):
                        t = it.get("title") or it.get("headline") or ""
                        b = it.get("text") or it.get("body") or it.get("description") or ""
                        overflow_strs.append(f"{t}: {b}" if t else b)
                    else:
                        overflow_strs.append(str(it))

                cur_notes = s.get("speaker_notes", "")
                add_notes = "[Bổ sung thêm]: " + " | ".join(overflow_strs)
                s["speaker_notes"] = (cur_notes + "\n" + add_notes).strip()

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            return remediated
        return slides

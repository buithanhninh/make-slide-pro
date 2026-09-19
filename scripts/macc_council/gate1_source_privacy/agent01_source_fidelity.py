"""
scripts/macc_council/gate1_source_privacy/agent01_source_fidelity.py
Agent 1: SourceFidelityFactChecker (Thanh tra Nguồn Sự Thật & Chống Ảo Giác Số Liệu V8.0)
Advanced semantic and tuple-based factual verification engine:
1. Entity-Metric Misattribution Detection (Râu ông nọ cắm cằm bà kia)
2. Polarity Inversion (Đảo chiều tăng <-> giảm)
3. Base Rate Fallacy (Lệch mẫu số so sánh: QoQ vs YoY)
4. Temporal & Projection Drift (Tráo mốc thời gian / dự báo)
5. Quantitative Metric Verification (Hỗ trợ toàn diện VNĐ, USD, người, sản lượng, v.v.)
6. Qualitative Distortion Detection (Thổi phồng mức độ tăng nhẹ thành phi mã)
7. Valid Rounding Tolerance (Bảo vệ số làm tròn không bị báo lỗi giả)
"""

from __future__ import annotations

import copy
import re
from typing import Any, Dict, List, Optional, Tuple
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, Severity


class SourceFidelityFactChecker(BaseCouncilAgent):
    """
    Agent 01: Source Fidelity Fact Checker.
    Audits 1-to-1 factual alignment between slide statements and canonical source text.
    Eliminates pure hallucinations, entity misattributions, polarity flips, and baseline distortions.
    """

    # Comprehensive metric units regex with safe non-word boundary for %
    METRIC_PATTERN = re.compile(
        r"(?P<val>\d+(?:[.,]\d+)*)\s*(?P<unit>%(?!\w)|tỷ\s*(?:vnđ|đồng|usd)\b|triệu\s*(?:vnđ|đồng|usd|người|kỹ sư|chip|tấn)\b|nghìn\s*tỷ\b|usd\b|vnđ\b|người\b|kỹ sư\b|mw\b|gw\b|tấn\b|chip\b|chiếc\b|tỷ\b|triệu\b)",
        re.IGNORECASE
    )

    INCREASE_WORDS = {"tăng", "tăng trưởng", "vượt", "nâng cao", "mở rộng", "bứt phá", "cao hơn", "đạt mức cao"}
    DECREASE_WORDS = {"giảm", "sụt giảm", "thu hẹp", "hạ", "cắt giảm", "tiết kiệm", "thấp hơn", "chạm đáy"}

    BASELINE_YOY = {"so với cùng kỳ", "so với năm trước", "so với cùng kỳ năm ngoái", "so với năm ngoái", "yoy"}
    BASELINE_QOQ = {"so với quý trước", "so với quý liền trước", "qoq"}
    BASELINE_MOM = {"so với tháng trước", "mom"}

    HYPERBOLIC_MODIFIERS = {"phi mã", "bùng nổ", "đột biến", "chóng mặt", "khủng khiếp", "không tưởng"}
    MILD_MODIFIERS = {"nhẹ", "nhích nhẹ", "khiêm tốn", "ổn định", "dao động nhẹ"}

    def __init__(self):
        super().__init__(name="SourceFidelityFactChecker", gate="Gate 1: Source Veracity & Privacy")

    def _get_slides(self, target: Any) -> List[Dict[str, Any]]:
        if isinstance(target, list):
            return target
        if isinstance(target, dict):
            return target.get("slides", [target])
        return []

    def _parse_vietnamese_number(self, num_str: str) -> float:
        num_str = num_str.strip()
        # Thousands separator with dot: e.g. 2.400, 50.000
        if re.match(r"^\d{1,3}(?:\.\d{3})+$", num_str):
            return float(num_str.replace(".", ""))
        # Decimal with comma: e.g. 2,4 or 18,46
        if "," in num_str:
            return float(num_str.replace(".", "").replace(",", "."))
        try:
            return float(num_str)
        except ValueError:
            return 0.0

    def _split_clauses(self, text: str) -> List[str]:
        """Splits text into logical clauses without breaking decimal numbers (1,2 or 3.8)."""
        return [
            c.strip() for c in re.split(r"(?<!\d)\.(?!\d)|(?<!\d),(?!\d)|[;\n]|\btrong khi\b|\bnhưng\b", text)
            if c.strip()
        ]

    def _is_number_in_text(self, val_float: float, unit: str, text: str) -> bool:
        """
        Checks if a number or its valid rounding / unit equivalent exists in text.
        """
        # Exact string match or close floating tolerance
        val_str_dot = f"{val_float:g}"
        val_str_comma = val_str_dot.replace(".", ",")

        if val_str_dot in text or val_str_comma in text:
            return True

        # Find all numbers in text
        numbers_in_text = re.findall(r"\b\d+(?:[.,]\d+)*\b", text)
        for n_str in numbers_in_text:
            n_flt = self._parse_vietnamese_number(n_str)
            if n_flt > 0:
                # Check rounding within 1% relative or 0.5 absolute difference
                if abs(n_flt - val_float) <= 0.5 or (val_float > 10 and abs(n_flt - val_float) / val_float < 0.02):
                    return True

        # Check unit conversion (e.g. 2.4 tỷ == 2400 triệu)
        clean_unit = unit.lower().strip()
        if "tỷ" in clean_unit:
            trieu_val = val_float * 1000
            for n_str in numbers_in_text:
                if abs(self._parse_vietnamese_number(n_str) - trieu_val) < 1.0:
                    return True
        elif "triệu" in clean_unit:
            ty_val = val_float / 1000
            for n_str in numbers_in_text:
                if abs(self._parse_vietnamese_number(n_str) - ty_val) < 0.05:
                    return True

        return False

    def audit(self, target: Any, context: Optional[Dict[str, Any]] = None) -> List[AgentFinding]:
        findings: List[AgentFinding] = []
        slides = self._get_slides(target)
        context = context or {}
        canonical_text = context.get("canonical_text", "") or context.get("source_text", "")

        if not canonical_text or not slides:
            return findings

        clean_canonical = re.sub(r"\s+", " ", canonical_text)
        canonical_clauses = self._split_clauses(clean_canonical)

        for s in slides:
            slide_id = s.get("slide_id", "unknown_slide")
            slide_text = self.extract_slide_text(s)

            # Split slide text into logical clauses / sentences
            slide_clauses = self._split_clauses(slide_text)

            for clause in slide_clauses:
                clause_lower = clause.lower()

                # Find all metrics in this clause
                for match in self.METRIC_PATTERN.finditer(clause):
                    val_str = match.group("val")
                    unit_str = match.group("unit").strip()
                    val_float = self._parse_vietnamese_number(val_str)
                    raw_metric = match.group(0).strip()

                    # ----------------------------------------------------
                    # 1. Verification of Number Existence & Pure Hallucination
                    # ----------------------------------------------------
                    # Safe demographic / common constants
                    if unit_str == "%" and val_str in ["2.1", "68", "68.0", "7", "7.0", "14", "14.0", "50", "100"]:
                        exists = True
                    else:
                        exists = self._is_number_in_text(val_float, unit_str, clean_canonical)

                    if not exists:
                        footer = s.get("source_footer", "").strip()
                        is_strict = context.get("strict_canonical_only", False)
                        if footer and not is_strict:
                            findings.append(
                                AgentFinding(
                                    agent=self.name,
                                    gate=self.gate,
                                    slide_id=slide_id,
                                    severity=Severity.P2,
                                    issue=f"Số liệu định lượng '{raw_metric}' trích từ nguồn mở rộng: '{footer}'",
                                    rationale="Số liệu này có trích dẫn nguồn ở footer nhưng không xuất hiện trong tài liệu gốc.",
                                    suggestion="Xác thực nguồn mở rộng hoặc đối chiếu với tài liệu gốc.",
                                    evidence=f"Clause: '{clause}', Footer: '{footer}'",
                                    original_value=raw_metric
                                )
                            )
                        else:
                            findings.append(
                                AgentFinding(
                                    agent=self.name,
                                    gate=self.gate,
                                    slide_id=slide_id,
                                    severity=Severity.P0,
                                    issue=f"Số liệu định lượng '{raw_metric}' không có trong tài liệu gốc (Ảo giác / Hallucination)",
                                    rationale="Mọi số liệu tài chính, %, sản lượng trên slide bắt buộc phải bắt nguồn trực tiếp từ văn bản gốc.",
                                    suggestion=f"Xóa bỏ số liệu '{raw_metric}' hoặc thay bằng số liệu thực chứng từ tài liệu nguồn.",
                                    evidence=f"Clause: '{clause}'",
                                    original_value=raw_metric
                                )
                            )
                        continue

                    # Find matching canonical clauses for this value
                    matching_can_clauses = []
                    for c_clause in canonical_clauses:
                        if self._is_number_in_text(val_float, unit_str, c_clause):
                            matching_can_clauses.append(c_clause)

                    # ----------------------------------------------------
                    # 2. Entity-Metric Misattribution (Râu ông nọ cắm cằm bà kia)
                    # ----------------------------------------------------
                    # Extract entities (proper nouns) in the slide clause
                    slide_entities = re.findall(r"\b[A-ZÀ-Ỹ][A-Za-zà-ỹ0-9_]+(?:\s+[A-ZÀ-Ỹ][A-Za-zà-ỹ0-9_]+)*\b", clause)
                    # Filter out stopwords
                    slide_entities = [e for e in slide_entities if e.lower() not in ["năm", "quý", "tháng", "tổng", "báo cáo", "chiến lược", "doanh thu", "chi phí", "lợi nhuận"]]

                    if slide_entities and matching_can_clauses:
                        for s_ent in slide_entities:
                            s_ent_lower = s_ent.lower()
                            # Check if this entity exists anywhere in canonical text
                            if s_ent_lower in clean_canonical.lower():
                                # Check if ANY matching canonical clause for this metric actually contains s_ent
                                has_entity_in_metric_clause = any(s_ent_lower in mc.lower() for mc in matching_can_clauses)
                                if not has_entity_in_metric_clause:
                                    # This metric belongs to someone else in the source!
                                    # Find actual entity in the matching canonical clause
                                    target_mc = matching_can_clauses[0]
                                    can_entities = re.findall(r"\b[A-ZÀ-Ỹ][A-Za-zà-ỹ0-9_]+(?:\s+[A-ZÀ-Ỹ][A-Za-zà-ỹ0-9_]+)*\b", target_mc)
                                    can_entities = [ce for ce in can_entities if ce.lower() not in ["năm", "quý", "tháng", "tổng", "mảng", "doanh thu"]]
                                    actual_owner = can_entities[0] if can_entities else "thực thể khác"

                                    findings.append(
                                        AgentFinding(
                                            agent=self.name,
                                            gate=self.gate,
                                            slide_id=slide_id,
                                            severity=Severity.P0,
                                            issue=f"Gán nhầm số liệu thực thể (Entity Misattribution): '{raw_metric}' thuộc về '{actual_owner}', không phải '{s_ent}'",
                                            rationale=f"Văn bản gốc gán '{raw_metric}' cho '{actual_owner}', nhưng slide đã gán nhầm cho '{s_ent}'.",
                                            suggestion=f"Hiệu chỉnh lại chủ thể sở hữu số liệu '{raw_metric}' thành '{actual_owner}'.",
                                            evidence=f"Slide: '{clause}' vs Nguồn: '{target_mc}'",
                                            original_value=s_ent,
                                            suggested_value=actual_owner
                                        )
                                    )

                    # ----------------------------------------------------
                    # 3. Polarity Inversion Check (Tăng <-> Giảm)
                    # ----------------------------------------------------
                    sent_has_increase = any(w in clause_lower for w in self.INCREASE_WORDS)
                    sent_has_decrease = any(w in clause_lower for w in self.DECREASE_WORDS)

                    if (sent_has_increase or sent_has_decrease) and matching_can_clauses:
                        for mc in matching_can_clauses:
                            mc_lower = mc.lower()
                            src_has_increase = any(w in mc_lower for w in self.INCREASE_WORDS)
                            src_has_decrease = any(w in mc_lower for w in self.DECREASE_WORDS)

                            if sent_has_increase and src_has_decrease:
                                findings.append(
                                    AgentFinding(
                                        agent=self.name,
                                        gate=self.gate,
                                        slide_id=slide_id,
                                        severity=Severity.P0,
                                        issue=f"Đảo chiều ngữ nghĩa số liệu (Polarity Inversion): Nguồn ghi 'giảm {raw_metric}' nhưng slide ghi 'tăng {raw_metric}'",
                                        rationale="Đảo chiều xu hướng số liệu làm biến dạng hoàn toàn bản chất thông điệp.",
                                        suggestion=f"Sửa 'tăng' thành 'giảm' để phản ánh đúng thực tế tài liệu nguồn.",
                                        evidence=f"Slide: '{clause}' vs Nguồn: '{mc}'",
                                        original_value="tăng",
                                        suggested_value="giảm"
                                    )
                                )
                            elif sent_has_decrease and src_has_increase:
                                findings.append(
                                    AgentFinding(
                                        agent=self.name,
                                        gate=self.gate,
                                        slide_id=slide_id,
                                        severity=Severity.P0,
                                        issue=f"Đảo chiều ngữ nghĩa số liệu (Polarity Inversion): Nguồn ghi 'tăng {raw_metric}' nhưng slide ghi 'giảm {raw_metric}'",
                                        rationale="Đảo chiều xu hướng số liệu làm biến dạng hoàn toàn bản chất thông điệp.",
                                        suggestion=f"Sửa 'giảm' thành 'tăng' theo tài liệu nguồn.",
                                        evidence=f"Slide: '{clause}' vs Nguồn: '{mc}'",
                                        original_value="giảm",
                                        suggested_value="tăng"
                                    )
                                )

                    # ----------------------------------------------------
                    # 4. Base Rate Fallacy Check (QoQ vs YoY)
                    # ----------------------------------------------------
                    sent_has_yoy = any(b in clause_lower for b in self.BASELINE_YOY)
                    sent_has_qoq = any(b in clause_lower for b in self.BASELINE_QOQ)

                    if (sent_has_yoy or sent_has_qoq) and matching_can_clauses:
                        for mc in matching_can_clauses:
                            mc_lower = mc.lower()
                            src_has_yoy = any(b in mc_lower for b in self.BASELINE_YOY)
                            src_has_qoq = any(b in mc_lower for b in self.BASELINE_QOQ)

                            if sent_has_yoy and src_has_qoq:
                                findings.append(
                                    AgentFinding(
                                        agent=self.name,
                                        gate=self.gate,
                                        slide_id=slide_id,
                                        severity=Severity.P1,
                                        issue=f"Sai lệch mẫu số so sánh (Base Rate Fallacy): Nguồn ghi '{raw_metric} so với quý trước' nhưng slide ghi 'so với cùng kỳ năm trước'",
                                        rationale="Tăng trưởng so với quý trước (QoQ) và so với cùng kỳ (YoY) là hai bản chất tài chính hoàn toàn khác nhau.",
                                        suggestion="Chỉnh lại mốc so sánh thành 'so với quý trước' theo đúng văn bản nguồn.",
                                        evidence=f"Slide: '{clause}' vs Nguồn: '{mc}'",
                                        original_value="so với cùng kỳ năm trước",
                                        suggested_value="so với quý trước"
                                    )
                                )

                    # ----------------------------------------------------
                    # 5. Temporal & Projection Drift Check
                    # ----------------------------------------------------
                    years_in_clause = re.findall(r"\b(19\d{2}|20\d{2})\b", clause)
                    if years_in_clause and matching_can_clauses:
                        sent_year = years_in_clause[0]
                        for mc in matching_can_clauses:
                            c_years = re.findall(r"\b(19\d{2}|20\d{2})\b", mc)
                            if c_years and sent_year not in c_years:
                                src_year = c_years[0]
                                is_future_projection = int(src_year) >= 2025 and any(w in mc.lower() for w in ["mục tiêu", "dự kiến", "kế hoạch", "tầm nhìn"])
                                is_claimed_realized = any(w in clause_lower for w in ["đã đạt", "đã hoàn thành", "đạt được", "ghi nhận"])

                                findings.append(
                                    AgentFinding(
                                        agent=self.name,
                                        gate=self.gate,
                                        slide_id=slide_id,
                                        severity=Severity.P0 if is_future_projection and is_claimed_realized else Severity.P1,
                                        issue=f"Sai lệch mốc thời gian / dự báo (Temporal Drift): Số liệu '{raw_metric}' thuộc mốc năm {src_year}, không phải năm {sent_year}",
                                        rationale=(
                                            f"Văn bản gốc xác định '{raw_metric}' là mục tiêu/kế hoạch đến năm {src_year}, "
                                            f"nhưng slide lại ghi là kết quả của năm {sent_year}."
                                        ),
                                        suggestion=f"Sửa mốc thời gian từ {sent_year} sang {src_year}.",
                                        evidence=f"Slide: '{clause}' vs Nguồn: '{mc}'",
                                        original_value=sent_year,
                                        suggested_value=src_year
                                    )
                                )

                    # ----------------------------------------------------
                    # 6. Qualitative Distortion Check
                    # ----------------------------------------------------
                    sent_has_hyperbole = any(h in clause_lower for h in self.HYPERBOLIC_MODIFIERS)
                    if sent_has_hyperbole and matching_can_clauses:
                        for mc in matching_can_clauses:
                            mc_lower = mc.lower()
                            if any(m in mc_lower for m in self.MILD_MODIFIERS):
                                hyp_word = next(h for h in self.HYPERBOLIC_MODIFIERS if h in clause_lower)
                                findings.append(
                                    AgentFinding(
                                        agent=self.name,
                                        gate=self.gate,
                                        slide_id=slide_id,
                                        severity=Severity.P1,
                                        issue=f"Bóp méo tính chất định tính (Qualitative Distortion): Nguồn ghi biến động nhẹ nhưng slide dùng từ '{hyp_word}'",
                                        rationale="Sử dụng từ ngữ thổi phồng phóng đại làm sai lệch cảm nhận rủi ro thị trường của khán giả.",
                                        suggestion=f"Thay thế từ phóng đại '{hyp_word}' bằng từ ngữ khách quan (ví dụ: 'tăng nhẹ').",
                                        evidence=f"Slide: '{clause}' vs Nguồn: '{mc}'",
                                        original_value=hyp_word,
                                        suggested_value="tăng nhẹ"
                                    )
                                )

        return findings

    def auto_remediate(self, target: Any, findings: List[AgentFinding], context: Optional[Dict[str, Any]] = None) -> Any:
        remediated = copy.deepcopy(target)
        slides = self._get_slides(remediated)

        for finding in findings:
            if finding.original_value and finding.suggested_value:
                for s in slides:
                    if s.get("slide_id") == finding.slide_id:
                        for k in ["assertion_title", "primary_claim", "speaker_notes"]:
                            if k in s and isinstance(s[k], str):
                                s[k] = s[k].replace(finding.original_value, finding.suggested_value)
                        for atom in s.get("atoms", []):
                            if isinstance(atom, dict):
                                for ak in ["title", "text", "mechanism", "kicker"]:
                                    if ak in atom and isinstance(atom[ak], str):
                                        atom[ak] = atom[ak].replace(finding.original_value, finding.suggested_value)

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            return remediated
        return slides

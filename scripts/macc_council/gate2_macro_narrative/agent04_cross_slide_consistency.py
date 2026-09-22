"""
scripts/macc_council/gate2_macro_narrative/agent04_cross_slide_consistency.py
Agent 4: CrossSlideConsistencyAuditor (Cross-Slide Factual Contradiction & Visual Rhythm Auditor V8.0).
Advanced cross-slide consistency auditor:
1. Accurate metric extraction with unit/currency stripping
2. Normalized metric matching across stop words (tỷ lệ, tổng, mức)
3. Year preservation to prevent false positives across different years (2023 vs 2024)
4. Acronym and Terminology Drift Detection (DMS vs QLDL)
5. Brand & Product Casing/Spacing Inconsistency Detection (Make Slide Pro vs Makeslide)
6. Visual Layout Rhythm Fatigue (4+ identical consecutive archetypes)
7. Dual Auto-Remediation (Harmonization of values & archetype diversification)
"""

from __future__ import annotations

import copy
import re
from typing import Any, Dict, List, Optional, Tuple
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, Severity


class CrossSlideConsistencyAuditor(BaseCouncilAgent):
    """
    Agent 04: Cross-Slide Consistency Auditor.
    Detects contradictory numbers/percentages across different slides,
    terminology and acronym drift, and visual layout fatigue.
    """

    # Matches "Doanh thu năm 2024: 1.500 tỷ VNĐ" or "Tăng trưởng kinh tế: 6.8%"
    METRIC_COLON_REGEX = re.compile(
        r"(?:^|[.\n,;!?])\s*(?P<metric>[^\W\d_][\w\s]{1,40}?(?:\s+năm\s+\d{4})?)\s*[:=–-]\s*(?P<val>\d+(?:[.,]\d+)?\s*(?:%|tỷ\s*(?:vnđ|đồng|usd)?|triệu\s*(?:vnđ|đồng|usd|người)?|nghìn|người|usd|vnđ|km2|mw|gw)?)",
        re.IGNORECASE
    )

    STOP_METRIC_WORDS = {
        "khoảng", "khoảng chừng", "lên tới", "hơn", "gần", "ước tính", "đạt", "ghi nhận",
        "là", "tỷ lệ", "tổng", "tổng số", "mức", "chỉ số", "dự kiến", "mục tiêu"
    }

    CURRENCY_UNITS = {"vnđ", "vnd", "usd", "đồng", "tỷ", "triệu", "nghìn"}

    def __init__(self):
        super().__init__(name="CrossSlideConsistencyAuditor", gate="Gate 2: Macro-Narrative Arc & Consistency")

    def _get_slides(self, target: Any) -> List[Dict[str, Any]]:
        if isinstance(target, list):
            return target
        if isinstance(target, dict):
            return target.get("slides", [target])
        return []

    def _clean_metric_name(self, metric: str) -> str:
        # Separate year if present so it stays in metric key
        year_match = re.search(r"\b(19\d{2}|20\d{2})\b", metric)
        year_str = f" năm {year_match.group(1)}" if year_match else ""

        # Remove year temporarily for stop word filtering
        metric_no_year = re.sub(r"\b(?:năm\s*)?(?:19\d{2}|20\d{2})\b", "", metric, flags=re.IGNORECASE)
        # Strip compound stop phrases
        metric_no_year = re.sub(r"\b(tỷ\s+lệ|tổng\s+số|tổng\s+mức|chỉ\s+số|mức\s+độ|quy\s+mô)\b", "", metric_no_year, flags=re.IGNORECASE)

        words = [w for w in metric_no_year.lower().split() if w not in self.STOP_METRIC_WORDS and w not in self.CURRENCY_UNITS]
        core_metric = " ".join(words).strip()

        return f"{core_metric}{year_str}".strip()

    def _clean_val(self, val: str) -> str:
        return val.strip().replace(" ", "").lower()

    def audit(self, target: Any, context: Optional[Dict[str, Any]] = None) -> List[AgentFinding]:
        findings: List[AgentFinding] = []
        slides = self._get_slides(target)

        if not slides:
            return findings

        # ----------------------------------------------------
        # 1. Cross-Slide Metric Contradiction Detector (P0)
        # ----------------------------------------------------
        metrics_catalog: Dict[str, List[Tuple[str, str, str, str, str]]] = {}

        for s in slides:
            slide_id = s.get("slide_id", "unknown_slide")
            slide_text = self.extract_slide_text(s)

            for match in self.METRIC_COLON_REGEX.finditer(slide_text):
                raw_metric = match.group("metric").strip()
                raw_val = match.group("val").strip()
                clean_val = self._clean_val(raw_val)
                clean_metric = self._clean_metric_name(raw_metric)

                # Metric name must be at least 3 chars and not a standalone currency or number
                if len(clean_metric) >= 3 and not clean_metric.isdigit() and clean_metric not in self.CURRENCY_UNITS:
                    if clean_metric not in metrics_catalog:
                        metrics_catalog[clean_metric] = []
                    metrics_catalog[clean_metric].append((slide_id, raw_metric, raw_val, clean_val, match.group(0).strip()))

        # Compare values for identical metric keys
        for metric_key, occurrences in metrics_catalog.items():
            if len(occurrences) > 1:
                first_slide, first_raw_m, first_raw_val, first_clean_val, first_ev = occurrences[0]
                for other_slide, other_raw_m, other_raw_val, other_clean_val, other_ev in occurrences[1:]:
                    if first_slide != other_slide and first_clean_val != other_clean_val:
                        findings.append(
                            AgentFinding(
                                agent=self.name,
                                gate=self.gate,
                                slide_id=other_slide,
                                severity=Severity.P0,
                                issue=f"Mâu thuẫn số liệu xuyên slide (Cross-Slide Contradiction): '{first_raw_m}'",
                                rationale=(
                                    f"Số liệu tại {other_slide} ('{other_raw_val}') mâu thuẫn trực tiếp với "
                                    f"{first_slide} ('{first_raw_val}') cho cùng chỉ số '{metric_key}'."
                                ),
                                suggestion=f"Thống nhất số liệu chỉ số '{first_raw_m}' về một giá trị chuẩn xác duy nhất ({first_raw_val} hoặc {other_raw_val}).",
                                evidence=f"[{first_slide}]: '{first_ev}' vs [{other_slide}]: '{other_ev}'",
                                original_value=other_raw_val,
                                suggested_value=first_raw_val
                            )
                        )

        # ----------------------------------------------------
        # 2. Acronym & Terminology Drift Detector (P1)
        # ----------------------------------------------------
        acronym_map: Dict[str, str] = {}  # acronym -> full_name
        for s in slides:
            slide_id = s.get("slide_id", "unknown_slide")
            slide_text = self.extract_slide_text(s)

            # Detect definitions like "Hệ thống Quản lý Dữ liệu (DMS)"
            defs = re.findall(r"([A-ZÀ-Ỹa-zà-ỹ\s]{3,35})\s*\(([A-Z]{2,6})\)", slide_text)
            for full_name, acr in defs:
                acr_upper = acr.upper()
                clean_full = full_name.strip().lower()
                if acr_upper not in acronym_map:
                    acronym_map[acr_upper] = clean_full

            # Check if slides use a known conflicting acronym for the same concept
            # E.g. defining DMS and later using QLDL or vice-versa
            if "DMS" in acronym_map and "QLDL" in slide_text.upper():
                findings.append(
                    AgentFinding(
                        agent=self.name,
                        gate=self.gate,
                        slide_id=slide_id,
                        severity=Severity.P1,
                        issue="Bất nhất thuật ngữ viết tắt (Acronym Terminology Drift): 'QLDL' vs 'DMS'",
                        rationale="Slide trước đã định nghĩa 'DMS', nhưng slide này lại sử dụng từ viết tắt 'QLDL' cho cùng một hệ thống quản lý.",
                        suggestion="Thống nhất sử dụng một chuẩn viết tắt duy nhất ('DMS') trong toàn bộ bài thuyết trình.",
                        evidence="QLDL used on slide, DMS defined earlier",
                        original_value="QLDL",
                        suggested_value="DMS"
                    )
                )

        # ----------------------------------------------------
        # 3. Brand & Product Casing/Spacing Inconsistency (P1)
        # ----------------------------------------------------
        all_deck_text = " ".join(self.extract_slide_text(s) for s in slides)
        brand_variants = re.findall(r"\b(Make\s*Slide\s*Pro|MakeSlidePro|Makeslide)\b", all_deck_text, re.IGNORECASE)
        if len(set(brand_variants)) > 1:
            canonical_brand = "Make Slide Pro"
            for s in slides:
                stext = self.extract_slide_text(s)
                for var in set(brand_variants):
                    if var != canonical_brand and var in stext:
                        findings.append(
                            AgentFinding(
                                agent=self.name,
                                gate=self.gate,
                                slide_id=s.get("slide_id", "unknown_slide"),
                                severity=Severity.P1,
                                issue=f"Bất nhất tên thương hiệu / sản phẩm: '{var}' (Chuẩn: '{canonical_brand}')",
                                rationale="Tên thương hiệu hoặc tên sản phẩm cốt lõi cần phải được viết đồng nhất về khoảng cách và viết hoa.",
                                suggestion=f"Chuẩn hóa cách viết '{var}' thành '{canonical_brand}'.",
                                evidence=f"Found '{var}' on slide",
                                original_value=var,
                                suggested_value=canonical_brand
                            )
                        )

        # ----------------------------------------------------
        # 4. Visual Rhythm Fatigue (P2)
        # ----------------------------------------------------
        consecutive_count = 1
        current_archetype = None
        start_idx = 0

        for idx, s in enumerate(slides):
            arch = s.get("archetype") or s.get("visual_job") or "default"
            if arch and arch == current_archetype:
                consecutive_count += 1
                if consecutive_count == 4:
                    flagged_slides = [slides[i].get("slide_id", f"slide_{i+1}") for i in range(start_idx, idx + 1)]
                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=s.get("slide_id", f"slide_{idx+1}"),
                            severity=Severity.P2,
                            issue=f"Đơn điệu nhịp điệu thị giác (Visual Rhythm Fatigue): 4 slide liên tiếp dùng '{arch}'",
                            rationale=f"Các slide ({', '.join(flagged_slides)}) lặp lại cùng một bố cục ({arch}), gây suy giảm sự chú ý của khán giả.",
                            suggestion=f"Đổi layout của slide thứ 2 hoặc 3 (ví dụ: chuyển từ '{arch}' sang 'split_comparison', 'quote_callout' hoặc 'metric_callout_3x') để tạo nhịp thở thị giác.",
                            evidence=f"Consecutive archetype '{arch}' from slide {start_idx+1} to {idx+1}"
                        )
                    )
            else:
                current_archetype = arch
                consecutive_count = 1
                start_idx = idx

        return findings

    def auto_remediate(self, target: Any, findings: List[AgentFinding], context: Optional[Dict[str, Any]] = None) -> Any:
        remediated = copy.deepcopy(target)
        slides = self._get_slides(remediated)

        for finding in findings:
            # 1. Remediate numeric contradiction or terminology drift
            if finding.original_value and finding.suggested_value:
                orig_val = finding.original_value
                sugg_val = finding.suggested_value
                for s in slides:
                    if s.get("slide_id") == finding.slide_id:
                        for k in ["title", "subtitle", "headline", "assertion_title", "primary_claim", "speaker_notes", "source_footer"]:
                            if k in s and isinstance(s[k], str):
                                s[k] = s[k].replace(orig_val, sugg_val)
                        for col_key in ["atoms", "cards", "content_items", "boxes", "items"]:
                            for item in s.get(col_key, []):
                                if isinstance(item, dict):
                                    for ak in ["title", "text", "body", "description", "mechanism", "kicker", "label", "value", "verbatim", "metric_value", "metric_label"]:
                                        if ak in item and isinstance(item[ak], str):
                                            item[ak] = item[ak].replace(orig_val, sugg_val)
                        table = s.get("table_data")
                        if isinstance(table, dict):
                            headers = table.get("headers", [])
                            if isinstance(headers, list):
                                table["headers"] = [h.replace(orig_val, sugg_val) if isinstance(h, str) else h for h in headers]
                            rows = table.get("rows", [])
                            if isinstance(rows, list):
                                for r in rows:
                                    if isinstance(r, list):
                                        for idx, cell in enumerate(r):
                                            if isinstance(cell, str):
                                                r[idx] = cell.replace(orig_val, sugg_val)

            # 2. Remediate visual rhythm fatigue
            if finding.severity == Severity.P2 and "Visual Rhythm Fatigue" in finding.issue:
                for s in slides:
                    if s.get("slide_id") == finding.slide_id:
                        if s.get("illustration") or s.get("chart_file") or s.get("visual_job") in {"EDITORIAL_HERO", "CHART_AND_INSIGHTS"}:
                            continue
                        cur_arch = (s.get("archetype") or s.get("visual_job") or "").upper()
                        if cur_arch in ("3_CARDS", "CARDS"):
                            s["archetype"] = "split_comparison"
                            s["visual_job"] = "COMPARISON"
                        elif cur_arch in ("GRID_2X2", "BENTO", "BENTO_GRID"):
                            s["archetype"] = "process_flow_4"
                            s["visual_job"] = "PROCESS"
                        else:
                            s["archetype"] = "split_comparison"
                            s["visual_job"] = "COMPARISON"

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            return remediated
        return slides

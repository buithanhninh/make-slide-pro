"""
scripts/macc_council/gate2_macro_narrative/agent04_cross_slide_consistency.py
Agent 4: CrossSlideConsistencyAuditor (Cross-Slide Factual Contradiction & Visual Rhythm Auditor).
Detects conflicting numbers/metrics across slides, terminology drift, and layout rhythm fatigue.
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
    visual layout fatigue (4+ identical consecutive archetypes), and terminology drift.
    """

    METRIC_REGEXES = [
        # Example: "Doanh thu năm 2024: 1.500 tỷ" or "Tỷ lệ tăng trưởng: 6.8%"
        re.compile(
            r"(?:^|[.\n,;!?])\s*(?P<metric>[^\W\d_][\w\s]{1,35}?(?:\s+năm\s+\d{4})?)\s*[:=–-]\s*(?P<val>\d+(?:[.,]\d+)?\s*(?:%|tỷ|triệu|nghìn|người|USD|VND|km2|MW|GW)?)",
            re.IGNORECASE
        ),
        # Example: "đạt 6.8% tăng trưởng"
        re.compile(
            r"(?:^|[.\n,;!?])\s*(?P<val>\d+(?:[.,]\d+)?\s*(?:%|tỷ|triệu|nghìn|người|USD|VND))\s+(?P<metric>[^\W\d_][\w\s]{2,30})",
            re.IGNORECASE
        )
    ]

    STOP_METRIC_WORDS = {"khoảng", "khoảng chừng", "lên tới", "hơn", "gần", "ước tính", "đạt", "ghi nhận", "là"}

    def __init__(self):
        super().__init__(name="CrossSlideConsistencyAuditor", gate="Gate 2: Macro-Narrative Arc & Consistency")

    def _get_slides(self, target: Any) -> List[Dict[str, Any]]:
        if isinstance(target, list):
            return target
        if isinstance(target, dict):
            return target.get("slides", [target])
        return []

    def _clean_metric_name(self, metric: str) -> str:
        words = [w for w in metric.lower().split() if w not in self.STOP_METRIC_WORDS]
        return " ".join(words).strip()

    def _clean_val(self, val: str) -> str:
        # Standardize number formatting: normalize commas and points
        return val.strip().replace(" ", "").lower()

    def audit(self, target: Any, context: Optional[Dict[str, Any]] = None) -> List[AgentFinding]:
        findings: List[AgentFinding] = []
        slides = self._get_slides(target)

        if not slides:
            return findings

        # ----------------------------------------------------
        # 1. Cross-Slide Metric Contradiction Detector (P0)
        # ----------------------------------------------------
        # Store: metric_key -> List[(slide_id, raw_metric, raw_val, clean_val, raw_evidence)]
        metrics_catalog: Dict[str, List[Tuple[str, str, str, str, str]]] = {}

        for s in slides:
            slide_id = s.get("slide_id", "unknown_slide")
            slide_text = self.extract_slide_text(s)

            for regex in self.METRIC_REGEXES:
                for match in regex.finditer(slide_text):
                    raw_metric = match.group("metric").strip()
                    raw_val = match.group("val").strip()
                    clean_val = self._clean_val(raw_val)
                    clean_metric = self._clean_metric_name(raw_metric)

                    # Only track meaningful metric phrases (length between 3 and 40 chars, not pure numbers)
                    if 3 <= len(clean_metric) <= 40 and not clean_metric.isdigit():
                        if clean_metric not in metrics_catalog:
                            metrics_catalog[clean_metric] = []
                        metrics_catalog[clean_metric].append((slide_id, raw_metric, raw_val, clean_val, match.group(0).strip()))

        # Compare values for identical or near-identical metric keys
        for metric_key, occurrences in metrics_catalog.items():
            if len(occurrences) > 1:
                first_slide, first_raw_m, first_raw_val, first_clean_val, first_ev = occurrences[0]
                for other_slide, other_raw_m, other_raw_val, other_clean_val, other_ev in occurrences[1:]:
                    if first_slide != other_slide and first_clean_val != other_clean_val:
                        # Direct contradiction found!
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
        # 2. Visual Rhythm Fatigue (P2)
        # ----------------------------------------------------
        # 4 or more consecutive slides using the exact same archetype
        consecutive_count = 1
        current_archetype = None
        start_idx = 0

        for idx, s in enumerate(slides):
            arch = s.get("archetype", "default")
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
        """
        Auto-remediates contradictions by harmonizing values to the first canonical instance,
        and diversifying repetitive archetypes.
        """
        remediated = copy.deepcopy(target)
        slides = self._get_slides(remediated)

        for finding in findings:
            # Remediate numeric contradiction
            if finding.severity == Severity.P0 and finding.original_value and finding.suggested_value:
                for s in slides:
                    if s.get("slide_id") == finding.slide_id:
                        # Replace in assertion_title, primary_claim, speaker_notes, atoms
                        if "assertion_title" in s:
                            s["assertion_title"] = s["assertion_title"].replace(finding.original_value, finding.suggested_value)
                        if "primary_claim" in s:
                            s["primary_claim"] = s["primary_claim"].replace(finding.original_value, finding.suggested_value)
                        if "speaker_notes" in s:
                            s["speaker_notes"] = s["speaker_notes"].replace(finding.original_value, finding.suggested_value)
                        for atom in s.get("atoms", []):
                            if isinstance(atom, dict):
                                for k in ["title", "text", "mechanism", "kicker"]:
                                    if k in atom and isinstance(atom[k], str):
                                        atom[k] = atom[k].replace(finding.original_value, finding.suggested_value)

            # Remediate visual rhythm fatigue
            if finding.severity == Severity.P2 and "Visual Rhythm Fatigue" in finding.issue:
                for s in slides:
                    if s.get("slide_id") == finding.slide_id:
                        cur_arch = s.get("archetype")
                        if cur_arch == "3_cards":
                            s["archetype"] = "split_comparison"
                        elif cur_arch == "grid_2x2":
                            s["archetype"] = "process_flow_4"

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            return remediated
        return slides

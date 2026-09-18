"""
scripts/macc_council/gate4_spatial_motion/agent11_layout_archetype.py
Agent 11: LayoutArchetypeStrategist (Spatial Layout & Archetype Fit Auditor).
Ensures chosen layout archetypes structurally match the density and semantics of slide atoms.
Hardened with schema-agnostic counting, semantic intent recognition, and auto-remediation.
"""

from __future__ import annotations

import copy
import re
from typing import Any, Dict, List, Optional
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, Severity


class LayoutArchetypeStrategist(BaseCouncilAgent):
    """
    Agent 11: Layout Archetype Strategist.
    Audits alignment between the selected layout archetype and the atom/card count and semantic intent.
    Prevents spatial collisions, visual vacuums, and mismatched layout structures.
    """

    ARCHETYPE_ATOM_RULES = {
        "title_hero": (0, 0),
        "split_comparison": (2, 2),
        "3_cards": (3, 3),
        "grid_2x2": (4, 4),
        "process_flow_4": (3, 4),
        "process_flow_5": (4, 5),
        "metric_callout_3x": (2, 3),
        "quote_callout": (0, 1),
        "conclusion_cta": (1, 4),
        "table_dense": (4, 12)
    }

    VJ_TO_ARCHETYPE = {
        "HERO_TITLE": "title_hero",
        "BENTO": "split_comparison",
        "BENTO_GRID": "split_comparison",
        "EDITORIAL_HERO": "split_comparison",
        "COMPARISON": "split_comparison",
        "VERSUS": "split_comparison",
        "TWO_PILLARS": "split_comparison",
        "CARDS": "3_cards",
        "PROCESS": "process_flow_4",
        "ROADMAP": "process_flow_4",
        "TIMELINE": "process_flow_4",
        "DATA_TABLE": "table_dense",
        "TABLE": "table_dense",
        "METRIC": "metric_callout_3x",
        "METRIC_HERO": "metric_callout_3x",
    }

    ARCHETYPE_TO_VJ = {
        "title_hero": "HERO_TITLE",
        "split_comparison": "COMPARISON",
        "3_cards": "CARDS",
        "grid_2x2": "CARDS",
        "process_flow_4": "PROCESS",
        "process_flow_5": "PROCESS",
        "metric_callout_3x": "METRIC",
        "quote_callout": "EDITORIAL_HERO",
        "conclusion_cta": "EDITORIAL_HERO",
        "table_dense": "DATA_TABLE"
    }

    PROCESS_KEYWORDS = [
        "quy trình", "tiến trình", "lộ trình", "giai đoạn", "bước",
        "phase", "step", "process", "timeline", "workflow", "nối tiếp"
    ]

    COMPARISON_KEYWORDS = [
        "so sánh", "đối chiếu", "trước và sau", "before and after",
        "before vs after", "versus", "vs", "ưu điểm và nhược điểm", "pros and cons"
    ]

    METRIC_KEYWORDS = [
        "chỉ số", "doanh thu", "lợi nhuận", "kết quả tài chính", "tăng trưởng", "kpi", "metrics"
    ]

    def __init__(self):
        super().__init__(name="LayoutArchetypeStrategist", gate="Gate 4: Spatial Geometry, Typography & Motion")

    def _get_slides(self, target: Any) -> List[Dict[str, Any]]:
        if isinstance(target, list):
            return target
        if isinstance(target, dict):
            return target.get("slides", [target])
        return []

    def _get_item_count(self, s: Dict[str, Any]) -> int:
        for k in ["atoms", "cards", "content_items", "boxes", "items"]:
            items = s.get(k)
            if isinstance(items, list) and len(items) > 0:
                return len(items)
        return 0

    def _recommend_archetype(self, count: int, text: str) -> str:
        lower_text = text.lower()
        is_process = any(k in lower_text for k in self.PROCESS_KEYWORDS)
        is_comparison = any(k in lower_text for k in self.COMPARISON_KEYWORDS)
        is_metric = any(k in lower_text for k in self.METRIC_KEYWORDS)

        if count <= 1:
            return "quote_callout"
        elif count == 2:
            return "split_comparison"
        elif count == 3:
            if is_process:
                return "process_flow_4"
            if is_metric:
                return "metric_callout_3x"
            return "3_cards"
        elif count == 4:
            if is_process:
                return "process_flow_4"
            return "grid_2x2"
        elif count == 5:
            return "process_flow_5"
        return "table_dense"

    def audit(self, target: Any, context: Optional[Dict[str, Any]] = None) -> List[AgentFinding]:
        findings: List[AgentFinding] = []
        slides = self._get_slides(target)

        for s in slides:
            slide_id = s.get("slide_id", "unknown_slide")
            role = s.get("role", "CONTENT").upper()
            if role == "COVER":
                continue

            visual_job = s.get("visual_job", "").upper()
            raw_arch = s.get("archetype")
            archetype = raw_arch or self.VJ_TO_ARCHETYPE.get(visual_job, "3_cards")
            item_count = self._get_item_count(s)
            slide_text = self.extract_slide_text(s)

            # 1. Check atom/card count fit
            if archetype in self.ARCHETYPE_ATOM_RULES:
                min_atoms, max_atoms = self.ARCHETYPE_ATOM_RULES[archetype]
                if visual_job in {"EDITORIAL_HERO", "BENTO", "BENTO_GRID"} and 1 <= item_count <= 3:
                    pass
                elif item_count < min_atoms or item_count > max_atoms:
                    rec_arch = self._recommend_archetype(item_count, slide_text)
                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=slide_id,
                            severity=Severity.P1,
                            issue=f"Bố cục archetype '{archetype}' không tương thích với số lượng atom ({item_count} atoms)",
                            rationale=f"Layout '{archetype}' được thiết kế tối ưu cho {min_atoms}-{max_atoms} thành phần. Với {item_count} atoms sẽ tạo khoảng trống thị giác hoặc gây đè chữ.",
                            suggestion=f"Chuyển đổi sang archetype phù hợp hơn: '{rec_arch}'.",
                            evidence=f"archetype='{archetype}', count={item_count}",
                            original_value=archetype,
                            suggested_value=rec_arch
                        )
                    )
                    continue

            # 2. Check semantic mismatch
            lower_text = slide_text.lower()
            is_process = any(k in lower_text for k in self.PROCESS_KEYWORDS)
            is_comparison = any(k in lower_text for k in self.COMPARISON_KEYWORDS)

            if is_process and archetype == "split_comparison":
                rec_arch = self._recommend_archetype(item_count, slide_text)
                findings.append(
                    AgentFinding(
                        agent=self.name,
                        gate=self.gate,
                        slide_id=slide_id,
                        severity=Severity.P1,
                        issue=f"Archetype '{archetype}' không phù hợp với ngữ nghĩa quy trình/tiến trình tuần tự",
                        rationale="Nội dung diễn giải quy trình/bước tuần tự cần hiển thị theo mạch dòng chảy ngang (Process Flow) thay vì chia đôi so sánh.",
                        suggestion=f"Chuyển đổi sang archetype tiến trình: '{rec_arch}'.",
                        evidence=f"Keywords in text, archetype='{archetype}'",
                        original_value=archetype,
                        suggested_value=rec_arch
                    )
                )
            elif is_comparison and item_count == 2 and archetype != "split_comparison":
                findings.append(
                    AgentFinding(
                        agent=self.name,
                        gate=self.gate,
                        slide_id=slide_id,
                        severity=Severity.P1,
                        issue=f"Nội dung mang ý nghĩa so sánh đối chiếu nhưng dùng archetype '{archetype}'",
                        rationale="Với 2 đối tượng so sánh (trước/sau, phương án A/B), 'split_comparison' tạo đối trọng thị giác trực quan rõ ràng nhất.",
                        suggestion="Chuyển đổi sang archetype 'split_comparison'.",
                        evidence=f"Comparison intent with 2 items in '{archetype}'",
                        original_value=archetype,
                        suggested_value="split_comparison"
                    )
                )

        return findings

    def auto_remediate(self, target: Any, findings: List[AgentFinding], context: Optional[Dict[str, Any]] = None) -> Any:
        remediated = copy.deepcopy(target)
        slides = self._get_slides(remediated)

        for finding in findings:
            if finding.agent == self.name and finding.suggested_value:
                for s in slides:
                    if s.get("slide_id") == finding.slide_id:
                        s["archetype"] = finding.suggested_value
                        if finding.suggested_value in self.ARCHETYPE_TO_VJ:
                            s["visual_job"] = self.ARCHETYPE_TO_VJ[finding.suggested_value]

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            return remediated
        return slides

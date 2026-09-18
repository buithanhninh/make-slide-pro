"""
scripts/macc_council/gate4_spatial_motion/agent11_layout_archetype.py
Agent 11: LayoutArchetypeStrategist (Spatial Layout & Archetype Fit Auditor).
Ensures chosen layout archetypes structurally match the density and semantics of slide atoms.
"""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, Severity


class LayoutArchetypeStrategist(BaseCouncilAgent):
    """
    Agent 11: Layout Archetype Strategist.
    Audits alignment between the selected layout archetype and the atom count / semantic content.
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
        "conclusion_cta": (1, 4)
    }

    def __init__(self):
        super().__init__(name="LayoutArchetypeStrategist", gate="Gate 4: Spatial Geometry, Typography & Motion")

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
            archetype = s.get("archetype", "3_cards")
            atoms = s.get("atoms", [])
            atom_count = len(atoms)

            if archetype in self.ARCHETYPE_ATOM_RULES:
                min_atoms, max_atoms = self.ARCHETYPE_ATOM_RULES[archetype]
                if atom_count < min_atoms or atom_count > max_atoms:
                    # Select recommended archetype
                    rec_arch = self._recommend_archetype(atom_count)
                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=slide_id,
                            severity=Severity.P1,
                            issue=f"Bố cục archetype '{archetype}' không tương thích với số lượng atom ({atom_count} atoms)",
                            rationale=f"Layout '{archetype}' được thiết kế tối ưu cho {min_atoms}-{max_atoms} thành phần. Với {atom_count} atoms sẽ tạo khoảng trống thị giác hoặc gây đè chữ.",
                            suggestion=f"Chuyển đổi sang archetype phù hợp hơn: '{rec_arch}'.",
                            evidence=f"archetype='{archetype}', atom_count={atom_count}",
                            original_value=archetype,
                            suggested_value=rec_arch
                        )
                    )

        return findings

    def _recommend_archetype(self, count: int) -> str:
        if count <= 1:
            return "quote_callout"
        elif count == 2:
            return "split_comparison"
        elif count == 3:
            return "3_cards"
        elif count == 4:
            return "grid_2x2"
        elif count == 5:
            return "process_flow_5"
        return "table_dense"

    def auto_remediate(self, target: Any, findings: List[AgentFinding], context: Optional[Dict[str, Any]] = None) -> Any:
        remediated = copy.deepcopy(target)
        slides = self._get_slides(remediated)

        for finding in findings:
            if finding.original_value and finding.suggested_value:
                for s in slides:
                    if s.get("slide_id") == finding.slide_id:
                        s["archetype"] = finding.suggested_value

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            return remediated
        return slides

"""
scripts/macc_council/gate4_spatial_motion/agent15_motion_choreographer.py
Agent 15: MotionChoreographer (60 FPS Morph Transition & Fluid Animation Auditor).
Audits PowerPoint Morph transitions, shape persistence naming (!!shape_name!!),
and optimal transition timing (0.8s - 1.2s).
"""

from __future__ import annotations

import copy
import re
from typing import Any, Dict, List, Optional
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, Severity


class MotionChoreographer(BaseCouncilAgent):
    """
    Agent 15: Motion Choreographer.
    Audits PowerPoint Morph animations and visual continuity.
    Enforces the strict '!!shape_name!!' naming convention required by PowerPoint
    for seamless 60 FPS shape morphing across adjacent slides.
    """

    def __init__(self):
        super().__init__(name="MotionChoreographer", gate="Gate 4: Spatial Geometry, Typography & Motion")

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
            transition = s.get("transition", "")
            duration = s.get("transition_duration")

            # 1. Transition Duration Check (Optimal 0.6s - 1.5s)
            if duration is not None and isinstance(duration, (int, float)):
                if duration > 2.5:
                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=slide_id,
                            severity=Severity.P2,
                            issue=f"Thời gian chuyển động chuyển cảnh quá chậm ({duration}s > 2.5s)",
                            rationale="Chuyển động quá chậm làm gián đoạn nhịp thuyết trình và tạo cảm giác nặng nề cho người nghe.",
                            suggestion="Đặt thời lượng chuyển động Morph tối ưu trong khoảng 0.8s - 1.2s.",
                            evidence=f"duration={duration}s",
                            original_value=str(duration),
                            suggested_value="1.0"
                        )
                    )
                elif duration < 0.3:
                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=slide_id,
                            severity=Severity.P2,
                            issue=f"Thời gian chuyển động quá ngắn ({duration}s < 0.3s)",
                            rationale="Chuyển động quá nhanh gây chớp mắt giật cục (visual flicker).",
                            suggestion="Đặt thời lượng chuyển động Morph tối ưu 1.0s.",
                            evidence=f"duration={duration}s",
                            original_value=str(duration),
                            suggested_value="1.0"
                        )
                    )

            # 2. PowerPoint Morph Shape Identifier Check
            if transition.lower() == "morph":
                morph_shapes = s.get("morph_shapes", [])
                for shape in morph_shapes:
                    if isinstance(shape, str) and not (shape.startswith("!!") and shape.endswith("!!")):
                        findings.append(
                            AgentFinding(
                                agent=self.name,
                                gate=self.gate,
                                slide_id=slide_id,
                                severity=Severity.P1,
                                issue=f"Tên hình khối Morph không chuẩn quy cách PowerPoint: '{shape}'",
                                rationale="PowerPoint yêu cầu các hình khối morph liên slide bắt buộc phải bắt đầu và kết thúc bằng hai dấu chấm than (!!shape_id!!) để nhận diện biến đổi liên tục 60 FPS.",
                                suggestion=f"Đổi tên hình khối thành '!!{shape.strip('!')}!!'.",
                                evidence=f"shape_name='{shape}'",
                                original_value=shape,
                                suggested_value=f"!!{shape.strip('!')}!!"
                            )
                        )

        return findings

    def auto_remediate(self, target: Any, findings: List[AgentFinding], context: Optional[Dict[str, Any]] = None) -> Any:
        remediated = copy.deepcopy(target)
        slides = self._get_slides(remediated)

        for finding in findings:
            for s in slides:
                if s.get("slide_id") == finding.slide_id:
                    if "Thời gian chuyển động" in finding.issue:
                        s["transition_duration"] = 1.0
                    elif "Tên hình khối Morph" in finding.issue and finding.original_value and finding.suggested_value:
                        morph_shapes = s.get("morph_shapes", [])
                        s["morph_shapes"] = [
                            finding.suggested_value if sh == finding.original_value else sh
                            for sh in morph_shapes
                        ]

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            return remediated
        return slides

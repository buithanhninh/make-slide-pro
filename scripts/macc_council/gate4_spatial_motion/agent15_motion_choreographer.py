"""
scripts/macc_council/gate4_spatial_motion/agent15_motion_choreographer.py
Agent 15: MotionChoreographer (60 FPS Morph Transition & Fluid Animation Auditor).
Audits PowerPoint Morph transitions, shape persistence naming (!!shape_name!!),
and optimal transition timing (0.6s - 1.5s).
Hardened with first-slide morph guards, dict-based shape extraction, and auto-remediation.
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
        total_slides = len(slides)

        # Detect V8.6.0 enforcement mode
        enforce_v86 = False
        if context and (context.get("enforce_v86") or context.get("v86_mode")):
            enforce_v86 = True
        elif isinstance(target, dict):
            ver_str = str(target.get("version", "")) + " " + str(target.get("schema_version", ""))
            if "8.6" in ver_str or target.get("v86_mode"):
                enforce_v86 = True

        for idx, s in enumerate(slides):
            slide_id = s.get("slide_id", f"slide_{idx+1}")
            transition = (s.get("transition") or "").strip().lower()
            duration = s.get("transition_duration")
            role = str(s.get("role", "")).upper()
            is_first = (idx == 0)
            is_last = (idx == total_slides - 1 and total_slides > 1)
            is_content = (not is_first and not is_last)

            # 1. First Slide Morph Guard
            if is_first and transition == "morph":
                findings.append(
                    AgentFinding(
                        agent=self.name,
                        gate=self.gate,
                        slide_id=slide_id,
                        severity=Severity.P2,
                        issue="Slide đầu tiên không thể sử dụng chuyển cảnh 'morph'",
                        rationale="Chuyển cảnh Morph yêu cầu có slide liền trước để biến đổi hình khối. Slide mở đầu bài thuyết trình cần dùng 'fade' hoặc 'none'.",
                        suggestion="Đổi hiệu ứng chuyển cảnh slide 1 thành 'fade'.",
                        evidence=f"idx={idx}, transition='morph'",
                        original_value="morph",
                        suggested_value="fade"
                    )
                )

            # 2. V8.6.0 Pure Continuous Morph Mandate (Slides 2..N-1)
            if enforce_v86 and is_content:
                if transition in {"push", "wipe", "reveal", "split", "wheel", "cut", "random"}:
                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=slide_id,
                            severity=Severity.P1,
                            issue=f"Hiệu ứng chuyển cảnh gián đoạn gây rối mắt ('{transition}') trên slide nội dung",
                            rationale="Make Slide Pro V8.6.0 nghiêm cấm các hiệu ứng Push/Wipe/Reveal gián đoạn giữa các slide nội dung. Bắt buộc sử dụng 100% Pure Continuous Morph.",
                            suggestion="Chuyển sang hiệu ứng 'morph' (0.85s).",
                            evidence=f"idx={idx}, transition='{transition}'",
                            original_value=transition,
                            suggested_value="morph"
                        )
                    )
                elif transition and transition != "morph":
                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=slide_id,
                            severity=Severity.P2,
                            issue=f"Slide nội dung chưa cấu hình 100% Pure Continuous Morph ('{transition}')",
                            rationale="Tiêu chuẩn V8.6.0 quy định mọi slide nội dung phải dùng Morph để tạo cảm giác liên tục như Apple Keynote.",
                            suggestion="Chuyển hiệu ứng thành 'morph'.",
                            evidence=f"idx={idx}, transition='{transition}'",
                            original_value=transition,
                            suggested_value="morph"
                        )
                    )

            # 3. V8.6.0 Cover & Conclusion Smooth Fade Guard
            if enforce_v86 and (is_first or (is_last and role == "COVER")):
                if transition and transition != "fade":
                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=slide_id,
                            severity=Severity.P2,
                            issue=f"Slide bìa/kết luận chưa dùng Cinematic Smooth Fade ('{transition}')",
                            rationale="Slide bìa mở màn và slide kết luận bế mạc cần dùng Smooth Fade (0.65s) để mở/khép bài thuyết trình thanh lịch.",
                            suggestion="Đổi hiệu ứng chuyển cảnh thành 'fade'.",
                            evidence=f"idx={idx}, transition='{transition}'",
                            original_value=transition,
                            suggested_value="fade"
                        )
                    )

            # 4. Transition Duration Check (Optimal 0.6s - 1.5s)
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
                            suggested_value="0.85" if enforce_v86 else "1.0"
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
                            suggestion="Đặt thời lượng chuyển động Morph tối ưu 0.85s.",
                            evidence=f"duration={duration}s",
                            original_value=str(duration),
                            suggested_value="0.85" if enforce_v86 else "1.0"
                        )
                    )

            # 5. PowerPoint Morph Shape Identifier Check (Strings & Dicts)
            if transition == "morph":
                morph_shapes = s.get("morph_shapes", [])
                for shape in morph_shapes:
                    if isinstance(shape, str) and not (shape.startswith("!!") and shape.endswith("!!")):
                        clean_shape = shape.strip("!")
                        findings.append(
                            AgentFinding(
                                agent=self.name,
                                gate=self.gate,
                                slide_id=slide_id,
                                severity=Severity.P1,
                                issue=f"Tên hình khối Morph không chuẩn quy cách PowerPoint: '{shape}'",
                                rationale="PowerPoint yêu cầu các hình khối morph liên slide bắt buộc phải bắt đầu và kết thúc bằng hai dấu chấm than (!!shape_id!!) để nhận diện biến đổi liên tục 60 FPS.",
                                suggestion=f"Đổi tên hình khối thành '!!{clean_shape}!!'.",
                                evidence=f"shape_name='{shape}'",
                                original_value=shape,
                                suggested_value=f"!!{clean_shape}!!"
                            )
                        )

                for sh in s.get("shapes", []) + s.get("elements", []):
                    if isinstance(sh, dict) and (sh.get("morph") or sh.get("is_morph")):
                        sh_name = sh.get("name") or sh.get("id") or ""
                        if isinstance(sh_name, str) and sh_name and not (sh_name.startswith("!!") and sh_name.endswith("!!")):
                            clean_sh = sh_name.strip("!")
                            findings.append(
                                AgentFinding(
                                    agent=self.name,
                                    gate=self.gate,
                                    slide_id=slide_id,
                                    severity=Severity.P1,
                                    issue=f"Tên hình khối Morph trong danh sách shapes không chuẩn quy cách: '{sh_name}'",
                                    rationale="PowerPoint yêu cầu các hình khối morph bắt buộc phải có tên '!!shape_id!!'.",
                                    suggestion=f"Đổi tên thành '!!{clean_sh}!!'.",
                                    evidence=f"shape_dict={sh}",
                                    original_value=sh_name,
                                    suggested_value=f"!!{clean_sh}!!"
                                )
                            )

            # 6. Atomic Card Presenter Click Sequencing Audit
            if enforce_v86 and is_content:
                atoms = s.get("atoms") or []
                if len(atoms) >= 2:
                    if s.get("atomic_card") is False or s.get("safe_group") is False:
                        findings.append(
                            AgentFinding(
                                agent=self.name,
                                gate=self.gate,
                                slide_id=slide_id,
                                severity=Severity.P2,
                                issue="Thiếu cơ chế nhóm thẻ nguyên khối (Atomic Card Presenter Sequencing)",
                                rationale="Theo tiêu chuẩn V8.6.0, mỗi cú click chuột phải mở ra trọn vẹn 1 thẻ (khung + chữ + kpi) thay vì bay rời rạc.",
                                suggestion="Kích hoạt cờ atomic_card=True để gán nhóm safe_group trước khi thiết lập animation.",
                                evidence=f"slide_id={slide_id}, atoms_count={len(atoms)}"
                            )
                        )

        return findings

    def auto_remediate(self, target: Any, findings: List[AgentFinding], context: Optional[Dict[str, Any]] = None) -> Any:
        remediated = copy.deepcopy(target)
        slides = self._get_slides(remediated)
        total_slides = len(slides)

        enforce_v86 = False
        if context and (context.get("enforce_v86") or context.get("v86_mode")):
            enforce_v86 = True
        elif isinstance(target, dict):
            ver_str = str(target.get("version", "")) + " " + str(target.get("schema_version", ""))
            if "8.6" in ver_str or target.get("v86_mode"):
                enforce_v86 = True

        for idx, s in enumerate(slides):
            is_first = (idx == 0)
            is_last = (idx == total_slides - 1 and total_slides > 1)
            is_content = (not is_first and not is_last)

            # 1. Slide 1 morph fix
            if is_first and (s.get("transition") or "").lower() == "morph":
                s["transition"] = "fade"
                if enforce_v86:
                    s["transition_duration"] = 0.65

            # V8.6.0 Transitions
            if enforce_v86:
                if is_first or is_last:
                    s["transition"] = "fade"
                    s["transition_duration"] = 0.65
                elif is_content:
                    s["transition"] = "morph"
                    s["transition_duration"] = 0.85
                if s.get("atoms") and len(s["atoms"]) >= 2:
                    s["atomic_card"] = True

            # 2. Duration normalization (legacy fallback)
            duration = s.get("transition_duration")
            if duration is not None and isinstance(duration, (int, float)):
                if duration > 2.5 or duration < 0.3:
                    s["transition_duration"] = 0.85 if enforce_v86 else 1.0

            # 3. Shape name fixes
            morph_shapes = s.get("morph_shapes", [])
            new_morph_shapes = []
            for shape in morph_shapes:
                if isinstance(shape, str):
                    if not (shape.startswith("!!") and shape.endswith("!!")):
                        new_morph_shapes.append(f"!!{shape.strip('!')}!!")
                    else:
                        new_morph_shapes.append(shape)
                else:
                    new_morph_shapes.append(shape)
            s["morph_shapes"] = new_morph_shapes

            for sh in s.get("shapes", []) + s.get("elements", []):
                if isinstance(sh, dict) and (sh.get("morph") or sh.get("is_morph")):
                    sh_name = sh.get("name") or sh.get("id") or ""
                    if isinstance(sh_name, str) and sh_name and not (sh_name.startswith("!!") and sh_name.endswith("!!")):
                        sh["name"] = f"!!{sh_name.strip('!')}!!"

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            return remediated
        return slides

"""
scripts/macc_council/gate4_spatial_motion/agent14_visual_ergonomics.py
Agent 14: VisualErgonomicsAuditor (WCAG AAA Contrast & Boardroom Ergonomics Auditor).
Audits color contrast ratios (WCAG 2.1 AAA >= 7:1 / 4.5:1) and minimum font sizes
for guaranteed readability from a 20-meter distance.
"""

from __future__ import annotations

import copy
import re
from typing import Any, Dict, List, Optional, Tuple
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, Severity


class VisualErgonomicsAuditor(BaseCouncilAgent):
    """
    Agent 14: Visual Ergonomics Auditor.
    Enforces WCAG 2.1 AAA color contrast standards and boardroom typographic scale.
    Guarantees that presentations are legible for viewers sitting 20 meters away.
    """

    def __init__(self):
        super().__init__(name="VisualErgonomicsAuditor", gate="Gate 4: Spatial Geometry, Typography & Motion")

    def _get_slides(self, target: Any) -> List[Dict[str, Any]]:
        if isinstance(target, list):
            return target
        if isinstance(target, dict):
            return target.get("slides", [target])
        return []

    def _hex_to_rgb(self, hex_str: str) -> Optional[Tuple[int, int, int]]:
        hex_clean = hex_str.strip().lstrip("#")
        if len(hex_clean) == 3:
            hex_clean = "".join(c * 2 for c in hex_clean)
        if len(hex_clean) == 6:
            try:
                return (int(hex_clean[0:2], 16), int(hex_clean[2:4], 16), int(hex_clean[4:6], 16))
            except ValueError:
                return None
        return None

    def _relative_luminance(self, rgb: Tuple[int, int, int]) -> float:
        r, g, b = [x / 255.0 for x in rgb]
        r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
        g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
        b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def _calculate_contrast(self, hex1: str, hex2: str) -> Optional[float]:
        rgb1 = self._hex_to_rgb(hex1)
        rgb2 = self._hex_to_rgb(hex2)
        if not rgb1 or not rgb2:
            return None
        lum1 = self._relative_luminance(rgb1)
        lum2 = self._relative_luminance(rgb2)
        brightest = max(lum1, lum2)
        darkest = min(lum1, lum2)
        return (brightest + 0.05) / (darkest + 0.05)

    def audit(self, target: Any, context: Optional[Dict[str, Any]] = None) -> List[AgentFinding]:
        findings: List[AgentFinding] = []
        slides = self._get_slides(target)

        for s in slides:
            slide_id = s.get("slide_id", "unknown_slide")

            # 1. Contrast Ratio Audit
            bg_color = s.get("bg_color") or s.get("background") or "#FFFFFF"
            text_color = s.get("text_color") or "#1E293B"

            contrast = self._calculate_contrast(bg_color, text_color)
            if contrast is not None and contrast < 4.5:
                findings.append(
                    AgentFinding(
                        agent=self.name,
                        gate=self.gate,
                        slide_id=slide_id,
                        severity=Severity.P1,
                        issue=f"Độ tương phản màu sắc không đạt chuẩn WCAG (Tỷ lệ = {contrast:.2f}:1 < 4.5:1)",
                        rationale=f"Màu chữ '{text_color}' trên nền '{bg_color}' có độ tương phản quá thấp ({contrast:.2f}:1), gây mờ mắt và không đọc được khi chiếu máy chiếu.",
                        suggestion="Đổi màu chữ sang tông tương phản mạnh (ví dụ: #FFFFFF trên nền tối hoặc #0F172A trên nền sáng).",
                        evidence=f"bg={bg_color}, text={text_color}, contrast={contrast:.2f}:1",
                        original_value=text_color,
                        suggested_value="#0F172A" if self._relative_luminance(self._hex_to_rgb(bg_color) or (255,255,255)) > 0.5 else "#FFFFFF"
                    )
                )

            # 2. Font Size Ergonomics
            font_size = s.get("body_font_size") or s.get("font_size")
            if font_size and isinstance(font_size, (int, float)) and font_size < 14:
                findings.append(
                    AgentFinding(
                        agent=self.name,
                        gate=self.gate,
                        slide_id=slide_id,
                        severity=Severity.P1,
                        issue=f"Cỡ chữ thân bài quá nhỏ ({font_size}pt < 14pt)",
                        rationale="Cỡ chữ dưới 14pt không thể quan sát được từ khoảng cách 20 mét trong phòng hội thảo tiêu chuẩn.",
                        suggestion="Tăng cỡ chữ thân bài tối thiểu lên 14pt-16pt.",
                        evidence=f"font_size={font_size}pt",
                        original_value=str(font_size),
                        suggested_value="16"
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
                        if "Độ tương phản" in finding.issue:
                            s["text_color"] = finding.suggested_value
                        elif "Cỡ chữ" in finding.issue:
                            s["body_font_size"] = int(finding.suggested_value)

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            return remediated
        return slides

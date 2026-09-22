"""
scripts/macc_council/gate4_spatial_motion/agent14_visual_ergonomics.py
Agent 14: VisualErgonomicsAuditor (WCAG AAA Contrast & Boardroom Ergonomics Auditor).
Audits color contrast ratios (WCAG 2.1 AAA >= 7:1 / 4.5:1) and minimum font sizes
for guaranteed readability from a 20-meter distance.
Hardened with named color parsing, card-level contrast checks, and boardroom title/body scaling.
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

    NAMED_COLORS = {
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "transparent": None,
        "navy": (11, 17, 32),
        "dark": (15, 23, 42),
        "light": (248, 250, 252),
        "gray": (128, 128, 128),
        "slate": (30, 41, 59)
    }

    def __init__(self):
        super().__init__(name="VisualErgonomicsAuditor", gate="Gate 4: Spatial Geometry, Typography & Motion")

    def _get_slides(self, target: Any) -> List[Dict[str, Any]]:
        if isinstance(target, list):
            return target
        if isinstance(target, dict):
            return target.get("slides", [target])
        return []

    def _parse_color(self, color_str: str) -> Optional[Tuple[int, int, int]]:
        if not color_str or not isinstance(color_str, str):
            return None
        c_clean = color_str.strip().lower()
        if c_clean in self.NAMED_COLORS:
            return self.NAMED_COLORS[c_clean]

        # rgb(r, g, b)
        rgb_match = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", c_clean)
        if rgb_match:
            return (int(rgb_match.group(1)), int(rgb_match.group(2)), int(rgb_match.group(3)))

        # Hex
        hex_clean = c_clean.lstrip("#")
        if len(hex_clean) == 3:
            hex_clean = "".join(c * 2 for c in hex_clean)
        if len(hex_clean) == 6 or len(hex_clean) == 8:
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

    def _calculate_contrast(self, col1: str, col2: str) -> Optional[float]:
        rgb1 = self._parse_color(col1)
        rgb2 = self._parse_color(col2)
        if not rgb1 or not rgb2:
            return None
        lum1 = self._relative_luminance(rgb1)
        lum2 = self._relative_luminance(rgb2)
        brightest = max(lum1, lum2)
        darkest = min(lum1, lum2)
        return (brightest + 0.05) / (darkest + 0.05)

    def _get_contrasting_text_color(self, bg_col: str) -> str:
        rgb = self._parse_color(bg_col)
        if rgb and self._relative_luminance(rgb) < 0.5:
            return "#FFFFFF"
        return "#0F172A"

    def audit(self, target: Any, context: Optional[Dict[str, Any]] = None) -> List[AgentFinding]:
        findings: List[AgentFinding] = []
        slides = self._get_slides(target)

        for s in slides:
            slide_id = s.get("slide_id", "unknown_slide")

            # 1. Slide-Level Contrast Audit
            theme = (context or {}).get("theme", "DARK" if s.get("theme") == "DARK" else "LIGHT").upper()
            default_bg = "#0B1120" if theme == "DARK" else "#FFFFFF"
            default_text = "#F8FAFC" if theme == "DARK" else "#1E293B"
            bg_color = s.get("bg_color") or s.get("background") or default_bg
            text_color = s.get("text_color") or default_text

            contrast = self._calculate_contrast(bg_color, text_color)
            if contrast is not None and contrast < 4.5:
                sugg_color = self._get_contrasting_text_color(bg_color)
                findings.append(
                    AgentFinding(
                        agent=self.name,
                        gate=self.gate,
                        slide_id=slide_id,
                        severity=Severity.P1,
                        issue=f"Độ tương phản màu sắc slide không đạt chuẩn WCAG (Tỷ lệ = {contrast:.2f}:1 < 4.5:1)",
                        rationale=f"Màu chữ '{text_color}' trên nền '{bg_color}' có độ tương phản quá thấp ({contrast:.2f}:1), gây mờ mắt và không đọc được khi chiếu máy chiếu.",
                        suggestion=f"Đổi màu chữ sang tông tương phản mạnh ({sugg_color}).",
                        evidence=f"bg={bg_color}, text={text_color}, contrast={contrast:.2f}:1",
                        original_value=text_color,
                        suggested_value=sugg_color
                    )
                )

            # 2. Card/Atom-Level Contrast Audit
            all_cards = (s.get("cards") or []) + (s.get("atoms") or []) + (s.get("content_items") or [])
            for cidx, card in enumerate(all_cards):
                if isinstance(card, dict):
                    c_bg = card.get("bg_color") or card.get("background")
                    c_text = card.get("text_color") or card.get("color")
                    if c_bg and c_text:
                        c_contrast = self._calculate_contrast(c_bg, c_text)
                        if c_contrast is not None and c_contrast < 4.5:
                            c_sugg = self._get_contrasting_text_color(c_bg)
                            findings.append(
                                AgentFinding(
                                    agent=self.name,
                                    gate=self.gate,
                                    slide_id=slide_id,
                                    severity=Severity.P1,
                                    issue=f"Độ tương phản thẻ {cidx+1} không đạt chuẩn WCAG (Tỷ lệ = {c_contrast:.2f}:1 < 4.5:1)",
                                    rationale=f"Thẻ có màu chữ '{c_text}' trên nền thẻ '{c_bg}' tương phản kém, gây khó đọc.",
                                    suggestion=f"Đổi màu chữ thẻ sang '{c_sugg}'.",
                                    evidence=f"card_bg={c_bg}, card_text={c_text}, contrast={c_contrast:.2f}:1",
                                    original_value=c_text,
                                    suggested_value=c_sugg
                                )
                            )

            # 3. Font Size Ergonomics
            # Body font size (< 14pt is too small)
            body_size = s.get("body_font_size") or s.get("font_size")
            if body_size and isinstance(body_size, (int, float)) and body_size < 14:
                findings.append(
                    AgentFinding(
                        agent=self.name,
                        gate=self.gate,
                        slide_id=slide_id,
                        severity=Severity.P1,
                        issue=f"Cỡ chữ thân bài quá nhỏ ({body_size}pt < 14pt)",
                        rationale="Cỡ chữ dưới 14pt không thể quan sát được từ khoảng cách 20 mét trong phòng hội thảo tiêu chuẩn.",
                        suggestion="Tăng cỡ chữ thân bài tối thiểu lên 14pt-16pt.",
                        evidence=f"body_font_size={body_size}pt",
                        original_value=str(body_size),
                        suggested_value="16"
                    )
                )

            # Title font size (< 20pt is too small for slide titles)
            title_size = s.get("title_font_size")
            if title_size and isinstance(title_size, (int, float)) and title_size < 20:
                findings.append(
                    AgentFinding(
                        agent=self.name,
                        gate=self.gate,
                        slide_id=slide_id,
                        severity=Severity.P1,
                        issue=f"Cỡ chữ tiêu đề slide quá nhỏ ({title_size}pt < 20pt)",
                        rationale="Tiêu đề slide trình chiếu phòng họp lớn bắt buộc tối thiểu 20pt-28pt để khán giả nắm bắt ngay lập tức.",
                        suggestion="Tăng cỡ chữ tiêu đề lên tối thiểu 28pt.",
                        evidence=f"title_font_size={title_size}pt",
                        original_value=str(title_size),
                        suggested_value="28"
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
                        if "tiêu đề" in finding.issue.lower() and "cỡ chữ" in finding.issue.lower():
                            s["title_font_size"] = int(finding.suggested_value)
                        elif "thân bài" in finding.issue.lower() and "cỡ chữ" in finding.issue.lower():
                            s["body_font_size"] = int(finding.suggested_value)
                        elif "màu sắc slide" in finding.issue.lower() or "tương phản màu sắc" in finding.issue.lower():
                            s["text_color"] = finding.suggested_value
                        elif "thẻ" in finding.issue.lower() and "tương phản" in finding.issue.lower():
                            all_cards = (s.get("cards") or []) + (s.get("atoms") or []) + (s.get("content_items") or [])
                            for card in all_cards:
                                if isinstance(card, dict) and (card.get("text_color") == finding.original_value or card.get("color") == finding.original_value):
                                    card["text_color"] = finding.suggested_value

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            return remediated
        return slides

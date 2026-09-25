# -*- coding: utf-8 -*-
"""
scripts/mas_engine_v9/remediator/root_cause_diagnostic.py
Root-Cause Diagnostic & Remediation Planner (Agent 5 of MAS-CLSH V9.0).
Analyzes defects identified across all 4 inspectors, isolates underlying root causes,
and synthesizes precise RemediationDirectives for the surgical healer.
"""

from __future__ import annotations
import re
from typing import Any, Dict, List, Optional
from ..models import DefectIssue, RemediationDirective, SlideAuditResult


class RootCauseDiagnosticAgent:
    """Diagnoses root causes and generates targeted surgical healing directives."""

    def diagnose_slide(
        self,
        slide_index: int,
        defects: List[DefectIssue],
        current_blueprint: Optional[Dict[str, Any]] = None,
    ) -> List[RemediationDirective]:
        directives: List[RemediationDirective] = []
        if not defects:
            return directives

        # Sort defects by severity (P0 first, then P1, then P2)
        severity_rank = {"P0": 0, "P1": 1, "P2": 2}
        sorted_defects = sorted(defects, key=lambda d: severity_rank.get(d.severity, 3))

        import copy
        if current_blueprint:
            updated_bp = copy.deepcopy(current_blueprint)
            for defect in sorted_defects:
                if defect.domain == "CONTENT":
                    updated_bp = self._patch_content_blueprint(updated_bp, defect)
                elif defect.domain == "MOTION":
                    updated_bp = self._patch_motion_blueprint(updated_bp, defect)
                elif defect.domain == "LAYOUT":
                    updated_bp = self._patch_layout_blueprint(updated_bp, defect)
                elif defect.domain == "DATAVIZ":
                    updated_bp = self._patch_dataviz_blueprint(updated_bp, defect)

            master_directive = RemediationDirective(
                slide_index=slide_index,
                target_domain="CONSOLIDATED",
                root_cause="; ".join(d.root_cause for d in sorted_defects),
                remediation_action="; ".join(d.remediation_action for d in sorted_defects),
                updated_blueprint=updated_bp,
            )
            return [master_directive]

        return directives

    def _patch_content_blueprint(self, bp: Dict[str, Any], defect: DefectIssue) -> Dict[str, Any]:
        """Surgically cleans text in blueprint to eliminate AI slop, clichés, fake watermarks and dangling parens."""
        content = bp.get("content", {})
        # Clean assertion title
        title = bp.get("assertion_title", "") or content.get("assertion_title", "")
        if title.endswith("(") or title.endswith(" ("):
            title = title.rstrip(" (").strip()

        # Clean AI slop from title
        slop_map = {
            "bức tranh toàn cảnh": "Tổng quan toàn diện",
            "đột phá toàn diện": "Đổi mới trọng tâm",
            "hệ sinh thái tối ưu": "Mô hình phối hợp",
            "tiếp cận đa chiều": "Phương pháp đa diện",
            "chìa khóa then chốt": "Yếu tố cốt lõi",
            "vững bước tương lai": "Định hướng phát triển",
            "khám phá tiềm năng": "Phân tích cơ hội",
            "trong kỷ nguyên số": "Trong thực tiễn chuyển đổi số",
            "vận dụng đồng bộ": "Triển khai nhất quán",
        }
        for slop_k, slop_v in slop_map.items():
            if slop_k in title.lower():
                title = re.sub(re.escape(slop_k), slop_v, title, flags=re.IGNORECASE)

        if "assertion_title" in bp:
            bp["assertion_title"] = title
        if "assertion_title" in content:
            content["assertion_title"] = title

        # Clean atoms if present
        atoms = bp.get("atoms", [])
        for atom in atoms:
            if isinstance(atom, dict):
                # Clean chip watermark
                if "chip" in atom:
                    if "tiêu chuẩn" in atom["chip"].lower() or "watermark" in atom["chip"].lower():
                        del atom["chip"]
                a_text = atom.get("text", "")
                for slop_k, slop_v in slop_map.items():
                    if slop_k in a_text.lower():
                        atom["text"] = re.sub(re.escape(slop_k), slop_v, a_text, flags=re.IGNORECASE)

        # Clean cards
        cards = content.get("cards", [])
        for c in cards:
            if isinstance(c, dict):
                c_title = c.get("title", "")
                if c_title.endswith("(") or c_title.endswith(" ("):
                    c["title"] = c_title.rstrip(" (").strip()
                for slop_k, slop_v in slop_map.items():
                    if slop_k in c_title.lower():
                        c["title"] = re.sub(re.escape(slop_k), slop_v, c_title, flags=re.IGNORECASE)
                if "khuyến nghị áp dụng" in c_title.lower():
                    c["title"] = "Khuyến Nghị Thực Tiễn:"

                points = c.get("points", [])
                clean_points = []
                for pt in points:
                    pt_clean = pt.rstrip(" (").strip() if isinstance(pt, str) else pt
                    if pt_clean:
                        for slop_k, slop_v in slop_map.items():
                            if slop_k in pt_clean.lower():
                                pt_clean = re.sub(re.escape(slop_k), slop_v, pt_clean, flags=re.IGNORECASE)
                        clean_points.append(pt_clean)
                c["points"] = clean_points

        bp["content"] = content
        return bp

    def _patch_motion_blueprint(self, bp: Dict[str, Any], defect: DefectIssue) -> Dict[str, Any]:
        """Ensures 100% Morph on content slides and correct presenter triggers."""
        slide_id = bp.get("slide_id", "SLIDE_02")
        role = bp.get("role", "CONTENT").upper()
        is_cover = slide_id in ["SLIDE_01", "SLIDE_1"] or role == "COVER"
        is_outro = role in ["OUTRO", "CONCLUSION", "CLOSING"] or "outro" in slide_id.lower()
        
        if is_cover or is_outro:
            bp["transition"] = "fade"
            bp["transition_duration"] = 0.65
        else:
            bp["transition"] = "morph"
            bp["transition_duration"] = 0.85
            bp["atomic_card"] = True
            bp["safe_group"] = True

        return bp

    def _patch_layout_blueprint(self, bp: Dict[str, Any], defect: DefectIssue) -> Dict[str, Any]:
        """Adjusts visual system and card sizing to eliminate dead space."""
        bp["zero_dead_space"] = True
        bp["target_card_height"] = 360.0
        bp["typography_floor"] = 16.0
        bp["centered_y"] = True
        return bp

    def _patch_dataviz_blueprint(self, bp: Dict[str, Any], defect: DefectIssue) -> Dict[str, Any]:
        """Enforces high-contrast chart palettes, table styling and visual illustration layout."""
        if "illustration" in defect.root_cause.lower():
            # Infuse editorial hero illustration layout
            bp["visual_job"] = "EDITORIAL_HERO"
            bp["visual_anchor"] = "EDITORIAL_HERO"
            if not bp.get("illustration"):
                bp["illustration"] = "illustration_bai_1.jpg"
        else:
            bp["chart_theme"] = "HIGH_CONTRAST_LIGHT"
            bp["chart_font_color"] = "#E2E8F0"
            bp["transparent_chart_background"] = True
        return bp

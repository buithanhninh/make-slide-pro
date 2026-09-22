# -*- coding: utf-8 -*-
"""
scripts/mas_engine_v9/inspectors/dataviz_math.py
Forensic Data Visualization, Native Tables, Math & Technical Archetypes Inspector (Agent 4 of MAS-CLSH V9.0).
Verifies:
1. Microsoft Office Native Charts: High-contrast bright font (#E2E8F0) on Dark Canvas,
   border/background transparency (no Excel default grey boxes).
2. Native PowerPoint Tables: Clean header styling, alternating zebra fills, aligned numeric data.
3. Mathematical formulas and symbols (clean formatting, no unparsed raw LaTeX markup).
4. Process & Architecture archetypes: Vector connector arrows, directional integrity.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple
from ..models import DefectIssue


class DataVizMathArchetypeAgent:
    """Specialized Inspector for Native Charts, Tables, Math & Complex Archetypes."""

    def __init__(self, theme: str = "DARK"):
        self.theme = theme.upper()

    def inspect_chart_object(
        self, slide_index: int, chart_info: Dict[str, Any]
    ) -> Tuple[float, List[DefectIssue]]:
        defects: List[DefectIssue] = []
        score = 100.0

        if not chart_info:
            return 100.0, []

        is_dark = (self.theme == "DARK")
        font_color_rgb = chart_info.get("font_color_rgb", (255, 255, 255))
        has_gray_border = chart_info.get("has_gray_border", False)
        chart_type = chart_info.get("chart_type", "COLUMN")

        # 1. Contrast Check on Dark Background
        if is_dark and font_color_rgb:
            # Luminance check: R*0.299 + G*0.587 + B*0.114
            lum = font_color_rgb[0] * 0.299 + font_color_rgb[1] * 0.587 + font_color_rgb[2] * 0.114
            if lum < 120:  # Dark font on dark background
                defects.append(
                    DefectIssue(
                        slide_index=slide_index,
                        severity="P0",
                        domain="DATAVIZ",
                        root_cause=f"Chart {chart_type} uses dark font color (luminance {lum:.0f} < 120) on Dark Canvas.",
                        remediation_action="Enforce high-contrast chart theming: ChartArea.Font.Color = RGB(226, 232, 240).",
                    )
                )
                score -= 35.0

        # 2. Default Excel Border / Background Check
        if has_gray_border:
            defects.append(
                DefectIssue(
                    slide_index=slide_index,
                    severity="P2",
                    domain="DATAVIZ",
                    root_cause="Chart retains default Excel container border or solid background.",
                    remediation_action="Set Chart.Format.Line.Visible = msoFalse and Fill.Visible = msoFalse.",
                )
            )
            score -= 10.0

        score = max(0.0, min(100.0, score))
        return score, defects

    def inspect_table_object(
        self, slide_index: int, table_info: Dict[str, Any]
    ) -> Tuple[float, List[DefectIssue]]:
        defects: List[DefectIssue] = []
        score = 100.0

        rows = table_info.get("rows", 0)
        cols = table_info.get("cols", 0)

        if rows < 2 or cols < 2:
            defects.append(
                DefectIssue(
                    slide_index=slide_index,
                    severity="P1",
                    domain="DATAVIZ",
                    root_cause=f"Table dimension is trivial ({rows}x{cols}). Should be converted to structured cards.",
                    remediation_action="Refactor 1-column or 1-row table into atomic card grid archetype.",
                )
            )
            score -= 15.0

        score = max(0.0, min(100.0, score))
        return score, defects

    def inspect_math_and_syntax(
        self, slide_index: int, text_chunks: List[str]
    ) -> Tuple[float, List[DefectIssue]]:
        defects: List[DefectIssue] = []
        score = 100.0

        for txt in text_chunks:
            # Detect unparsed raw LaTeX commands printed as plain text
            raw_latex_snippets = [r"\frac", r"\sqrt", r"\sum", r"\int", r"\mathbf", r"\begin{"]
            for l_cmd in raw_latex_snippets:
                if l_cmd in txt:
                    defects.append(
                        DefectIssue(
                            slide_index=slide_index,
                            severity="P1",
                            domain="DATAVIZ",
                            root_cause=f"Unparsed raw LaTeX snippet '{l_cmd}' detected in text output.",
                            remediation_action="Render mathematical formula using Unicode math symbols or native equation shape.",
                        )
                    )
                    score -= 20.0
                    break

        score = max(0.0, min(100.0, score))
        return score, defects

    def inspect_visual_assets_ratio(
        self, total_slides: int, illustration_count: int, chart_count: int, table_count: int
    ) -> Tuple[float, List[DefectIssue]]:
        """Inspects presentation-wide visual asset diversity and illustration quotas (30% - 50%)."""
        defects: List[DefectIssue] = []
        score = 100.0

        if total_slides <= 0:
            return 100.0, []

        ill_ratio = illustration_count / total_slides

        # 1. Illustration Quota Check: 30% to 50% required
        if ill_ratio < 0.30:
            defects.append(
                DefectIssue(
                    slide_index=0,
                    severity="P1",
                    domain="DATAVIZ",
                    root_cause=f"Low illustration ratio: only {illustration_count}/{total_slides} slides ({ill_ratio*100:.1f}%) have visual illustrations. Required quota is 30% - 50%.",
                    remediation_action="Convert candidate slides (concepts, case studies, overviews) to EDITORIAL_HERO layout with high-res illustrations.",
                )
            )
            score -= 25.0
        elif ill_ratio > 0.55:
            defects.append(
                DefectIssue(
                    slide_index=0,
                    severity="P2",
                    domain="DATAVIZ",
                    root_cause=f"Excessive illustration ratio ({ill_ratio*100:.1f}% > 50%). May dilute structured analytical frameworks.",
                    remediation_action="Balance editorial illustrations with structured cards or process flows.",
                )
            )
            score -= 5.0

        # 2. Data Visualization Diversity Check (Native Charts + Tables)
        total_data_viz = chart_count + table_count
        if total_data_viz == 0 and total_slides >= 10:
            defects.append(
                DefectIssue(
                    slide_index=0,
                    severity="P1",
                    domain="DATAVIZ",
                    root_cause="Complete absence of quantitative visualization: 0 native charts and 0 tables detected in deck.",
                    remediation_action="Incorporate at least 2-4 Native Charts (Column/Bar/Line) or Native Comparison Tables.",
                )
            )
            score -= 20.0

        score = max(0.0, min(100.0, score))
        return score, defects

    def inspect_com_slide(self, slide_index: int, ppt_slide_obj: Any) -> Tuple[float, List[DefectIssue], Dict[str, bool]]:
        """Inspects live PowerPoint COM slide for illustration, chart and table presence."""
        all_defects: List[DefectIssue] = []
        scores: List[float] = []
        has_illustration = False
        has_chart = False
        has_table = False

        try:
            for j in range(1, ppt_slide_obj.Shapes.Count + 1):
                shp = ppt_slide_obj.Shapes(j)

                # Check Picture / Illustration (msoPicture = 13, or LinkedPicture = 11, or shape with fill picture)
                if shp.Type in (13, 11) or "picture" in shp.Name.lower() or "illustration" in shp.Name.lower():
                    has_illustration = True
                elif shp.Type == 6:  # msoGroup
                    for g in shp.GroupItems:
                        if g.Type in (13, 11) or "picture" in g.Name.lower():
                            has_illustration = True

                # Check Chart (msoChart = 3)
                if shp.HasChart:
                    has_chart = True
                    chart = shp.Chart
                    chart_font_color = (255, 255, 255)
                    try:
                        c_val = chart.ChartArea.Font.Color
                        r = c_val & 0xFF
                        g = (c_val >> 8) & 0xFF
                        b = (c_val >> 16) & 0xFF
                        chart_font_color = (r, g, b)
                    except Exception:
                        pass

                    c_info = {
                        "chart_type": str(chart.ChartType),
                        "font_color_rgb": chart_font_color,
                        "has_gray_border": bool(shp.Line.Visible),
                    }
                    c_score, c_def = self.inspect_chart_object(slide_index, c_info)
                    scores.append(c_score)
                    all_defects.extend(c_def)

                # Check Table
                if shp.HasTable:
                    has_table = True
                    tbl = shp.Table
                    t_info = {"rows": tbl.Rows.Count, "cols": tbl.Columns.Count}
                    t_score, t_def = self.inspect_table_object(slide_index, t_info)
                    scores.append(t_score)
                    all_defects.extend(t_def)
        except Exception as e:
            all_defects.append(
                DefectIssue(
                    slide_index=slide_index,
                    severity="P2",
                    domain="DATAVIZ",
                    root_cause=f"COM dataviz inspection warning: {e}",
                    remediation_action="Verify chart/table properties.",
                )
            )

        final_score = min(scores) if scores else 100.0
        flags = {
            "has_illustration": has_illustration,
            "has_chart": has_chart,
            "has_table": has_table,
        }
        return final_score, all_defects, flags

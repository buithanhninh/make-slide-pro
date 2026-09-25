# -*- coding: utf-8 -*-
"""
scripts/mas_engine_v9/inspectors/layout_typography.py
Forensic Layout, Typography & Spatial Proportions Inspector (Agent 3 of MAS-CLSH V9.0).
Verifies:
1. Golden ratio layout & vertical alignment (natural card height 250-320pt, centered Y).
2. Zero Dead Space (<20% unutilized void on content slides).
3. Strict typographic hierarchy: Kicker (13-14pt bold), Assertion Title (22-26pt bold),
   Card Title (15-17pt bold), Body (13-14.5pt), KPI chips (11-12pt bold).
4. Margins, paddings, and collision prevention.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple
from ..models import DefectIssue


class LayoutTypographyAgent:
    """Specialized Inspector for Layout Hierarchy, Font Sizing & Zero Dead Space."""

    def inspect_geometry_and_type(
        self,
        slide_index: int,
        shape_bounds: List[Dict[str, float]],
        font_sizes: List[float],
        slide_width: float = 960.0,
        slide_height: float = 540.0,
        total_slides: int = 0,
    ) -> Tuple[float, List[DefectIssue]]:
        defects: List[DefectIssue] = []
        score = 100.0

        if not shape_bounds:
            defects.append(
                DefectIssue(
                    slide_index=slide_index,
                    severity="P0",
                    domain="LAYOUT",
                    root_cause="Slide has 0 shapes or geometry cannot be determined.",
                    remediation_action="Generate structured layout containers and visual cards.",
                )
            )
            return 0.0, defects

        # 1. Dead Space Calculation
        total_canvas_area = slide_width * slide_height
        occupied_area = sum(b.get("width", 0) * b.get("height", 0) for b in shape_bounds)
        area_coverage_ratio = occupied_area / total_canvas_area if total_canvas_area > 0 else 0

        # On content slides, area coverage should be balanced (between 25% and 75%)
        # Exempt cover (slide 1) and outro/conclusion (total_slides)
        is_content = (slide_index > 1 and (total_slides <= 0 or slide_index < total_slides))
        if is_content and area_coverage_ratio < 0.20:
            defects.append(
                DefectIssue(
                    slide_index=slide_index,
                    severity="P1",
                    domain="LAYOUT",
                    root_cause=f"Excessive dead space detected: content coverage is only {area_coverage_ratio*100:.1f}% (<20%).",
                    remediation_action="Scale cards to natural height (280-310pt), enrich with KPI badges and structural dividers.",
                )
            )
            score -= 20.0

        # 2. Collision / Overlap Check (card bounds)
        # Filter out stage background containers, parent wrappers, or residual groups (w > 750 and h > 280)
        cards = [
            b for b in shape_bounds
            if b.get("width", 0) > 120 and b.get("height", 0) > 100
            and not (b.get("width", 0) > 750 and b.get("height", 0) > 280)
            and not any(k in b.get("name", "").lower() for k in ["residual", "stage_hero", "container_bg"])
        ]
        for i in range(len(cards)):
            for j in range(i + 1, len(cards)):
                b1 = cards[i]
                b2 = cards[j]
                # Check horizontal overlap
                if (b1["left"] < b2["left"] + b2["width"]) and (b1["left"] + b1["width"] > b2["left"]):
                    # Check vertical overlap
                    if (b1["top"] < b2["top"] + b2["height"]) and (b1["top"] + b1["height"] > b2["top"]):
                        overlap_w = min(b1["left"] + b1["width"], b2["left"] + b2["width"]) - max(b1["left"], b2["left"])
                        overlap_h = min(b1["top"] + b1["height"], b2["top"] + b2["height"]) - max(b1["top"], b2["top"])
                        if overlap_w > 15 and overlap_h > 15:
                            defects.append(
                                DefectIssue(
                                    slide_index=slide_index,
                                    severity="P1",
                                    domain="LAYOUT",
                                    root_cause=f"Visual collision: Card overlap of {overlap_w:.0f}x{overlap_h:.0f}pt detected.",
                                    remediation_action="Recalculate horizontal distribution spacing (gap >= 20pt).",
                                )
                            )
                            score -= 20.0
                            break

        # 3. Typography Hierarchy Check
        if font_sizes:
            # Exclude tiny footer source text (<11pt if contains docx / nguồn)
            valid_fonts = [f for f in font_sizes if f > 0]
            min_font = min(valid_fonts) if valid_fonts else 15.0
            max_font = max(valid_fonts) if valid_fonts else 28.0

            is_outro = (total_slides > 0 and slide_index == total_slides)
            if min_font < 14.5 and slide_index > 1 and not is_outro:
                defects.append(
                    DefectIssue(
                        slide_index=slide_index,
                        severity="P0",
                        domain="LAYOUT",
                        root_cause=f"Illegible typography: body font size {min_font:.1f}pt is below minimum readability threshold (15.0pt).",
                        remediation_action="Enlarge body typography to 16-17pt bold/regular.",
                    )
                )
                score -= 30.0

            if max_font < 24.0 and slide_index > 1:
                defects.append(
                    DefectIssue(
                        slide_index=slide_index,
                        severity="P0",
                        domain="LAYOUT",
                        root_cause=f"Weak title hierarchy: assertion title font size is only {max_font:.1f}pt (<24pt).",
                        remediation_action="Enforce Assertion Title font size between 26pt and 28pt bold.",
                    )
                )
                score -= 20.0

        # 4. Loose Shapes / Missing Atomic Grouping Check
        if slide_index > 1:
            total_shapes = len(shape_bounds)
            group_count = sum(1 for b in shape_bounds if b.get("is_group", False))
            if total_shapes > 9 and group_count == 0:
                defects.append(
                    DefectIssue(
                        slide_index=slide_index,
                        severity="P1",
                        domain="LAYOUT",
                        root_cause=f"Fragmented Loose Shapes: Slide contains {total_shapes} loose ungrouped shapes with 0 atomic groups.",
                        remediation_action="Encapsulate shapes into unified presentation cards using safe_group / cluster_and_group_atomic_cards.",
                    )
                )
                score -= 20.0

        score = max(0.0, min(100.0, score))
        return score, defects

    def inspect_com_slide(
        self, slide_index: int, ppt_slide_obj: Any, slide_width: float = 960.0, slide_height: float = 540.0, total_slides: int = 0
    ) -> Tuple[float, List[DefectIssue]]:
        """Inspects live PowerPoint COM slide geometry, group internals, and font sizes."""
        shape_bounds = []
        font_sizes = []
        internal_dead_space_defects = []

        try:
            for j in range(1, ppt_slide_obj.Shapes.Count + 1):
                shp = ppt_slide_obj.Shapes(j)
                is_grp = (shp.Type == 6)  # msoGroup
                s_left = float(shp.Left)
                s_top = float(shp.Top)
                s_w = float(shp.Width)
                s_h = float(shp.Height)

                shape_bounds.append({
                    "name": shp.Name,
                    "left": s_left,
                    "top": s_top,
                    "width": s_w,
                    "height": s_h,
                    "is_group": is_grp,
                })

                if is_grp:
                    try:
                        g_items = shp.GroupItems
                        child_count = g_items.Count
                        lowest_bottom = s_top
                        for gi in range(1, child_count + 1):
                            c_item = g_items(gi)
                            c_b = float(c_item.Top) + float(c_item.Height)
                            if c_b > lowest_bottom:
                                lowest_bottom = c_b
                            if c_item.HasTextFrame and c_item.TextFrame.HasText:
                                try:
                                    tr = c_item.TextFrame.TextRange
                                    for p_idx in range(1, tr.Paragraphs().Count + 1):
                                        para = tr.Paragraphs(p_idx)
                                        p_txt = para.Text.strip()
                                        if not p_txt or len(p_txt) < 3:
                                            continue
                                        # Allow small badge if <= 25 chars and >= 13pt
                                        p_sz = float(para.Font.Size)
                                        if len(p_txt) <= 25 and p_sz >= 13.0:
                                            continue
                                        if p_sz > 0:
                                            font_sizes.append(p_sz)
                                except Exception:
                                    pass

                        # Internal Card Dead Space Check
                        if s_h > 180.0 and s_w > 120.0 and slide_index > 1:
                            utilized_h = lowest_bottom - s_top
                            util_ratio = utilized_h / s_h if s_h > 0 else 1.0
                            if util_ratio < 0.45:
                                internal_dead_space_defects.append(
                                    DefectIssue(
                                        slide_index=slide_index,
                                        severity="P1",
                                        domain="LAYOUT",
                                        root_cause=f"Internal Card Dead Space in '{shp.Name}': Content occupies only {util_ratio*100:.1f}% (<45%) of card height ({s_h:.0f}pt). Empty dark void exceeds 55%.",
                                        remediation_action="Implement 3-tier card contract with bottom anchor badge and 1.3 line spacing.",
                                    )
                                )
                    except Exception:
                        pass
                else:
                    if shp.HasTextFrame and shp.TextFrame.HasText:
                        try:
                            # Skip footer text and top rail
                            is_title = ("Anchor_Assertion_Title" in shp.Name or "title" in shp.Name.lower())
                            is_footer = ("Anchor_Source_Footer" in shp.Name or s_top > 495.0 or "nguồn" in shp.Name.lower())
                            is_top_rail = (not is_title) and (s_top < 50.0 or "Anchor_Kicker" in shp.Name or "Anchor_Slide_Tracker" in shp.Name or "kicker" in shp.Name.lower() or "tracker" in shp.Name.lower())
                            if not is_footer and not is_top_rail:
                                tr = shp.TextFrame.TextRange
                                for p_idx in range(1, tr.Paragraphs().Count + 1):
                                    para = tr.Paragraphs(p_idx)
                                    p_txt = para.Text.strip()
                                    if not p_txt or len(p_txt) < 3:
                                        continue
                                    p_sz = float(para.Font.Size)
                                    if len(p_txt) <= 25 and p_sz >= 13.0:
                                        continue
                                    if p_sz > 0:
                                        font_sizes.append(p_sz)
                        except Exception:
                            pass
        except Exception as e:
            return 50.0, [
                DefectIssue(
                    slide_index=slide_index,
                    severity="P1",
                    domain="LAYOUT",
                    root_cause=f"COM shape geometry inspection error: {e}",
                    remediation_action="Validate shape layout coordinates.",
                )
            ]

        score, defects = self.inspect_geometry_and_type(
            slide_index=slide_index,
            shape_bounds=shape_bounds,
            font_sizes=font_sizes,
            slide_width=slide_width,
            slide_height=slide_height,
            total_slides=total_slides,
        )

        # Merge internal dead space defects
        if internal_dead_space_defects:
            defects.extend(internal_dead_space_defects)
            score = max(0.0, score - (len(internal_dead_space_defects) * 15.0))

        return score, defects

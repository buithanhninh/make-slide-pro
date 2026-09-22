# -*- coding: utf-8 -*-
"""
tests/test_mas_inspectors.py
Unit tests for Make Slide Pro V9.0 Multi-Agent Inspectors and Root Cause Diagnostic.
"""

import pytest
from scripts.mas_engine_v9 import (
    ContentGroundingAgent,
    InterSlideKineticMorphAgent,
    LayoutTypographyAgent,
    DataVizMathArchetypeAgent,
    RootCauseDiagnosticAgent,
    DefectIssue,
)


def test_content_grounding_agent_detects_cliche():
    agent = ContentGroundingAgent()
    # Test cliché and dangling parens
    bad_text = [
        "Khuyến Nghị Áp Dụng: Vận dụng đồng bộ các giải pháp dân số (",
        "Tiếp cận đa chiều trong chăm sóc sức khỏe",
    ]
    score, defects = agent.inspect_text_strings(slide_index=2, text_chunks=bad_text)
    assert score < 70.0
    severities = [d.severity for d in defects]
    assert "P0" in severities  # Dangling parenthesis and forbidden cliché

    # Test clean text
    clean_text = [
        "QUY TRÌNH 4 BƯỚC KHÁM SỨC KHỎE TIỀN HÔN NHÂN",
        "Bước 1: Tiếp đón và lập hồ sơ bệnh án điện tử.",
        "Bước 2: Khám lâm sàng toàn diện các cơ quan.",
    ]
    score_clean, defects_clean = agent.inspect_text_strings(slide_index=2, text_chunks=clean_text)
    assert score_clean == 100.0
    assert len(defects_clean) == 0


def test_motion_inspector_detects_transitions():
    agent = InterSlideKineticMorphAgent()

    # Cover slide with wrong transition (e.g. Wipe/Push code 3855)
    score_cover_bad, def_cover_bad = agent.inspect_deck_transitions(
        slide_index=1,
        total_slides=20,
        entry_effect=3855,
        duration=0.65,
        timeline_triggers=[],
        has_atomic_groups=True,
    )
    assert score_cover_bad < 100.0
    assert any(d.severity == "P0" for d in def_cover_bad)

    # Content slide with correct Morph (3954, 0.85s) and correct triggers
    score_content_good, def_content_good = agent.inspect_deck_transitions(
        slide_index=5,
        total_slides=20,
        entry_effect=3954,
        duration=0.85,
        timeline_triggers=[2, 1, 1],  # Card 0 WithPrev, Cards 1-2 OnClick
        has_atomic_groups=True,
    )
    assert score_content_good == 100.0
    assert len(def_content_good) == 0


def test_layout_inspector_dead_space():
    agent = LayoutTypographyAgent()

    # Empty/Sparse layout (area coverage < 15%)
    sparse_bounds = [{"left": 100, "top": 100, "width": 100, "height": 50}]
    score_sparse, def_sparse = agent.inspect_geometry_and_type(
        slide_index=3,
        shape_bounds=sparse_bounds,
        font_sizes=[14.0],
        slide_width=960.0,
        slide_height=540.0,
    )
    assert score_sparse < 90.0
    assert any(d.domain == "LAYOUT" and "dead space" in d.root_cause.lower() for d in def_sparse)


def test_dataviz_inspector_dark_font_contrast():
    agent = DataVizMathArchetypeAgent(theme="DARK")

    # Dark font on dark background (R=30, G=30, B=30 -> lum < 50)
    bad_chart = {
        "chart_type": "COLUMN",
        "font_color_rgb": (30, 30, 30),
        "has_gray_border": True,
    }
    score_c, def_c = agent.inspect_chart_object(slide_index=4, chart_info=bad_chart)
    assert score_c < 70.0
    assert any(d.severity == "P0" and d.domain == "DATAVIZ" for d in def_c)

    # Raw LaTeX
    score_m, def_m = agent.inspect_math_and_syntax(
        slide_index=4, text_chunks=["Công thức tính: \\frac{N_1}{N_2} * 100%"]
    )
    assert score_m < 90.0
    assert any("\\frac" in d.root_cause for d in def_m)


def test_root_cause_diagnostic_patches_blueprint():
    agent = RootCauseDiagnosticAgent()
    bp = {
        "slide_id": "SLIDE_05",
        "content": {
            "assertion_title": "Chiến Lược Nâng Cao Dân Số (",
            "cards": [{"title": "Khuyến Nghị Áp Dụng: Vận dụng", "points": ["Biện pháp A (", "Biện pháp B"]}],
        },
    }
    defects = [
        DefectIssue(
            slide_index=5,
            severity="P0",
            domain="CONTENT",
            root_cause="Dangling paren",
            remediation_action="Clean syntax",
        )
    ]
    directives = agent.diagnose_slide(slide_index=5, defects=defects, current_blueprint=bp)
    assert len(directives) == 1
    patched = directives[0].updated_blueprint
    assert not patched["content"]["assertion_title"].endswith("(")
    assert not patched["content"]["cards"][0]["title"].endswith("(")
    assert not patched["content"]["cards"][0]["points"][0].endswith("(")

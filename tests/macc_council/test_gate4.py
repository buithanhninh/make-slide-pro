"""
tests/macc_council/test_gate4.py
Adversarial Unit Tests for Gate 4: Spatial Geometry, Typography & Motion
Tests Agents 11 through 15.
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from scripts.macc_council.gate4_spatial_motion import (
    LayoutArchetypeStrategist,
    DataChartCartographer,
    TypographyWidowOrphanSentinel,
    VisualErgonomicsAuditor,
    MotionChoreographer
)
from scripts.macc_council.models import Severity


def test_agent11_layout_archetype():
    agent = LayoutArchetypeStrategist()
    deck = {
        "slides": [
            {
                "slide_id": "s1",
                "archetype": "grid_2x2",  # Expects 4 atoms, has only 1!
                "atoms": [{"title": "Only One", "text": "Detail text"}]
            }
        ]
    }
    findings = agent.audit(deck)
    assert len(findings) == 1, "Must flag incompatible archetype atom count"
    assert findings[0].severity == Severity.P1

    remediated = agent.auto_remediate(deck, findings)
    assert remediated["slides"][0]["archetype"] == "quote_callout"
    print("✔ test_agent11_layout_archetype passed")


def test_agent12_data_chart():
    agent = DataChartCartographer()
    deck = {
        "slides": [
            {
                "slide_id": "s1",
                "chart": {
                    "type": "pie",
                    "data": [40, 50, 35]  # Sum = 125% -> Contradiction!
                    # Missing unit!
                }
            },
            {
                "slide_id": "s2",
                "chart": {
                    "type": "bar_vertical",
                    "series": []  # Empty data -> P0!
                }
            }
        ]
    }
    findings = agent.audit(deck)
    p0_issues = [f for f in findings if f.severity == Severity.P0]
    p1_issues = [f for f in findings if f.severity == Severity.P1]
    assert len(p0_issues) == 2, f"Expected 2 P0 chart issues (sum != 100% and empty series), got {len(p0_issues)}"
    assert len(p1_issues) >= 1, "Expected P1 issue for missing unit"

    # Auto-remediation
    remediated = agent.auto_remediate(deck, findings)
    s1_data = remediated["slides"][0]["chart"]["data"]
    assert abs(sum(s1_data) - 100.0) <= 0.5, f"Pie chart must sum to 100%, got {sum(s1_data)}"
    assert remediated["slides"][0]["chart"]["unit"] == "%"
    print("✔ test_agent12_data_chart passed")


def test_agent13_typography_sentinel():
    agent = TypographyWidowOrphanSentinel()
    deck = {
        "slides": [
            {
                "slide_id": "s1",
                "assertion_title": "Chiến lược chuyển đổi số quốc gia và",  # Ends with orphan 'và'
                "atoms": [
                    {"title": "Mục tiêu", "text": "Dự kiến tốc độ tăng trưởng đạt 15%"}  # Ends with '15%'
                ]
            }
        ]
    }
    findings = agent.audit(deck)
    assert len(findings) == 2, f"Expected 2 orphan findings, got {len(findings)}"
    assert any("và" in f.issue for f in findings)
    assert any("15%" in f.issue for f in findings)

    # Auto-remediation: Injects non-breaking space
    remediated = agent.auto_remediate(deck, findings)
    s1 = remediated["slides"][0]
    assert "\u00A0và" in s1["assertion_title"], "Must bind orphan with non-breaking space"
    assert "\u00A015%" in s1["atoms"][0]["text"], "Must bind orphan percentage"
    print("✔ test_agent13_typography_sentinel passed")


def test_agent14_visual_ergonomics():
    agent = VisualErgonomicsAuditor()
    deck = {
        "slides": [
            {
                "slide_id": "s1",
                "bg_color": "#FFFFFF",
                "text_color": "#D0D5DD",  # Low contrast grey on white!
                "body_font_size": 10      # Too small (< 14pt)
            }
        ]
    }
    findings = agent.audit(deck)
    assert len(findings) == 2, f"Expected 2 ergonomics findings, got {len(findings)}"
    assert any("tương phản" in f.issue for f in findings)
    assert any("Cỡ chữ" in f.issue for f in findings)

    # Auto-remediation
    remediated = agent.auto_remediate(deck, findings)
    s1 = remediated["slides"][0]
    assert s1["text_color"] == "#0F172A"
    assert s1["body_font_size"] >= 14
    print("✔ test_agent14_visual_ergonomics passed")


def test_agent15_motion_choreographer():
    agent = MotionChoreographer()
    deck = {
        "slides": [
            {
                "slide_id": "s1",
                "transition": "morph",
                "transition_duration": 4.0,  # Too slow (> 2.5s)
                "morph_shapes": ["hero_card", "!!valid_card!!"]  # hero_card lacks !!
            }
        ]
    }
    findings = agent.audit(deck)
    assert any("chậm" in f.issue for f in findings), "Must flag sluggish duration"
    assert any("hero_card" in f.issue for f in findings), "Must flag invalid morph shape identifier"

    # Auto-remediation
    remediated = agent.auto_remediate(deck, findings)
    s1 = remediated["slides"][0]
    assert s1["transition_duration"] == 1.0
    assert "!!hero_card!!" in s1["morph_shapes"]
    print("✔ test_agent15_motion_choreographer passed")


if __name__ == "__main__":
    print("Running Gate 4 Unit Tests...")
    test_agent11_layout_archetype()
    test_agent12_data_chart()
    test_agent13_typography_sentinel()
    test_agent14_visual_ergonomics()
    test_agent15_motion_choreographer()
    print("🎉 Gate 4 Unit Tests Passed 100%!")

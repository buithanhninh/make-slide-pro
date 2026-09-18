"""
tests/macc_council/test_gate2.py
Adversarial Unit Tests for Gate 2: Macro-Narrative Arc & Consistency
Tests Agent 3 (NarrativeArcDirector) and Agent 4 (CrossSlideConsistencyAuditor).
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from scripts.macc_council.gate2_macro_narrative import (
    NarrativeArcDirector,
    CrossSlideConsistencyAuditor
)
from scripts.macc_council.models import Severity


def test_agent03_abrupt_ending():
    agent = NarrativeArcDirector()
    deck = {
        "slides": [
            {
                "slide_id": "slide_01",
                "assertion_title": "Báo cáo Chiến lược Phát triển AI 2025",
                "archetype": "title_hero"
            },
            {
                "slide_id": "slide_02",
                "assertion_title": "Phân tích số liệu thị trường bán dẫn",
                "archetype": "table_dense",
                "section": "Thực trạng"
            },
            {
                "slide_id": "slide_03",
                "assertion_title": "Bảng dự toán chi phí cơ sở hạ tầng",
                "archetype": "table_dense",
                "section": "Thực trạng"
            }
        ]
    }
    findings = agent.audit(deck)
    p1_issues = [f for f in findings if f.severity == Severity.P1]
    assert len(p1_issues) >= 1, "Must flag missing conclusion on abrupt ending"
    assert "Thiếu slide Kết luận" in p1_issues[0].issue
    print("✔ test_agent03_abrupt_ending passed")


def test_agent03_section_fragmentation():
    agent = NarrativeArcDirector()
    deck = {
        "slides": [
            {"slide_id": "slide_01", "assertion_title": "Tổng quan dự án", "section": "Mở đầu"},
            {"slide_id": "slide_02", "assertion_title": "Chi phí năm 2024", "section": "Tài chính"},
            {"slide_id": "slide_03", "assertion_title": "Kiến trúc kỹ thuật", "section": "Công nghệ"},
            {"slide_id": "slide_04", "assertion_title": "Dự toán quý 4", "section": "Tài chính"},  # Jumped back!
            {"slide_id": "slide_05", "assertion_title": "Tổng kết và hành động", "section": "Kết luận"}
        ]
    }
    findings = agent.audit(deck)
    mece_issues = [f for f in findings if "non-MECE" in f.issue or "nhảy cóc" in f.issue]
    assert len(mece_issues) >= 1, "Must flag non-MECE section bouncing"
    print("✔ test_agent03_section_fragmentation passed")


def test_agent03_auto_remediate_conclusion():
    agent = NarrativeArcDirector()
    deck = {
        "slides": [
            {"slide_id": "slide_01", "assertion_title": "Báo cáo Chiến lược AI", "archetype": "title_hero"},
            {"slide_id": "slide_02", "assertion_title": "Phân tích thị trường", "archetype": "split_comparison"},
            {"slide_id": "slide_03", "assertion_title": "Chi tiết số liệu", "archetype": "table_dense"}
        ]
    }
    findings = agent.audit(deck)
    assert any("Thiếu slide Kết luận" in f.issue for f in findings)

    remediated = agent.auto_remediate(deck, findings)
    assert len(remediated["slides"]) == 4, "Must append a conclusion slide"
    assert remediated["slides"][-1]["archetype"] == "conclusion_cta"
    print("✔ test_agent03_auto_remediate_conclusion passed")


def test_agent04_cross_slide_contradiction():
    agent = CrossSlideConsistencyAuditor()
    deck = {
        "slides": [
            {
                "slide_id": "slide_01",
                "assertion_title": "Doanh thu năm 2024: 1.500 tỷ",
                "primary_claim": "Tổng mức tăng trưởng ấn tượng trong năm."
            },
            {
                "slide_id": "slide_02",
                "assertion_title": "Tập trung mở rộng chuỗi cung ứng khu vực",
                "primary_claim": "Đẩy mạnh hợp tác quốc tế."
            },
            {
                "slide_id": "slide_03",
                "assertion_title": "Báo cáo tổng kết hiệu quả sản xuất kinh doanh",
                "primary_claim": "Doanh thu năm 2024: 2.100 tỷ vượt kế hoạch ban đầu."
            }
        ]
    }
    findings = agent.audit(deck)
    p0_issues = [f for f in findings if f.severity == Severity.P0]
    assert len(p0_issues) >= 1, "Must flag cross-slide numeric contradiction as P0"
    assert "Mâu thuẫn số liệu xuyên slide" in p0_issues[0].issue
    print(f"✔ test_agent04_cross_slide_contradiction passed: {p0_issues[0].issue}")


def test_agent04_visual_rhythm_fatigue():
    agent = CrossSlideConsistencyAuditor()
    deck = {
        "slides": [
            {"slide_id": "s1", "archetype": "3_cards", "assertion_title": "Trụ cột 1"},
            {"slide_id": "s2", "archetype": "3_cards", "assertion_title": "Trụ cột 2"},
            {"slide_id": "s3", "archetype": "3_cards", "assertion_title": "Trụ cột 3"},
            {"slide_id": "s4", "archetype": "3_cards", "assertion_title": "Trụ cột 4"},
            {"slide_id": "s5", "archetype": "conclusion_cta", "assertion_title": "Tổng kết"}
        ]
    }
    findings = agent.audit(deck)
    p2_issues = [f for f in findings if f.severity == Severity.P2 and "Rhythm Fatigue" in f.issue]
    assert len(p2_issues) >= 1, "Must flag 4 consecutive identical archetypes as rhythm fatigue"
    print("✔ test_agent04_visual_rhythm_fatigue passed")


def test_agent04_auto_remediation():
    agent = CrossSlideConsistencyAuditor()
    deck = {
        "slides": [
            {"slide_id": "s1", "assertion_title": "Doanh thu năm 2024: 1.500 tỷ", "archetype": "3_cards"},
            {"slide_id": "s2", "assertion_title": "Đầu tư hạ tầng", "archetype": "3_cards"},
            {"slide_id": "s3", "assertion_title": "Chuyển đổi số", "archetype": "3_cards"},
            {"slide_id": "s4", "assertion_title": "Doanh thu năm 2024: 2.100 tỷ", "archetype": "3_cards"}
        ]
    }
    findings = agent.audit(deck)
    remediated = agent.auto_remediate(deck, findings)
    # Check that s4 numeric contradiction was harmonized to 1.500 tỷ
    assert "1.500 tỷ" in remediated["slides"][3]["assertion_title"], "Contradiction must be remediated to canonical value"
    # Check that archetype of s4 was diversified
    assert remediated["slides"][3]["archetype"] != "3_cards", "Rhythm fatigue must be diversified"
    print("✔ test_agent04_auto_remediation passed")


if __name__ == "__main__":
    print("Running Gate 2 Unit Tests...")
    test_agent03_abrupt_ending()
    test_agent03_section_fragmentation()
    test_agent03_auto_remediate_conclusion()
    test_agent04_cross_slide_contradiction()
    test_agent04_visual_rhythm_fatigue()
    test_agent04_auto_remediation()
    print("🎉 Gate 2 Unit Tests Passed 100%!")

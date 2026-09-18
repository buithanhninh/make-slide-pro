"""
tests/macc_council/adversarial/test_agent04_hard.py
Adversarial Stress Test Matrix for Agent 04: CrossSlideConsistencyAuditor.
10 ruthless edge cases:
1. Exact metric contradiction across slides (P0)
2. Fuzzy metric contradiction (Tổng doanh thu vs Doanh thu) (P0)
3. Percentage metric contradiction (Tăng trưởng 6.8% vs 7.5%) (P0)
4. Legitimate metric progression across different years (2023 vs 2024 - NO FALSE POSITIVE)
5. Acronym & Terminology drift (DMS vs QLDL) (P1)
6. Brand / Product name inconsistency (Make Slide Pro vs Makeslide) (P1)
7. Visual rhythm fatigue (4 consecutive identical archetypes) (P2)
8. Healthy layout diversity (NO FALSE POSITIVE)
9. Auto-remediation harmonizes numeric contradictions
10. Auto-remediation diversifies fatigued archetypes
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from scripts.macc_council.gate2_macro_narrative import CrossSlideConsistencyAuditor
from scripts.macc_council.models import Severity


def run_all_adversarial_tests():
    agent = CrossSlideConsistencyAuditor()
    results = {}

    # Case 1: Exact metric contradiction
    deck_1 = {
        "slides": [
            {"slide_id": "s1", "assertion_title": "Doanh thu năm 2024: 1.500 tỷ VNĐ"},
            {"slide_id": "s2", "assertion_title": "Đầu tư hạ tầng"},
            {"slide_id": "s3", "assertion_title": "Doanh thu năm 2024: 2.100 tỷ VNĐ"}
        ]
    }
    f1 = agent.audit(deck_1)
    results["Case 1 (Exact Metric Contradiction)"] = any(f.severity == Severity.P0 and "Mâu thuẫn" in f.issue for f in f1)

    # Case 2: Fuzzy metric contradiction (Tổng doanh thu vs Doanh thu)
    deck_2 = {
        "slides": [
            {"slide_id": "s1", "assertion_title": "Tổng doanh thu năm 2024: 1.500 tỷ VNĐ"},
            {"slide_id": "s2", "assertion_title": "Doanh thu năm 2024: 2.100 tỷ VNĐ"}
        ]
    }
    f2 = agent.audit(deck_2)
    results["Case 2 (Fuzzy Metric Contradiction)"] = any(f.severity == Severity.P0 and "Mâu thuẫn" in f.issue for f in f2)

    # Case 3: Percentage contradiction
    deck_3 = {
        "slides": [
            {"slide_id": "s1", "assertion_title": "Tỷ lệ tăng trưởng kinh tế: 6.8%"},
            {"slide_id": "s2", "assertion_title": "Tăng trưởng kinh tế: 7.5%"}
        ]
    }
    f3 = agent.audit(deck_3)
    results["Case 3 (Percentage Contradiction)"] = any(f.severity == Severity.P0 and "Mâu thuẫn" in f.issue for f in f3)

    # Case 4: Legitimate different years (2023 vs 2024 - NO FALSE POSITIVE)
    deck_4 = {
        "slides": [
            {"slide_id": "s1", "assertion_title": "Doanh thu năm 2023: 1.200 tỷ VNĐ"},
            {"slide_id": "s2", "assertion_title": "Doanh thu năm 2024: 1.500 tỷ VNĐ"}
        ]
    }
    f4 = agent.audit(deck_4)
    results["Case 4 (Different Years - No False Positive)"] = len(f4) == 0

    # Case 5: Acronym & Terminology drift
    deck_5 = {
        "slides": [
            {"slide_id": "s1", "assertion_title": "Hệ thống Quản lý Dữ liệu (DMS)"},
            {"slide_id": "s2", "assertion_title": "Giải pháp triển khai phần mềm"},
            {"slide_id": "s3", "assertion_title": "Tích hợp ứng dụng QLDL vào cơ sở dữ liệu"}
        ]
    }
    f5 = agent.audit(deck_5)
    results["Case 5 (Acronym Terminology Drift)"] = any("thuật ngữ" in f.issue.lower() or "dms" in f.issue.lower() or "qldl" in f.issue.lower() or f.severity in [Severity.P0, Severity.P1] for f in f5)

    # Case 6: Brand / Product name inconsistency
    deck_6 = {
        "slides": [
            {"slide_id": "s1", "assertion_title": "Giới thiệu nền tảng Make Slide Pro"},
            {"slide_id": "s2", "assertion_title": "Kiến trúc MakeSlidePro V8"},
            {"slide_id": "s3", "assertion_title": "Khả năng mở rộng của Makeslide"}
        ]
    }
    f6 = agent.audit(deck_6)
    results["Case 6 (Brand Name Inconsistency)"] = any("bất nhất" in f.issue.lower() or "makeslide" in f.issue.lower() or f.severity in [Severity.P1, Severity.P2] for f in f6)

    # Case 7: Visual rhythm fatigue (4 identical consecutive)
    deck_7 = {
        "slides": [
            {"slide_id": "s1", "archetype": "3_cards", "assertion_title": "Cột 1"},
            {"slide_id": "s2", "archetype": "3_cards", "assertion_title": "Cột 2"},
            {"slide_id": "s3", "archetype": "3_cards", "assertion_title": "Cột 3"},
            {"slide_id": "s4", "archetype": "3_cards", "assertion_title": "Cột 4"}
        ]
    }
    f7 = agent.audit(deck_7)
    results["Case 7 (Visual Rhythm Fatigue)"] = any("Fatigue" in f.issue or "nhịp điệu" in f.issue.lower() for f in f7)

    # Case 8: Healthy layout diversity (NO FALSE POSITIVE)
    deck_8 = {
        "slides": [
            {"slide_id": "s1", "archetype": "title_hero", "assertion_title": "Chiến lược"},
            {"slide_id": "s2", "archetype": "split_comparison", "assertion_title": "So sánh"},
            {"slide_id": "s3", "archetype": "3_cards", "assertion_title": "Trụ cột"},
            {"slide_id": "s4", "archetype": "conclusion_cta", "assertion_title": "Tổng kết"}
        ]
    }
    f8 = agent.audit(deck_8)
    results["Case 8 (Healthy Layout Diversity - No False Positive)"] = len(f8) == 0

    # Case 9: Auto-remediation harmonizes numeric contradictions
    deck_9 = {
        "slides": [
            {"slide_id": "s1", "assertion_title": "Doanh thu năm 2024: 1.500 tỷ VNĐ"},
            {"slide_id": "s2", "assertion_title": "Doanh thu năm 2024: 2.100 tỷ VNĐ"}
        ]
    }
    f9 = agent.audit(deck_9)
    rem9 = agent.auto_remediate(deck_9, f9)
    results["Case 9 (Auto-Remediate Contradiction)"] = "1.500 tỷ VNĐ" in rem9["slides"][1]["assertion_title"]

    # Case 10: Auto-remediation diversifies fatigued archetypes
    deck_10 = {
        "slides": [
            {"slide_id": "s1", "archetype": "3_cards", "assertion_title": "Cột 1"},
            {"slide_id": "s2", "archetype": "3_cards", "assertion_title": "Cột 2"},
            {"slide_id": "s3", "archetype": "3_cards", "assertion_title": "Cột 3"},
            {"slide_id": "s4", "archetype": "3_cards", "assertion_title": "Cột 4"}
        ]
    }
    f10 = agent.audit(deck_10)
    rem10 = agent.auto_remediate(deck_10, f10)
    results["Case 10 (Auto-Remediate Rhythm Fatigue)"] = rem10["slides"][3]["archetype"] != "3_cards"

    return results


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING ADVERSARIAL STRESS TEST MATRIX FOR AGENT 04")
    print("=" * 60)
    res = run_all_adversarial_tests()
    passed_count = sum(1 for v in res.values() if v)
    total_count = len(res)

    for case_name, passed in res.items():
        status = "PASSED" if passed else "FAILED"
        icon = "✔" if passed else "✘"
        print(f"{icon} [{status}] {case_name}")

    print("-" * 60)
    print(f"Total Score: {passed_count}/{total_count} ({passed_count/total_count*100:.1f}%)")
    print("=" * 60)

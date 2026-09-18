"""
tests/macc_council/adversarial/test_agent13_hard.py
Adversarial Stress Test Matrix for Agent 13: TypographyWidowOrphanSentinel.
Validates Vietnamese orphan word detection, non-breaking space binding (\u00A0), schema-agnostic traversal, and auto-remediation.
"""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from scripts.macc_council.gate4_spatial_motion.agent13_typography_sentinel import TypographyWidowOrphanSentinel
from scripts.macc_council.models import Severity


def test_agent13_adversarial_matrix():
    print("=" * 60)
    print("RUNNING ADVERSARIAL STRESS TEST MATRIX FOR AGENT 13")
    print("=" * 60)

    agent = TypographyWidowOrphanSentinel()
    passed = 0
    total = 10

    # CASE 1: Title ending with orphan preposition "cho" (P2)
    slide_c1 = {
        "slide_id": "c1",
        "assertion_title": "Tập trung triển khai các giải pháp chuyển đổi cho",
        "archetype": "card_grid",
        "atoms": []
    }
    findings_c1 = agent.audit([slide_c1])
    assert len(findings_c1) >= 1 and any("mồ côi" in f.issue.lower() for f in findings_c1), "Case 1 Failed: Terminal orphan word 'cho' missed"
    print("✔ [PASSED] Case 1 (Terminal Orphan Preposition 'cho' - P2 Caught)")
    passed += 1

    # CASE 2: Title ending with orphan year "2024" (P2)
    slide_c2 = {
        "slide_id": "c2",
        "assertion_title": "Doanh thu tăng trưởng vượt kế hoạch năm 2024",
        "archetype": "card_grid",
        "atoms": []
    }
    findings_c2 = agent.audit([slide_c2])
    assert len(findings_c2) >= 1 and any("mồ côi" in f.issue.lower() for f in findings_c2), "Case 2 Failed: Terminal orphan year '2024' missed"
    print("✔ [PASSED] Case 2 (Terminal Orphan Year '2024' - P2 Caught)")
    passed += 1

    # CASE 3: Title already bound with non-breaking space \u00A0 (Valid - No False Positive)
    slide_c3 = {
        "slide_id": "c3",
        "assertion_title": "Doanh thu tăng trưởng vượt kế hoạch năm\u00A02024",
        "archetype": "card_grid",
        "atoms": []
    }
    findings_c3 = agent.audit([slide_c3])
    assert len(findings_c3) == 0, f"Case 3 Failed: False positive on \u00A0 bound title: {[f.issue for f in findings_c3]}"
    print("✔ [PASSED] Case 3 (Already Bound Title with \\u00A0 - No False Positive)")
    passed += 1

    # CASE 4: Content item text ending with orphan percentage "18%" (P2)
    slide_c4 = {
        "slide_id": "c4",
        "assertion_title": "Chỉ số hoàn thành kế hoạch năm",
        "atoms": [
            {"title": "Mục tiêu", "text": "Tỷ lệ tăng trưởng biên lợi nhuận đạt 18%"}
        ]
    }
    findings_c4 = agent.audit([slide_c4])
    assert len(findings_c4) >= 1 and any("18%" in f.issue or "mồ côi" in f.issue.lower() for f in findings_c4), "Case 4 Failed: Orphan percentage '18%' missed"
    print("✔ [PASSED] Case 4 (Content Item Ending with '18%' - P2 Caught)")
    passed += 1

    # CASE 5: Schema-Agnostic 'title' field ending with orphan word "và" (P2)
    slide_c5 = {
        "slide_id": "c5",
        "title": "Chiến lược phát triển thị trường và",
        "archetype": "card_grid"
    }
    findings_c5 = agent.audit([slide_c5])
    assert len(findings_c5) >= 1 and any("mồ côi" in f.issue.lower() for f in findings_c5), "Case 5 Failed: Schema-agnostic title orphan 'và' missed"
    print("✔ [PASSED] Case 5 (Schema-Agnostic 'title' Ending with 'và' - P2 Caught)")
    passed += 1

    # CASE 6: Schema-Agnostic cards description ending with orphan unit "tỷ" (P2)
    slide_c6 = {
        "slide_id": "c6",
        "title": "Kế hoạch huy động vốn đầu tư",
        "cards": [
            {"headline": "Vốn điều lệ", "description": "Tổng ngân sách phân bổ đạt 50 tỷ"}
        ]
    }
    findings_c6 = agent.audit([slide_c6])
    assert len(findings_c6) >= 1 and any("mồ côi" in f.issue.lower() for f in findings_c6), "Case 6 Failed: Cards description orphan 'tỷ' missed"
    print("✔ [PASSED] Case 6 (Schema-Agnostic Cards Description Orphan 'tỷ' - P2 Caught)")
    passed += 1

    # CASE 7: Clean multi-syllable normal ending (Valid - No False Positive)
    slide_c7 = {
        "slide_id": "c7",
        "assertion_title": "Tối ưu hóa quy trình quản trị doanh nghiệp toàn diện",
        "archetype": "card_grid",
        "atoms": [
            {"title": "Quy trình", "text": "Chuẩn hóa các mắt xích tác nghiệp phòng ban"}
        ]
    }
    findings_c7 = agent.audit([slide_c7])
    assert len(findings_c7) == 0, f"Case 7 Failed: False positive on clean multi-syllable ending: {[f.issue for f in findings_c7]}"
    print("✔ [PASSED] Case 7 (Clean Multi-Syllable Ending - No False Positive)")
    passed += 1

    # CASE 8: Single-word title (Valid - No False Positive)
    slide_c8 = {
        "slide_id": "c8",
        "assertion_title": "Overview",
        "archetype": "title_hero"
    }
    findings_c8 = agent.audit([slide_c8])
    assert len(findings_c8) == 0, f"Case 8 Failed: False positive on single-word title: {[f.issue for f in findings_c8]}"
    print("✔ [PASSED] Case 8 (Single-Word Title - No False Positive)")
    passed += 1

    # CASE 9: Text ending with punctuation after orphan word (P2)
    slide_c9 = {
        "slide_id": "c9",
        "assertion_title": "Thị trường xuất khẩu mở rộng sang khu vực ASEAN trong năm 2024.",
        "archetype": "card_grid"
    }
    findings_c9 = agent.audit([slide_c9])
    assert len(findings_c9) >= 1 and any("mồ côi" in f.issue.lower() for f in findings_c9), "Case 9 Failed: Orphan word followed by period missed"
    print("✔ [PASSED] Case 9 (Orphan Word Followed by Period - P2 Caught)")
    passed += 1

    # CASE 10: Auto-Remediation Binds Orphan Words Across Schemas
    slide_c10 = {
        "slide_id": "c10",
        "title": "Mục tiêu tăng trưởng năm 2025",
        "cards": [
            {"headline": "Doanh thu", "description": "Kỳ vọng mức tăng 25%"}
        ]
    }
    findings_c10 = agent.audit([slide_c10])
    assert len(findings_c10) >= 2, f"Case 10 Failed: Expected findings for remediation, got {len(findings_c10)}"
    remediated = agent.auto_remediate([slide_c10], findings_c10)
    rem_title = remediated[0].get("assertion_title") or remediated[0].get("title")
    rem_desc = remediated[0]["cards"][0]["description"]
    assert "\u00A02025" in rem_title, f"Title not bound with \\u00A0: {repr(rem_title)}"
    assert "\u00A025%" in rem_desc, f"Cards description not bound with \\u00A0: {repr(rem_desc)}"
    re_audit = agent.audit(remediated)
    assert len(re_audit) == 0, f"Case 10 Failed: Residual orphan findings after remediation: {[f.issue for f in re_audit]}"
    print("✔ [PASSED] Case 10 (Auto-Remediation Binds \\u00A0 & Passes Re-Audit)")
    passed += 1

    print("-" * 60)
    print(f"Total Score: {passed}/{total} ({passed/total*100:.1f}%)")
    print("=" * 60)
    assert passed == total, f"Adversarial matrix failed: {passed}/{total}"


if __name__ == "__main__":
    test_agent13_adversarial_matrix()

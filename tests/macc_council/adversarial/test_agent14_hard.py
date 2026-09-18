"""
tests/macc_council/adversarial/test_agent14_hard.py
Adversarial Stress Test Matrix for Agent 14: VisualErgonomicsAuditor.
Validates WCAG AAA color contrast, boardroom 20m font scaling, named color parsing, and auto-remediation.
"""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from scripts.macc_council.gate4_spatial_motion.agent14_visual_ergonomics import VisualErgonomicsAuditor
from scripts.macc_council.models import Severity


def test_agent14_adversarial_matrix():
    print("=" * 60)
    print("RUNNING ADVERSARIAL STRESS TEST MATRIX FOR AGENT 14")
    print("=" * 60)

    agent = VisualErgonomicsAuditor()
    passed = 0
    total = 10

    # CASE 1: Low contrast text on light background (#94A3B8 on #FFFFFF ~ 2.3:1) (P1)
    slide_c1 = {
        "slide_id": "c1",
        "title": "Báo cáo hiệu suất",
        "bg_color": "#FFFFFF",
        "text_color": "#94A3B8"
    }
    findings_c1 = agent.audit([slide_c1])
    assert len(findings_c1) >= 1 and any("tương phản" in f.issue.lower() for f in findings_c1), "Case 1 Failed: Low contrast light gray on white missed"
    print("✔ [PASSED] Case 1 (Low Contrast on Light Background - P1 Caught)")
    passed += 1

    # CASE 2: Low contrast text on dark background (#1E293B on #0B1120 ~ 1.3:1) (P1)
    slide_c2 = {
        "slide_id": "c2",
        "title": "Kiến trúc hệ thống bảo mật",
        "bg_color": "#0B1120",
        "text_color": "#1E293B"
    }
    findings_c2 = agent.audit([slide_c2])
    assert len(findings_c2) >= 1 and any("tương phản" in f.issue.lower() for f in findings_c2), "Case 2 Failed: Low contrast dark slate on navy missed"
    print("✔ [PASSED] Case 2 (Low Contrast on Dark Background - P1 Caught)")
    passed += 1

    # CASE 3: High contrast on light background (#0F172A on #FFFFFF ~ 16:1) (Valid - No False Positive)
    slide_c3 = {
        "slide_id": "c3",
        "title": "Kế hoạch quý 4",
        "bg_color": "#FFFFFF",
        "text_color": "#0F172A"
    }
    findings_c3 = agent.audit([slide_c3])
    assert len(findings_c3) == 0, f"Case 3 Failed: False positive on high contrast light: {[f.issue for f in findings_c3]}"
    print("✔ [PASSED] Case 3 (High Contrast on Light Background - No False Positive)")
    passed += 1

    # CASE 4: High contrast on dark background (#F8FAFC on #0F172A ~ 15:1) (Valid - No False Positive)
    slide_c4 = {
        "slide_id": "c4",
        "title": "Báo cáo công nghệ",
        "bg_color": "#0F172A",
        "text_color": "#F8FAFC"
    }
    findings_c4 = agent.audit([slide_c4])
    assert len(findings_c4) == 0, f"Case 4 Failed: False positive on high contrast dark: {[f.issue for f in findings_c4]}"
    print("✔ [PASSED] Case 4 (High Contrast on Dark Background - No False Positive)")
    passed += 1

    # CASE 5: Body font size < 14pt (11pt) (P1)
    slide_c5 = {
        "slide_id": "c5",
        "title": "Chi tiết số liệu",
        "body_font_size": 11
    }
    findings_c5 = agent.audit([slide_c5])
    assert len(findings_c5) >= 1 and any("cỡ chữ" in f.issue.lower() or "14pt" in f.issue for f in findings_c5), "Case 5 Failed: Body font size 11pt missed"
    print("✔ [PASSED] Case 5 (Body Font Size < 14pt - P1 Caught)")
    passed += 1

    # CASE 6: Title font size < 20pt (16pt) (P1)
    slide_c6 = {
        "slide_id": "c6",
        "title": "Tiêu đề quá nhỏ",
        "title_font_size": 16
    }
    findings_c6 = agent.audit([slide_c6])
    assert len(findings_c6) >= 1 and any("tiêu đề" in f.issue.lower() or "cỡ chữ" in f.issue.lower() for f in findings_c6), "Case 6 Failed: Title font size 16pt missed"
    print("✔ [PASSED] Case 6 (Title Font Size < 20pt - P1 Caught)")
    passed += 1

    # CASE 7: Valid font sizes (title: 32pt, body: 16pt) (Valid - No False Positive)
    slide_c7 = {
        "slide_id": "c7",
        "title": "Quy chuẩn trình chiếu phòng họp",
        "title_font_size": 32,
        "body_font_size": 16
    }
    findings_c7 = agent.audit([slide_c7])
    assert len(findings_c7) == 0, f"Case 7 Failed: False positive on valid font sizes: {[f.issue for f in findings_c7]}"
    print("✔ [PASSED] Case 7 (Valid Boardroom Font Sizes - No False Positive)")
    passed += 1

    # CASE 8: Named color parsing ('white', 'black') (Valid - No False Positive)
    slide_c8 = {
        "slide_id": "c8",
        "title": "Giao diện tương phản đen trắng",
        "bg_color": "white",
        "text_color": "black"
    }
    findings_c8 = agent.audit([slide_c8])
    assert len(findings_c8) == 0, f"Case 8 Failed: Failed to parse named colors white/black: {[f.issue for f in findings_c8]}"
    print("✔ [PASSED] Case 8 (Named Colors Parsing 'white/black' - No False Positive)")
    passed += 1

    # CASE 9: Card-level low contrast check (P1)
    slide_c9 = {
        "slide_id": "c9",
        "title": "Thẻ phân tích chuyên sâu",
        "cards": [
            {"headline": "Mục 1", "bg_color": "#F1F5F9", "text_color": "#CBD5E1"}  # contrast ~1.3:1
        ]
    }
    findings_c9 = agent.audit([slide_c9])
    assert len(findings_c9) >= 1 and any("tương phản" in f.issue.lower() for f in findings_c9), "Case 9 Failed: Card-level low contrast missed"
    print("✔ [PASSED] Case 9 (Card-Level Low Contrast - P1 Caught)")
    passed += 1

    # CASE 10: Auto-Remediation Corrects Contrast and Font Scale
    slide_c10 = {
        "slide_id": "c10",
        "title": "Hiệu chỉnh tự động",
        "bg_color": "#0B1120",
        "text_color": "#1E293B",
        "body_font_size": 10,
        "title_font_size": 16
    }
    findings_c10 = agent.audit([slide_c10])
    assert len(findings_c10) >= 2, f"Case 10 Failed: Expected findings for remediation, got {len(findings_c10)}"
    remediated = agent.auto_remediate([slide_c10], findings_c10)
    rem_slide = remediated[0]
    assert rem_slide["text_color"] == "#FFFFFF", f"Text color not fixed to white: {rem_slide['text_color']}"
    assert rem_slide["body_font_size"] >= 14, f"Body font size not bumped: {rem_slide['body_font_size']}"
    assert rem_slide["title_font_size"] >= 24, f"Title font size not bumped: {rem_slide['title_font_size']}"
    re_audit = agent.audit(remediated)
    assert len(re_audit) == 0, f"Case 10 Failed: Residual issues after auto-remediation: {[f.issue for f in re_audit]}"
    print("✔ [PASSED] Case 10 (Auto-Remediation Corrects Contrast & Font Scale)")
    passed += 1

    print("-" * 60)
    print(f"Total Score: {passed}/{total} ({passed/total*100:.1f}%)")
    print("=" * 60)
    assert passed == total, f"Adversarial matrix failed: {passed}/{total}"


if __name__ == "__main__":
    test_agent14_adversarial_matrix()

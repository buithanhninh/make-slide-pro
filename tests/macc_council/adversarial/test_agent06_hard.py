"""
tests/macc_council/adversarial/test_agent06_hard.py
Adversarial Stress Test Matrix for Agent 06: MathematicalOMMLValidator.
Validates LaTeX equations, OMML syntax integrity, bracket balancing, currency shielding, and auto-remediation.
"""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from scripts.macc_council.gate3_micro_pedagogy.agent06_mathematical_omml import MathematicalOMMLValidator
from scripts.macc_council.models import Severity


def test_agent06_adversarial_matrix():
    print("=" * 60)
    print("RUNNING ADVERSARIAL STRESS TEST MATRIX FOR AGENT 06")
    print("=" * 60)

    agent = MathematicalOMMLValidator()
    passed = 0
    total = 10

    # CASE 1: Unclosed curly brace in complex fraction (P0)
    slide_c1 = {
        "slide_id": "c1",
        "title": "Mô hình định lượng rủi ro",
        "content_items": [
            {"body": r"Phương sai mẫu được tính theo công thức: $\frac{\sum_{i=1}^n (x_i - \bar{x})^2}{n - 1$"}
        ]
    }
    findings_c1 = agent.audit([slide_c1])
    assert len(findings_c1) >= 1 and any(f.severity == Severity.P0 for f in findings_c1), "Case 1 Failed: Unclosed curly brace not flagged as P0"
    print("✔ [PASSED] Case 1 (Unclosed Curly Brace in Complex Fraction - P0 Caught)")
    passed += 1

    # CASE 2: Missing closing math delimiter $$ (P0)
    slide_c2 = {
        "slide_id": "c2",
        "title": "Tích phân Gauss",
        "content_items": [
            {"body": r"Mật độ phân phối: $$f(x) = \int_0^\infty e^{-x^2} dx"}
        ]
    }
    findings_c2 = agent.audit([slide_c2])
    assert len(findings_c2) >= 1 and any("delimiter" in f.issue.lower() or "đóng" in f.issue.lower() or "cú pháp" in f.issue.lower() for f in findings_c2), "Case 2 Failed: Unclosed $$ delimiter missed"
    print("✔ [PASSED] Case 2 (Unclosed $$ Math Delimiter - P0 Caught)")
    passed += 1

    # CASE 3: Valid complex LaTeX formula (Valid - No False Positive)
    slide_c3 = {
        "slide_id": "c3",
        "title": "Độ lệch chuẩn tổng thể",
        "content_items": [
            {"body": r"Công thức chuẩn: $$\sigma = \sqrt{\frac{1}{N} \sum_{i=1}^N (x_i - \mu)^2}$$ áp dụng cho toàn bộ dữ liệu."}
        ]
    }
    findings_c3 = agent.audit([slide_c3])
    assert len(findings_c3) == 0, f"Case 3 Failed: False positive on valid complex LaTeX: {[f.issue for f in findings_c3]}"
    print("✔ [PASSED] Case 3 (Valid Complex LaTeX Formula - No False Positive)")
    passed += 1

    # CASE 4: Financial currency notation with $ (Valid - No False Positive)
    slide_c4 = {
        "slide_id": "c4",
        "title": "Tình hình tài chính quý 3",
        "content_items": [
            {"body": "Doanh thu vượt mốc $150 million USD và lợi nhuận gộp đạt $45M, tăng trưởng 20%."}
        ]
    }
    findings_c4 = agent.audit([slide_c4])
    assert len(findings_c4) == 0, f"Case 4 Failed: False positive on financial currency $ signs: {[f.issue for f in findings_c4]}"
    print("✔ [PASSED] Case 4 (Financial Currency Notation - No False Positive)")
    passed += 1

    # CASE 5: Text citations and markdown brackets (Valid - No False Positive)
    slide_c5 = {
        "slide_id": "c5",
        "title": "Tài liệu tham khảo",
        "content_items": [
            {"body": "Theo báo cáo [GSO, 2024] và nghiên cứu của WB (World Bank, 2023), chỉ số FDI tăng mạnh."}
        ]
    }
    findings_c5 = agent.audit([slide_c5])
    assert len(findings_c5) == 0, f"Case 5 Failed: False positive on text parentheses and brackets: {[f.issue for f in findings_c5]}"
    print("✔ [PASSED] Case 5 (Text Citations and Brackets - No False Positive)")
    passed += 1

    # CASE 6: Double superscript without braces x^2^3 (P1 Crash Risk)
    slide_c6 = {
        "slide_id": "c6",
        "title": "Lũy thừa đa tầng",
        "content_items": [
            {"body": r"Giá trị mở rộng tính theo $y = x^2^3 + a_i_j$ gây lỗi phân tích."}
        ]
    }
    findings_c6 = agent.audit([slide_c6])
    assert len(findings_c6) >= 1 and any("lũy thừa" in f.issue.lower() or "chỉ số" in f.issue.lower() or "superscript" in f.issue.lower() or "subscript" in f.issue.lower() or "cú pháp" in f.issue.lower() for f in findings_c6), "Case 6 Failed: Double superscript/subscript missed"
    print("✔ [PASSED] Case 6 (Double Superscript/Subscript Without Braces - P1 Caught)")
    passed += 1

    # CASE 7: \frac with single argument (P1)
    slide_c7 = {
        "slide_id": "c7",
        "title": "Công thức phân số lỗi",
        "content_items": [
            {"body": r"Tỷ số biến thiên $\frac{a + b}$ không hợp lệ trong KaTeX/OMML."}
        ]
    }
    findings_c7 = agent.audit([slide_c7])
    assert len(findings_c7) >= 1 and any("frac" in f.issue.lower() or "phân số" in f.issue.lower() for f in findings_c7), "Case 7 Failed: Incomplete \frac missed"
    print("✔ [PASSED] Case 7 (Incomplete \frac Argument - P1 Caught)")
    passed += 1

    # CASE 8: Trailing unescaped backslash inside math block (P1)
    slide_c8 = {
        "slide_id": "c8",
        "title": "Ký tự kết thúc lỗi",
        "content_items": [
            {"body": r"Hàm mục tiêu: $\alpha + \beta\ $"}
        ]
    }
    findings_c8 = agent.audit([slide_c8])
    assert len(findings_c8) >= 1 and any("backslash" in f.issue.lower() or "ký tự" in f.issue.lower() or "cú pháp" in f.issue.lower() for f in findings_c8), "Case 8 Failed: Trailing backslash missed"
    print("✔ [PASSED] Case 8 (Trailing Unescaped Backslash in Math - P1 Caught)")
    passed += 1

    # CASE 9: Schema Robustness - Math error inside generic card format
    slide_c9 = {
        "slide_id": "c9",
        "title": "Thẻ phân tích chuyên sâu",
        "cards": [
            {"headline": "Mô hình kinh tế lượng", "description": r"Hàm ước lượng: $Y = \beta_0 + \beta_1 X_1 + \epsilon_{i$"}
        ]
    }
    findings_c9 = agent.audit([slide_c9])
    assert len(findings_c9) >= 1, "Case 9 Failed: Formula error inside cards/description missed"
    print("✔ [PASSED] Case 9 (Schema Agnostic Card Extraction - Caught)")
    passed += 1

    # CASE 10: Auto-Remediation of Unbalanced Formula Brackets
    slide_c10 = {
        "slide_id": "c10",
        "title": "Công thức tự sửa chữa",
        "content_items": [
            {"body": r"Hàm số: $f(x) = \sqrt{\frac{x^2 + 1}{2x$"}
        ]
    }
    findings_c10 = agent.audit([slide_c10])
    assert len(findings_c10) >= 1, "Case 10 Failed: Expected finding for auto-remediation"
    remediated = agent.auto_remediate([slide_c10], findings_c10)
    rem_text = agent.extract_slide_text(remediated[0])
    re_audit = agent.audit(remediated)
    assert len(re_audit) == 0, f"Case 10 Failed: Re-audit of remediated formula found residual issues: {[f.issue for f in re_audit]}"
    print("✔ [PASSED] Case 10 (Auto-Remediation Balances Brackets & Passes Re-Audit)")
    passed += 1

    print("-" * 60)
    print(f"Total Score: {passed}/{total} ({passed/total*100:.1f}%)")
    print("=" * 60)
    assert passed == total, f"Adversarial matrix failed: {passed}/{total}"


if __name__ == "__main__":
    test_agent06_adversarial_matrix()

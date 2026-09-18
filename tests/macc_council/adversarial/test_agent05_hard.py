"""
tests/macc_council/adversarial/test_agent05_hard.py
Adversarial Stress Test Matrix for Agent 05: DomainPedagogyScholar.
Validates macroeconomic, demographic, financial, and technical domain ontology and unit rigor.
"""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from scripts.macc_council.gate3_micro_pedagogy.agent05_domain_pedagogy import DomainPedagogyScholar
from scripts.macc_council.models import Severity


def test_agent05_adversarial_matrix():
    print("=" * 60)
    print("RUNNING ADVERSARIAL STRESS TEST MATRIX FOR AGENT 05")
    print("=" * 60)

    agent = DomainPedagogyScholar()
    passed = 0
    total = 10

    # CASE 1: GDP per capita in billions USD (Violation)
    slide_c1 = {
        "slide_id": "c1",
        "title": "Báo cáo kinh tế vĩ mô",
        "content_items": [
            {"body": "GDP bình quân đầu người của Việt Nam năm 2024 đạt 4.300 tỷ USD, tăng trưởng mạnh mẽ."}
        ]
    }
    findings_c1 = agent.audit([slide_c1])
    assert len(findings_c1) >= 1 and any("gdp bình quân" in f.issue.lower() for f in findings_c1), "Case 1 Failed: GDP per capita in billions USD missed"
    print("✔ [PASSED] Case 1 (GDP Per Capita in Billions USD - Violation Caught)")
    passed += 1

    # CASE 2: GDP per capita correct unit (Valid - No False Positive)
    slide_c2 = {
        "slide_id": "c2",
        "title": "Chỉ số thu nhập bình quân",
        "content_items": [
            {"body": "GDP bình quân đầu người năm 2024 đạt 4.300 USD/người/năm (tương đương 105 triệu VNĐ/người)."}
        ]
    }
    findings_c2 = agent.audit([slide_c2])
    assert len(findings_c2) == 0, f"Case 2 Failed: False positive on correct GDP per capita: {[f.issue for f in findings_c2]}"
    print("✔ [PASSED] Case 2 (GDP Per Capita Correct Unit - No False Positive)")
    passed += 1

    # CASE 3: Macro GDP nominal in billions USD (Valid - No False Positive)
    slide_c3 = {
        "slide_id": "c3",
        "title": "Quy mô nền kinh tế",
        "content_items": [
            {"body": "Tổng sản phẩm quốc nội (GDP) của Việt Nam đạt quy mô 430 tỷ USD vào cuối năm 2023."}
        ]
    }
    findings_c3 = agent.audit([slide_c3])
    assert len(findings_c3) == 0, f"Case 3 Failed: False positive on nominal GDP in billions: {[f.issue for f in findings_c3]}"
    print("✔ [PASSED] Case 3 (Nominal GDP in Billions USD - No False Positive)")
    passed += 1

    # CASE 4: TFR in percentage (Violation)
    slide_c4 = {
        "slide_id": "c4",
        "title": "Xu hướng nhân khẩu học",
        "content_items": [
            {"body": "Mức sinh thay thế (TFR) khu vực Đông Nam Bộ đã giảm mạnh xuống còn 1.48%."}
        ]
    }
    findings_c4 = agent.audit([slide_c4])
    assert len(findings_c4) >= 1 and any("mức sinh" in f.issue.lower() or "tfr" in f.issue.lower() or "tỷ suất sinh" in f.issue.lower() for f in findings_c4), "Case 4 Failed: TFR in % missed"
    print("✔ [PASSED] Case 4 (TFR in % - Violation Caught)")
    passed += 1

    # CASE 5: TFR correct unit (Valid - No False Positive)
    slide_c5 = {
        "slide_id": "c5",
        "title": "Chỉ số sinh sản",
        "content_items": [
            {"body": "Tỷ suất sinh thay thế toàn quốc duy trì ở mức 1,95 con/phụ nữ."}
        ]
    }
    findings_c5 = agent.audit([slide_c5])
    assert len(findings_c5) == 0, f"Case 5 Failed: False positive on valid TFR: {[f.issue for f in findings_c5]}"
    print("✔ [PASSED] Case 5 (TFR in con/phụ nữ - No False Positive)")
    passed += 1

    # CASE 6: Life expectancy in percentage (Violation)
    slide_c6 = {
        "slide_id": "c6",
        "title": "Chăm sóc sức khỏe y tế",
        "content_items": [
            {"body": "Tuổi thọ trung bình của người dân đạt 74.5%, cao hơn mức bình quân khu vực."}
        ]
    }
    findings_c6 = agent.audit([slide_c6])
    assert len(findings_c6) >= 1 and any("tuổi thọ" in f.issue.lower() for f in findings_c6), "Case 6 Failed: Life expectancy in % missed"
    print("✔ [PASSED] Case 6 (Life Expectancy in % - Violation Caught)")
    passed += 1

    # CASE 7: Semiconductor node in GHz (Violation)
    slide_c7 = {
        "slide_id": "c7",
        "title": "Năng lực sản xuất vi mạch",
        "content_items": [
            {"body": "Dây chuyền đúc chip bán dẫn tiến trình 3GHz dự kiến vận hành vào quý 4."}
        ]
    }
    findings_c7 = agent.audit([slide_c7])
    assert len(findings_c7) >= 1 and any("tiến trình" in f.issue.lower() or "bán dẫn" in f.issue.lower() for f in findings_c7), "Case 7 Failed: Semiconductor node in GHz missed"
    print("✔ [PASSED] Case 7 (Semiconductor Node in GHz - Violation Caught)")
    passed += 1

    # CASE 8: NPL (Non-Performing Loan / Nợ xấu) in absolute currency instead of ratio (Violation)
    slide_c8 = {
        "slide_id": "c8",
        "title": "Chỉ số an toàn ngân hàng",
        "content_items": [
            {"body": "Tỷ lệ nợ xấu (NPL) toàn hệ thống được kiểm soát ở mức 15.000 tỷ đồng."}
        ]
    }
    findings_c8 = agent.audit([slide_c8])
    assert len(findings_c8) >= 1 and any("nợ xấu" in f.issue.lower() or "npl" in f.issue.lower() for f in findings_c8), "Case 8 Failed: NPL in currency missed"
    print("✔ [PASSED] Case 8 (NPL Ratio in Absolute Currency - Violation Caught)")
    passed += 1

    # CASE 9: Foreign exchange reserves in percentage (Violation)
    slide_c9 = {
        "slide_id": "c9",
        "title": "Chính sách tiền tệ",
        "content_items": [
            {"body": "Dự trữ ngoại hối quốc gia đạt mức kỷ lục 12.5% trong năm 2024."}
        ]
    }
    findings_c9 = agent.audit([slide_c9])
    assert len(findings_c9) >= 1 and any("ngoại hối" in f.issue.lower() for f in findings_c9), "Case 9 Failed: Forex reserves in % missed"
    print("✔ [PASSED] Case 9 (Foreign Exchange Reserves in % - Violation Caught)")
    passed += 1

    # CASE 10: Auto-Remediation of Domain Unit Errors
    slide_c10 = {
        "slide_id": "c10",
        "title": "Tóm lược chỉ số kinh tế",
        "content_items": [
            {"title": "Mức sống", "body": "GDP bình quân đầu người: 4.500 tỷ USD."},
            {"title": "Dân số", "body": "Mức sinh thay thế: 2.1%."}
        ]
    }
    findings_c10 = agent.audit([slide_c10])
    assert len(findings_c10) >= 2, f"Case 10 Failed: Expected at least 2 findings for remediation, got {len(findings_c10)}"
    remediated = agent.auto_remediate([slide_c10], findings_c10)
    rem_text = agent.extract_slide_text(remediated[0])
    assert "tỷ usd" not in rem_text.lower(), f"Remediation failed to replace 'tỷ USD' in GDP per capita: {rem_text}"
    assert "usd/người" in rem_text.lower() or "usd" in rem_text.lower(), f"Remediation did not insert USD/người: {rem_text}"
    assert "2.1%" not in rem_text, f"Remediation failed to replace '2.1%' in TFR: {rem_text}"
    assert "con/phụ nữ" in rem_text.lower(), f"Remediation did not insert con/phụ nữ: {rem_text}"
    print("✔ [PASSED] Case 10 (Auto-Remediation Corrects Domain Units)")
    passed += 1

    print("-" * 60)
    print(f"Total Score: {passed}/{total} ({passed/total*100:.1f}%)")
    print("=" * 60)
    assert passed == total, f"Adversarial matrix failed: {passed}/{total}"


if __name__ == "__main__":
    test_agent05_adversarial_matrix()

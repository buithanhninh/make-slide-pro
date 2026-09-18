"""
tests/macc_council/adversarial/test_agent09_hard.py
Adversarial Stress Test Matrix for Agent 09: AdversarialContentCritic.
Validates red teaming of unsubstantiated superlatives (VN & EN), citation shielding, and defensible auto-remediation.
"""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from scripts.macc_council.gate3_micro_pedagogy.agent09_adversarial_critic import AdversarialContentCritic
from scripts.macc_council.models import Severity


def test_agent09_adversarial_matrix():
    print("=" * 60)
    print("RUNNING ADVERSARIAL STRESS TEST MATRIX FOR AGENT 09")
    print("=" * 60)

    agent = AdversarialContentCritic()
    passed = 0
    total = 10

    # CASE 1: Unsubstantiated "số 1 thị trường" (P1)
    slide_c1 = {
        "slide_id": "c1",
        "title": "Năng lực cạnh tranh cốt lõi",
        "content_items": [
            {"body": "Nền tảng của chúng tôi hiện là giải pháp số 1 thị trường về tối ưu hóa chi phí doanh nghiệp."}
        ]
    }
    findings_c1 = agent.audit([slide_c1])
    assert len(findings_c1) >= 1 and any("số 1" in f.issue.lower() or "kiểm chứng" in f.issue.lower() for f in findings_c1), "Case 1 Failed: 'số 1 thị trường' missed"
    print("✔ [PASSED] Case 1 (Unsubstantiated 'số 1 thị trường' - P1 Caught)")
    passed += 1

    # CASE 2: Scientifically impossible "bảo mật tuyệt đối" (P1)
    slide_c2 = {
        "slide_id": "c2",
        "title": "Kiến trúc an ninh mạng",
        "content_items": [
            {"body": "Hệ thống cam kết bảo mật tuyệt đối và ngăn chặn 100% mọi cuộc tấn công mạng."}
        ]
    }
    findings_c2 = agent.audit([slide_c2])
    assert len(findings_c2) >= 1 and any("tuyệt đối" in f.issue.lower() or "100%" in f.issue.lower() for f in findings_c2), "Case 2 Failed: 'bảo mật tuyệt đối' missed"
    print("✔ [PASSED] Case 2 (Absolute Security Claim 'bảo mật tuyệt đối' - P1 Caught)")
    passed += 1

    # CASE 3: Unrealistic "100% khách hàng hài lòng" (P1)
    slide_c3 = {
        "slide_id": "c3",
        "title": "Chỉ số tin cậy dịch vụ",
        "content_items": [
            {"body": "Khảo sát cho thấy 100% khách hàng hài lòng sau 3 tháng triển khai dịch vụ."}
        ]
    }
    findings_c3 = agent.audit([slide_c3])
    assert len(findings_c3) >= 1 and any("100%" in f.issue.lower() or "hài lòng" in f.issue.lower() for f in findings_c3), "Case 3 Failed: '100% khách hàng hài lòng' missed"
    print("✔ [PASSED] Case 3 (Unrealistic '100% khách hàng hài lòng' - P1 Caught)")
    passed += 1

    # CASE 4: English "100% secure and zero risk" (P1)
    slide_c4 = {
        "slide_id": "c4",
        "title": "Cloud Infrastructure",
        "content_items": [
            {"body": "Our cloud environment is 100% secure with zero risk of data exposure."}
        ]
    }
    findings_c4 = agent.audit([slide_c4])
    assert len(findings_c4) >= 1 and any("secure" in f.issue.lower() or "risk" in f.issue.lower() or "tuyệt đối" in f.issue.lower() or "chủ quan" in f.issue.lower() for f in findings_c4), "Case 4 Failed: English '100% secure / zero risk' missed"
    print("✔ [PASSED] Case 4 (English '100% Secure / Zero Risk' - P1 Caught)")
    passed += 1

    # CASE 5: English "undisputed market leader" without proof (P1)
    slide_c5 = {
        "slide_id": "c5",
        "title": "Market Positioning",
        "content_items": [
            {"body": "We stand as the undisputed market leader across all digital retail touchpoints."}
        ]
    }
    findings_c5 = agent.audit([slide_c5])
    assert len(findings_c5) >= 1 and any("leader" in f.issue.lower() or "chủ quan" in f.issue.lower() or "kiểm chứng" in f.issue.lower() for f in findings_c5), "Case 5 Failed: English 'undisputed market leader' missed"
    print("✔ [PASSED] Case 5 (English 'Undisputed Market Leader' - P1 Caught)")
    passed += 1

    # CASE 6: Valid Citation from Gartner (Valid - No False Positive)
    slide_c6 = {
        "slide_id": "c6",
        "title": "Đánh giá của tổ chức độc lập",
        "content_items": [
            {"body": "Theo báo cáo Magic Quadrant của Gartner 2024, giải pháp được vinh danh trong nhóm dẫn đầu thị trường."}
        ]
    }
    findings_c6 = agent.audit([slide_c6])
    assert len(findings_c6) == 0, f"Case 6 Failed: False positive on Gartner citation: {[f.issue for f in findings_c6]}"
    print("✔ [PASSED] Case 6 (Empirical Gartner Citation - No False Positive)")
    passed += 1

    # CASE 7: Valid Citation from GSO (General Statistics Office) (Valid - No False Positive)
    slide_c7 = {
        "slide_id": "c7",
        "title": "Tăng trưởng vĩ mô",
        "content_items": [
            {"body": "Theo số liệu của Tổng cục Thống kê (GSO), quy mô nền kinh tế thuộc top đầu khu vực Đông Nam Á."}
        ]
    }
    findings_c7 = agent.audit([slide_c7])
    assert len(findings_c7) == 0, f"Case 7 Failed: False positive on GSO citation: {[f.issue for f in findings_c7]}"
    print("✔ [PASSED] Case 7 (Official GSO Citation - No False Positive)")
    passed += 1

    # CASE 8: Defensible corporate prose with ISO / SOC standards (Valid - No False Positive)
    slide_c8 = {
        "slide_id": "c8",
        "title": "Chứng chỉ tiêu chuẩn vận hành",
        "content_items": [
            {"body": "Hạ tầng tuân thủ nghiêm ngặt các khung bảo mật tiêu chuẩn quốc tế ISO 27001 và SOC 2 Type II."}
        ]
    }
    findings_c8 = agent.audit([slide_c8])
    assert len(findings_c8) == 0, f"Case 8 Failed: False positive on standard ISO compliance: {[f.issue for f in findings_c8]}"
    print("✔ [PASSED] Case 8 (Standard Compliance Prose - No False Positive)")
    passed += 1

    # CASE 9: Schema Robustness - Superlative in Cards Description
    slide_c9 = {
        "slide_id": "c9",
        "title": "Hệ thống tích hợp",
        "cards": [
            {"headline": "Hiệu suất tối đa", "description": "Hệ thống sở hữu tốc độ xử lý tốt nhất thị trường hiện nay."}
        ]
    }
    findings_c9 = agent.audit([slide_c9])
    assert len(findings_c9) >= 1 and any("tốt nhất" in f.issue.lower() for f in findings_c9), "Case 9 Failed: Superlative in cards/description missed"
    print("✔ [PASSED] Case 9 (Schema Robustness Cards Description - Caught)")
    passed += 1

    # CASE 10: Auto-Remediation into Defensible Phrasing
    slide_c10 = {
        "slide_id": "c10",
        "title": "Năng lực công nghệ",
        "content_items": [
            {"body": "Giải pháp bảo mật tuyệt đối với vị thế số 1 thị trường."}
        ]
    }
    findings_c10 = agent.audit([slide_c10])
    assert len(findings_c10) >= 2, f"Case 10 Failed: Expected findings for remediation, got {len(findings_c10)}"
    remediated = agent.auto_remediate([slide_c10], findings_c10)
    rem_text = agent.extract_slide_text(remediated[0])
    assert "tuyệt đối" not in rem_text.lower(), f"Remediation left 'tuyệt đối': {rem_text}"
    assert "số 1 thị trường" not in rem_text.lower(), f"Remediation left 'số 1 thị trường': {rem_text}"
    re_audit = agent.audit(remediated)
    assert len(re_audit) == 0, f"Case 10 Failed: Re-audit found residual superlatives: {[f.issue for f in re_audit]}"
    print("✔ [PASSED] Case 10 (Auto-Remediation Into Defensible Phrasing - Passed)")
    passed += 1

    print("-" * 60)
    print(f"Total Score: {passed}/{total} ({passed/total*100:.1f}%)")
    print("=" * 60)
    assert passed == total, f"Adversarial matrix failed: {passed}/{total}"


if __name__ == "__main__":
    test_agent09_adversarial_matrix()

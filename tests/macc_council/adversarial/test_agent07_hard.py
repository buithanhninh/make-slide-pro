"""
tests/macc_council/adversarial/test_agent07_hard.py
Adversarial Stress Test Matrix for Agent 07: NaturalLanguagePurist.
Validates AI cliché detection (VN & EN), lazy ellipsis policing, math ellipsis shielding, and auto-remediation.
"""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from scripts.macc_council.gate3_micro_pedagogy.agent07_natural_language import NaturalLanguagePurist
from scripts.macc_council.models import Severity


def test_agent07_adversarial_matrix():
    print("=" * 60)
    print("RUNNING ADVERSARIAL STRESS TEST MATRIX FOR AGENT 07")
    print("=" * 60)

    agent = NaturalLanguagePurist()
    passed = 0
    total = 10

    # CASE 1: Vietnamese AI cliché (kỷ nguyên số ngày nay)
    slide_c1 = {
        "slide_id": "c1",
        "title": "Chuyển đổi số doanh nghiệp",
        "content_items": [
            {"body": "Trong kỷ nguyên số ngày nay, các doanh nghiệp bắt buộc phải tái cấu trúc mô hình vận hành."}
        ]
    }
    findings_c1 = agent.audit([slide_c1])
    assert len(findings_c1) >= 1 and any("kỷ nguyên số" in f.issue.lower() for f in findings_c1), "Case 1 Failed: 'kỷ nguyên số ngày nay' missed"
    print("✔ [PASSED] Case 1 (Vietnamese AI Cliché 'kỷ nguyên số' - Caught)")
    passed += 1

    # CASE 2: Vietnamese filler fluff (không thể phủ nhận + đóng vai trò vô cùng quan trọng)
    slide_c2 = {
        "slide_id": "c2",
        "title": "Vai trò của dữ liệu",
        "content_items": [
            {"body": "Không thể phủ nhận rằng dữ liệu đóng vai trò vô cùng quan trọng trong việc định hướng kinh doanh."}
        ]
    }
    findings_c2 = agent.audit([slide_c2])
    assert len(findings_c2) >= 2, f"Case 2 Failed: Expected at least 2 findings, got {len(findings_c2)}"
    print("✔ [PASSED] Case 2 (Vietnamese Compound Filler Fluff - Multiple Caught)")
    passed += 1

    # CASE 3: English AI boilerplate (in today's rapidly changing world + delve into)
    slide_c3 = {
        "slide_id": "c3",
        "title": "Strategic Roadmap",
        "content_items": [
            {"body": "In today's rapidly changing world, let's delve into the operational transformation roadmap."}
        ]
    }
    findings_c3 = agent.audit([slide_c3])
    assert len(findings_c3) >= 1 and any("delve into" in f.issue.lower() or "rapidly changing" in f.issue.lower() or "cliché" in f.issue.lower() for f in findings_c3), "Case 3 Failed: English AI boilerplate missed"
    print("✔ [PASSED] Case 3 (English AI Boilerplate 'delve into / rapidly changing' - Caught)")
    passed += 1

    # CASE 4: English buzzwords (game changer + testament to)
    slide_c4 = {
        "slide_id": "c4",
        "title": "Platform Impact",
        "content_items": [
            {"body": "This new feature is an absolute game changer and a testament to our engineering excellence."}
        ]
    }
    findings_c4 = agent.audit([slide_c4])
    assert len(findings_c4) >= 1 and any("game changer" in f.issue.lower() or "testament to" in f.issue.lower() or "cliché" in f.issue.lower() for f in findings_c4), "Case 4 Failed: English buzzwords missed"
    print("✔ [PASSED] Case 4 (English Buzzwords 'game changer / testament to' - Caught)")
    passed += 1

    # CASE 5: Lazy trailing ellipsis (v.v... and ...)
    slide_c5 = {
        "slide_id": "c5",
        "title": "Danh mục giải pháp",
        "content_items": [
            {"body": "Các giải pháp bao gồm: tự động hóa kho bãi, kiểm soát chuỗi cung ứng, v.v..."}
        ]
    }
    findings_c5 = agent.audit([slide_c5])
    assert len(findings_c5) >= 1 and any("chấm lửng" in f.issue.lower() or "ellipsis" in f.issue.lower() for f in findings_c5), "Case 5 Failed: Lazy ellipsis missed"
    print("✔ [PASSED] Case 5 (Lazy Trailing Ellipsis - Caught)")
    passed += 1

    # CASE 6: Math ellipsis inside LaTeX (Valid - No False Positive)
    slide_c6 = {
        "slide_id": "c6",
        "title": "Chuỗi tính tổng",
        "content_items": [
            {"body": r"Công thức chuỗi hữu hạn: $S_n = x_1 + x_2 + \dots + x_n$ với $n \ge 1$."}
        ]
    }
    findings_c6 = agent.audit([slide_c6])
    assert len(findings_c6) == 0, f"Case 6 Failed: False positive on math ellipsis inside LaTeX: {[f.issue for f in findings_c6]}"
    print("✔ [PASSED] Case 6 (Math Ellipsis in LaTeX - No False Positive)")
    passed += 1

    # CASE 7: Policy document citing Industry 4.0 (Valid - No False Positive)
    slide_c7 = {
        "slide_id": "c7",
        "title": "Căn cứ pháp lý",
        "content_items": [
            {"body": "Căn cứ Nghị quyết số 52-NQ/TW của Bộ Chính trị về một số chủ trương tham gia cuộc Cách mạng công nghiệp lần thứ tư."}
        ]
    }
    findings_c7 = agent.audit([slide_c7])
    assert len(findings_c7) == 0, f"Case 7 Failed: False positive on official government policy title: {[f.issue for f in findings_c7]}"
    print("✔ [PASSED] Case 7 (Official Government Policy Title - No False Positive)")
    passed += 1

    # CASE 8: Clean concise action-oriented business prose (Valid - No False Positive)
    slide_c8 = {
        "slide_id": "c8",
        "title": "Tối ưu hóa logistics",
        "content_items": [
            {"body": "Cắt giảm 25% thời gian xử lý đơn hàng và tiết kiệm 12 tỷ đồng chi phí lưu kho trong năm 2024."}
        ]
    }
    findings_c8 = agent.audit([slide_c8])
    assert len(findings_c8) == 0, f"Case 8 Failed: False positive on clean business prose: {[f.issue for f in findings_c8]}"
    print("✔ [PASSED] Case 8 (Clean Action-Oriented Business Prose - No False Positive)")
    passed += 1

    # CASE 9: Schema Agnostic Card Extraction
    slide_c9 = {
        "slide_id": "c9",
        "title": "Tổng quan sáng kiến",
        "cards": [
            {"headline": "Hành trình vươn mình", "description": "Thời đại 4.0 mở ra nhiều thách thức mới cho các phòng ban."}
        ]
    }
    findings_c9 = agent.audit([slide_c9])
    assert len(findings_c9) >= 2, f"Case 9 Failed: Expected cards/headline & cards/description clichés caught, got {len(findings_c9)}"
    print("✔ [PASSED] Case 9 (Schema Agnostic Card Cliché Extraction - Caught)")
    passed += 1

    # CASE 10: Auto-Remediation Cleanses Clichés & Passes Re-Audit
    slide_c10 = {
        "slide_id": "c10",
        "title": "Kế hoạch quý 4",
        "content_items": [
            {"body": "Trong kỷ nguyên số ngày nay, chúng ta cần hành động nhanh chóng... Không thể phủ nhận rằng dữ liệu rất quan trọng."}
        ]
    }
    findings_c10 = agent.audit([slide_c10])
    assert len(findings_c10) >= 2, f"Case 10 Failed: Expected findings for remediation, got {len(findings_c10)}"
    remediated = agent.auto_remediate([slide_c10], findings_c10)
    rem_text = agent.extract_slide_text(remediated[0])
    assert "kỷ nguyên số" not in rem_text.lower(), f"Remediation left 'kỷ nguyên số': {rem_text}"
    assert "không thể phủ nhận" not in rem_text.lower(), f"Remediation left 'không thể phủ nhận': {rem_text}"
    assert "..." not in rem_text, f"Remediation left ellipsis: {rem_text}"
    re_audit = agent.audit(remediated)
    assert len(re_audit) == 0, f"Case 10 Failed: Re-audit of remediated text found residual clichés: {[f.issue for f in re_audit]}"
    print("✔ [PASSED] Case 10 (Auto-Remediation Cleanses Clichés & Passes Re-Audit)")
    passed += 1

    print("-" * 60)
    print(f"Total Score: {passed}/{total} ({passed/total*100:.1f}%)")
    print("=" * 60)
    assert passed == total, f"Adversarial matrix failed: {passed}/{total}"


if __name__ == "__main__":
    test_agent07_adversarial_matrix()

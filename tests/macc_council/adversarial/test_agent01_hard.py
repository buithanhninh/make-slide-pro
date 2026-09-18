"""
tests/macc_council/adversarial/test_agent01_hard.py
Adversarial Stress Test Matrix for Agent 01: SourceFidelityFactChecker.
10 ruthless edge cases testing:
1. Entity-Metric Misattribution (Tráo đổi chủ thể)
2. Polarity Inversion (Đảo chiều tăng/giảm)
3. Base Rate Fallacy (Lệch mẫu số so sánh QoQ vs YoY)
4. Temporal Drift (Biến dự báo 2030 thành hiện thực 2024)
5. Valid Rounding Tolerance (Làm tròn hợp lệ không được báo lỗi giả)
6. Pure Hallucination (Số liệu bịa đặt hoàn toàn)
7. Qualitative Distortion (Bóp méo tính chất tăng nhẹ thành tăng phi mã)
8. Unit Conversion (Quy đổi 2,4 tỷ = 2.400 triệu không báo lỗi giả)
9. Table/Annex Extraction (Số liệu nằm trong bảng phụ lục)
10. Invented Arithmetic Sum (Tự tính tổng sai lệch)
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from scripts.macc_council.gate1_source_privacy import SourceFidelityFactChecker
from scripts.macc_council.models import Severity


def run_all_adversarial_tests():
    agent = SourceFidelityFactChecker()
    results = {}

    # ----------------------------------------------------
    # Case 1: Entity-Metric Misattribution
    # ----------------------------------------------------
    source_1 = "Năm 2024, doanh thu mảng xe điện của VinFast đạt 1,2 tỷ USD, trong khi mảng bất động sản của Vinhomes đạt 3,8 tỷ USD."
    slide_1 = {
        "slide_id": "case_1",
        "assertion_title": "Doanh thu mảng xe điện VinFast năm 2024 đạt 3,8 tỷ USD",
        "primary_claim": "Tăng trưởng vượt bậc của xe điện VinFast."
    }
    findings_1 = agent.audit(slide_1, context={"source_text": source_1})
    p0_1 = [f for f in findings_1 if f.severity == Severity.P0 or "thực thể" in f.issue.lower() or "misattribution" in f.issue.lower() or "3,8" in f.issue]
    results["Case 1 (Entity Misattribution)"] = len(p0_1) > 0

    # ----------------------------------------------------
    # Case 2: Polarity Inversion (Tăng <-> Giảm)
    # ----------------------------------------------------
    source_2 = "Nhờ tối ưu quy trình, chi phí vận hành năm 2024 giảm 14.5% so với năm trước."
    slide_2 = {
        "slide_id": "case_2",
        "assertion_title": "Chi phí vận hành năm 2024 tăng 14.5%",
        "primary_claim": "Ghi nhận mức biến động chi phí trong năm."
    }
    findings_2 = agent.audit(slide_2, context={"source_text": source_2})
    polarity_findings = [f for f in findings_2 if "đảo chiều" in f.issue.lower() or "tăng" in f.issue.lower() or "giảm" in f.issue.lower() or f.severity == Severity.P0]
    results["Case 2 (Polarity Inversion)"] = len(polarity_findings) > 0

    # ----------------------------------------------------
    # Case 3: Base Rate Fallacy (QoQ vs YoY)
    # ----------------------------------------------------
    source_3 = "Lợi nhuận ròng quý 3 đạt 450 tỷ, tăng 22% so với quý trước."
    slide_3 = {
        "slide_id": "case_3",
        "assertion_title": "Lợi nhuận ròng quý 3 tăng 22% so với cùng kỳ năm trước",
        "primary_claim": "Hiệu quả kinh doanh tích cực."
    }
    findings_3 = agent.audit(slide_3, context={"source_text": source_3})
    base_rate_findings = [f for f in findings_3 if "mẫu số" in f.issue.lower() or "cùng kỳ" in f.issue.lower() or "quý trước" in f.issue.lower() or f.severity in [Severity.P0, Severity.P1]]
    results["Case 3 (Base Rate Fallacy)"] = len(base_rate_findings) > 0

    # ----------------------------------------------------
    # Case 4: Temporal Drift (2030 goal -> 2024 achieved)
    # ----------------------------------------------------
    source_4 = "Mục tiêu chiến lược đến năm 2030 Việt Nam đào tạo được 50.000 kỹ sư bán dẫn."
    slide_4 = {
        "slide_id": "case_4",
        "assertion_title": "Đến năm 2024 Việt Nam đã đào tạo được 50.000 kỹ sư bán dẫn",
        "primary_claim": "Nguồn nhân lực chất lượng cao sẵn sàng."
    }
    findings_4 = agent.audit(slide_4, context={"source_text": source_4})
    temporal_findings = [f for f in findings_4 if "mốc thời gian" in f.issue.lower() or "dự báo" in f.issue.lower() or "2024" in f.issue or f.severity in [Severity.P0, Severity.P1]]
    results["Case 4 (Temporal Drift)"] = len(temporal_findings) > 0

    # ----------------------------------------------------
    # Case 5: Valid Rounding Tolerance (NO FALSE POSITIVE)
    # ----------------------------------------------------
    source_5 = "Tỷ lệ phổ cập giáo dục trung học đạt 87.64% trên toàn quốc."
    slide_5 = {
        "slide_id": "case_5",
        "assertion_title": "Tỷ lệ phổ cập giáo dục trung học đạt khoảng 87.6%",
        "primary_claim": "Nâng cao dân trí toàn diện."
    }
    findings_5 = agent.audit(slide_5, context={"source_text": source_5})
    # Must NOT report error for valid rounding
    results["Case 5 (Rounding Tolerance - No False Positive)"] = (len(findings_5) == 0)

    # ----------------------------------------------------
    # Case 6: Pure Hallucination
    # ----------------------------------------------------
    source_6 = "Quy mô thị trường thương mại điện tử Việt Nam đạt 20,5 tỷ USD năm 2023."
    slide_6 = {
        "slide_id": "case_6",
        "assertion_title": "Quy mô thị trường thương mại điện tử đạt 99,9 tỷ USD",
        "primary_claim": "Tăng trưởng vượt bậc."
    }
    findings_6 = agent.audit(slide_6, context={"source_text": source_6})
    hallucination_findings = [f for f in findings_6 if f.severity == Severity.P0 and ("99,9" in f.issue or "ảo giác" in f.issue.lower())]
    results["Case 6 (Pure Hallucination Detection)"] = len(hallucination_findings) > 0

    # ----------------------------------------------------
    # Case 7: Qualitative Distortion (Tăng nhẹ -> Tăng phi mã)
    # ----------------------------------------------------
    source_7 = "Chỉ số CPI tháng 8 tăng nhẹ 0.15% so với tháng 7."
    slide_7 = {
        "slide_id": "case_7",
        "assertion_title": "Chỉ số CPI tháng 8 tăng phi mã 0.15% gây bất ổn thị trường",
        "primary_claim": "Áp lực lạm phát đè nặng."
    }
    findings_7 = agent.audit(slide_7, context={"source_text": source_7})
    qual_findings = [f for f in findings_7 if "bóp méo" in f.issue.lower() or "phi mã" in f.issue.lower() or "tăng nhẹ" in f.issue.lower() or f.severity in [Severity.P0, Severity.P1]]
    results["Case 7 (Qualitative Distortion)"] = len(qual_findings) > 0

    # ----------------------------------------------------
    # Case 8: Unit Conversion (2,4 tỷ == 2.400 triệu - NO FALSE POSITIVE)
    # ----------------------------------------------------
    source_8 = "Tổng vốn đầu tư đăng ký đạt 2,4 tỷ USD."
    slide_8 = {
        "slide_id": "case_8",
        "assertion_title": "Tổng vốn đầu tư đăng ký đạt 2.400 triệu USD",
        "primary_claim": "Thu hút dòng vốn FDI mạnh mẽ."
    }
    findings_8 = agent.audit(slide_8, context={"source_text": source_8})
    results["Case 8 (Unit Conversion - No False Positive)"] = (len(findings_8) == 0)

    # ----------------------------------------------------
    # Case 9: Table/Annex Data Extraction (Valid data)
    # ----------------------------------------------------
    source_9 = "Phụ lục bảng số 4: Tỷ lệ thâm nhập internet nông thôn là 68.2%, thành thị là 84.5%."
    slide_9 = {
        "slide_id": "case_9",
        "assertion_title": "Tỷ lệ thâm nhập internet khu vực nông thôn đạt 68.2%",
        "primary_claim": "Phổ cập hạ tầng số."
    }
    findings_9 = agent.audit(slide_9, context={"source_text": source_9})
    results["Case 9 (Table/Annex Extraction)"] = (len(findings_9) == 0)

    # ----------------------------------------------------
    # Case 10: Invented Arithmetic Sum (300 + 500 = 800 != 950)
    # ----------------------------------------------------
    source_10 = "Doanh thu chi nhánh miền Bắc đạt 300 tỷ VNĐ, chi nhánh miền Nam đạt 500 tỷ VNĐ."
    slide_10 = {
        "slide_id": "case_10",
        "assertion_title": "Tổng doanh thu hai miền đạt 950 tỷ VNĐ",
        "primary_claim": "Vượt mức kỳ vọng năm."
    }
    findings_10 = agent.audit(slide_10, context={"source_text": source_10})
    arith_findings = [f for f in findings_10 if "950" in f.issue or f.severity == Severity.P0]
    results["Case 10 (Invented Arithmetic Sum)"] = len(arith_findings) > 0

    return results


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING ADVERSARIAL STRESS TEST MATRIX FOR AGENT 01")
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

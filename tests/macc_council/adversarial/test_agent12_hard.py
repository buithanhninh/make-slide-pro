"""
tests/macc_council/adversarial/test_agent12_hard.py
Adversarial Stress Test Matrix for Agent 12: DataChartCartographer.
Validates chart series integrity, deep data emptiness, unit labeling, 100% pie/donut summation, and auto-remediation.
"""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from scripts.macc_council.gate4_spatial_motion.agent12_data_chart import DataChartCartographer
from scripts.macc_council.models import Severity


def test_agent12_adversarial_matrix():
    print("=" * 60)
    print("RUNNING ADVERSARIAL STRESS TEST MATRIX FOR AGENT 12")
    print("=" * 60)

    agent = DataChartCartographer()
    passed = 0
    total = 10

    # CASE 1: Empty chart data (P0)
    slide_c1 = {
        "slide_id": "c1",
        "title": "Tăng trưởng doanh thu",
        "chart": {
            "type": "bar_vertical",
            "unit": "Tỷ VNĐ",
            "series": [],
            "data": []
        }
    }
    findings_c1 = agent.audit([slide_c1])
    assert len(findings_c1) >= 1 and any(f.severity == Severity.P0 and "thiếu dữ liệu" in f.issue.lower() for f in findings_c1), "Case 1 Failed: Empty chart data not caught as P0"
    print("✔ [PASSED] Case 1 (Empty Chart Data - P0 Caught)")
    passed += 1

    # CASE 2: Deeply empty series data (P0)
    slide_c2 = {
        "slide_id": "c2",
        "title": "Lợi nhuận theo quý",
        "chart": {
            "type": "line",
            "unit": "Tỷ VNĐ",
            "series": [
                {"name": "2024", "data": []}
            ]
        }
    }
    findings_c2 = agent.audit([slide_c2])
    assert len(findings_c2) >= 1 and any(f.severity == Severity.P0 and "thiếu dữ liệu" in f.issue.lower() for f in findings_c2), "Case 2 Failed: Deeply empty series data missed"
    print("✔ [PASSED] Case 2 (Deeply Empty Series Data - P0 Caught)")
    passed += 1

    # CASE 3: Missing measurement unit on bar chart (P1)
    slide_c3 = {
        "slide_id": "c3",
        "title": "Sản lượng sản xuất",
        "chart": {
            "type": "bar_vertical",
            "data": [100, 150, 220, 300]
        }
    }
    findings_c3 = agent.audit([slide_c3])
    assert len(findings_c3) >= 1 and any("thiếu đơn vị" in f.issue.lower() for f in findings_c3), "Case 3 Failed: Missing measurement unit missed"
    print("✔ [PASSED] Case 3 (Missing Measurement Unit - P1 Caught)")
    passed += 1

    # CASE 4: Valid bar chart with unit and data (Valid - No False Positive)
    slide_c4 = {
        "slide_id": "c4",
        "title": "Doanh thu theo vùng miền",
        "chart": {
            "type": "bar_vertical",
            "unit": "Tỷ VNĐ",
            "data": [
                {"label": "Miền Bắc", "value": 450},
                {"label": "Miền Nam", "value": 620},
                {"label": "Miền Trung", "value": 280}
            ]
        }
    }
    findings_c4 = agent.audit([slide_c4])
    assert len(findings_c4) == 0, f"Case 4 Failed: False positive on valid bar chart: {[f.issue for f in findings_c4]}"
    print("✔ [PASSED] Case 4 (Valid Bar Chart with Unit & Data - No False Positive)")
    passed += 1

    # CASE 5: Pie chart with numeric array summing to 125% (P0)
    slide_c5 = {
        "slide_id": "c5",
        "title": "Cơ cấu thị phần",
        "chart": {
            "type": "pie",
            "unit": "%",
            "data": [50.0, 45.0, 30.0]  # Sum = 125.0%
        }
    }
    findings_c5 = agent.audit([slide_c5])
    assert len(findings_c5) >= 1 and any(f.severity == Severity.P0 and "100%" in f.issue for f in findings_c5), "Case 5 Failed: Pie summing to 125% missed"
    print("✔ [PASSED] Case 5 (Pie Summing to 125% - P0 Caught)")
    passed += 1

    # CASE 6: Donut chart with dict array summing to 70% (P0)
    slide_c6 = {
        "slide_id": "c6",
        "title": "Cơ cấu chi phí vận hành",
        "chart": {
            "type": "donut",
            "unit": "%",
            "data": [
                {"label": "Nhân sự", "value": 40.0},
                {"label": "Thuê mặt bằng", "value": 30.0}
            ]  # Sum = 70.0%
        }
    }
    findings_c6 = agent.audit([slide_c6])
    assert len(findings_c6) >= 1 and any(f.severity == Severity.P0 and "100%" in f.issue for f in findings_c6), "Case 6 Failed: Donut summing to 70% missed"
    print("✔ [PASSED] Case 6 (Donut Dict Array Summing to 70% - P0 Caught)")
    passed += 1

    # CASE 7: Valid Donut chart summing to 100% (Valid - No False Positive)
    slide_c7 = {
        "slide_id": "c7",
        "title": "Phân bổ danh mục đầu tư",
        "chart": {
            "type": "donut",
            "unit": "%",
            "data": [
                {"label": "Cổ phiếu", "value": 55.0},
                {"label": "Trái phiếu", "value": 35.0},
                {"label": "Tiền mặt", "value": 10.0}
            ]  # Sum = 100.0%
        }
    }
    findings_c7 = agent.audit([slide_c7])
    assert len(findings_c7) == 0, f"Case 7 Failed: False positive on valid donut: {[f.issue for f in findings_c7]}"
    print("✔ [PASSED] Case 7 (Valid Donut Summing to 100% - No False Positive)")
    passed += 1

    # CASE 8: Time-series abuse in Pie Chart (P1)
    slide_c8 = {
        "slide_id": "c8",
        "title": "Xu hướng doanh số qua các năm",
        "chart": {
            "type": "pie",
            "unit": "%",
            "data": [
                {"label": f"Năm {year}", "value": 12.5} for year in range(2017, 2025)
            ]
        }
    }
    findings_c8 = agent.audit([slide_c8])
    assert len(findings_c8) >= 1 and any("chuỗi thời gian" in f.issue.lower() or "line" in f.suggested_value.lower() or "thời gian" in f.issue.lower() or "clutter" in f.issue.lower() for f in findings_c8), "Case 8 Failed: Time-series in pie chart missed"
    print("✔ [PASSED] Case 8 (Time-Series Abuse in Pie Chart - P1 Caught)")
    passed += 1

    # CASE 9: Pie chart slice clutter (> 7 slices) (P1)
    slide_c9 = {
        "slide_id": "c9",
        "title": "Phân bổ doanh số theo 9 nhóm sản phẩm",
        "chart": {
            "type": "pie",
            "unit": "%",
            "data": [
                {"label": f"Nhóm {i}", "value": 11.1} for i in range(1, 10)
            ]
        }
    }
    findings_c9 = agent.audit([slide_c9])
    assert len(findings_c9) >= 1 and any("quá nhiều" in f.issue.lower() or "clutter" in f.issue.lower() or "lát cắt" in f.issue.lower() for f in findings_c9), "Case 9 Failed: Pie chart clutter (>7 slices) missed"
    print("✔ [PASSED] Case 9 (Pie Chart Clutter > 7 Slices - P1 Caught)")
    passed += 1

    # CASE 10: Auto-Remediation Normalizes Dict Array and Injects Missing Unit
    slide_c10 = {
        "slide_id": "c10",
        "title": "Cơ cấu doanh thu",
        "chart": {
            "type": "pie",
            "data": [
                {"label": "Bán lẻ", "value": 50.0},
                {"label": "Bán buôn", "value": 30.0}
            ]
        }
    }
    findings_c10 = agent.audit([slide_c10])
    assert len(findings_c10) >= 2, f"Case 10 Failed: Expected at least 2 findings, got {len(findings_c10)}"
    remediated = agent.auto_remediate([slide_c10], findings_c10)
    rem_chart = remediated[0]["chart"]
    assert rem_chart.get("unit") == "%", f"Unit not injected: {rem_chart.get('unit')}"
    # Verify dict values sum to 100.0%
    values = [d["value"] for d in rem_chart["data"]]
    assert abs(sum(values) - 100.0) < 0.2, f"Normalized values do not sum to 100%: {values} (sum={sum(values)})"
    re_audit = agent.audit(remediated)
    assert len(re_audit) == 0, f"Case 10 Failed: Residual issues after remediation: {[f.issue for f in re_audit]}"
    print("✔ [PASSED] Case 10 (Auto-Remediation Normalizes Dict Array & Injects Unit)")
    passed += 1

    print("-" * 60)
    print(f"Total Score: {passed}/{total} ({passed/total*100:.1f}%)")
    print("=" * 60)
    assert passed == total, f"Adversarial matrix failed: {passed}/{total}"


if __name__ == "__main__":
    test_agent12_adversarial_matrix()

"""
tests/macc_council/adversarial/test_agent11_hard.py
Adversarial Stress Test Matrix for Agent 11: LayoutArchetypeStrategist.
Validates archetype-to-atom fit, schema-agnostic counting, semantic archetype alignment, and auto-remediation.
"""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from scripts.macc_council.gate4_spatial_motion.agent11_layout_archetype import LayoutArchetypeStrategist
from scripts.macc_council.models import Severity


def test_agent11_adversarial_matrix():
    print("=" * 60)
    print("RUNNING ADVERSARIAL STRESS TEST MATRIX FOR AGENT 11")
    print("=" * 60)

    agent = LayoutArchetypeStrategist()
    passed = 0
    total = 10

    # CASE 1: Atom count mismatch - split_comparison with 4 atoms (P1)
    slide_c1 = {
        "slide_id": "c1",
        "assertion_title": "So sánh các mô hình vận hành",
        "archetype": "split_comparison",
        "atoms": [
            {"title": f"Mô hình {i}", "text": f"Mô tả {i}"} for i in range(1, 5)
        ]
    }
    findings_c1 = agent.audit([slide_c1])
    assert len(findings_c1) >= 1 and any("không tương thích" in f.issue.lower() for f in findings_c1), "Case 1 Failed: split_comparison with 4 atoms missed"
    print("✔ [PASSED] Case 1 (split_comparison with 4 Atoms Overload - P1 Caught)")
    passed += 1

    # CASE 2: Atom count mismatch - grid_2x2 with only 1 atom (P1)
    slide_c2 = {
        "slide_id": "c2",
        "assertion_title": "Định hướng trọng tâm duy nhất",
        "archetype": "grid_2x2",
        "atoms": [
            {"title": "Mục tiêu 1", "text": "Mô tả nội dung"}
        ]
    }
    findings_c2 = agent.audit([slide_c2])
    assert len(findings_c2) >= 1 and any("không tương thích" in f.issue.lower() for f in findings_c2), "Case 2 Failed: grid_2x2 with 1 atom missed"
    print("✔ [PASSED] Case 2 (grid_2x2 with 1 Atom Vacuum - P1 Caught)")
    passed += 1

    # CASE 3: Schema-agnostic cards count - 3_cards with 3 cards (Valid - No False Positive)
    slide_c3 = {
        "slide_id": "c3",
        "title": "Ba giải pháp chiến lược",
        "archetype": "3_cards",
        "cards": [
            {"headline": f"Giải pháp {i}", "description": f"Mô tả {i}"} for i in range(1, 4)
        ]
    }
    findings_c3 = agent.audit([slide_c3])
    assert len(findings_c3) == 0, f"Case 3 Failed: False positive on valid 3_cards schema: {[f.issue for f in findings_c3]}"
    print("✔ [PASSED] Case 3 (Schema-Agnostic 3_cards with Cards - No False Positive)")
    passed += 1

    # CASE 4: Schema-agnostic content_items - grid_2x2 with 4 items (Valid - No False Positive)
    slide_c4 = {
        "slide_id": "c4",
        "title": "Bốn trụ cột chuyển đổi",
        "archetype": "grid_2x2",
        "content_items": [
            {"title": f"Trụ cột {i}", "body": f"Nội dung {i}"} for i in range(1, 5)
        ]
    }
    findings_c4 = agent.audit([slide_c4])
    assert len(findings_c4) == 0, f"Case 4 Failed: False positive on valid grid_2x2 content_items: {[f.issue for f in findings_c4]}"
    print("✔ [PASSED] Case 4 (Schema-Agnostic grid_2x2 with Content Items - No False Positive)")
    passed += 1

    # CASE 5: Semantic Mismatch - Chronological process labeled as split_comparison (P1)
    slide_c5 = {
        "slide_id": "c5",
        "assertion_title": "Quy trình triển khai dự án qua 4 bước nối tiếp",
        "archetype": "split_comparison",
        "atoms": [
            {"title": f"Bước {i}", "text": f"Giai đoạn thực thi bước {i}"} for i in range(1, 5)
        ]
    }
    findings_c5 = agent.audit([slide_c5])
    assert len(findings_c5) >= 1 and any("process" in f.suggested_value.lower() or "quy trình" in f.issue.lower() or "tương thích" in f.issue.lower() for f in findings_c5), "Case 5 Failed: Chronological process in split_comparison missed"
    print("✔ [PASSED] Case 5 (Semantic Process Mismatch - P1 Caught)")
    passed += 1

    # CASE 6: Semantic Mismatch - Comparison intent with 2 atoms placed in 3_cards (P1)
    slide_c6 = {
        "slide_id": "c6",
        "assertion_title": "So sánh ưu thế vượt trội giữa phương án A và phương án B",
        "archetype": "3_cards",
        "atoms": [
            {"title": "Phương án A", "text": "Mô hình truyền thống"},
            {"title": "Phương án B", "text": "Mô hình đổi mới"}
        ]
    }
    findings_c6 = agent.audit([slide_c6])
    assert len(findings_c6) >= 1 and any("split_comparison" in f.suggested_value.lower() or "tương thích" in f.issue.lower() for f in findings_c6), "Case 6 Failed: Comparison intent in 3_cards missed"
    print("✔ [PASSED] Case 6 (Comparison Intent in 3_cards - P1 Caught)")
    passed += 1

    # CASE 7: Title hero with 0 atoms (Valid - No False Positive)
    slide_c7 = {
        "slide_id": "c7",
        "title": "Báo cáo Toàn cảnh Thị trường 2025",
        "archetype": "title_hero"
    }
    findings_c7 = agent.audit([slide_c7])
    assert len(findings_c7) == 0, f"Case 7 Failed: False positive on title_hero: {[f.issue for f in findings_c7]}"
    print("✔ [PASSED] Case 7 (Title Hero with 0 Atoms - No False Positive)")
    passed += 1

    # CASE 8: Metric callout with 3 metric items (Valid - No False Positive)
    slide_c8 = {
        "slide_id": "c8",
        "assertion_title": "Chỉ số tài chính bứt phá trong quý 3",
        "archetype": "metric_callout_3x",
        "atoms": [
            {"title": "Doanh thu", "metric_value": "1.200 tỷ", "metric_label": "VNĐ"},
            {"title": "Lợi nhuận", "metric_value": "350 tỷ", "metric_label": "VNĐ"},
            {"title": "Biên lãi gộp", "metric_value": "29%", "metric_label": "%"}
        ]
    }
    findings_c8 = agent.audit([slide_c8])
    assert len(findings_c8) == 0, f"Case 8 Failed: False positive on metric_callout_3x: {[f.issue for f in findings_c8]}"
    print("✔ [PASSED] Case 8 (Metric Callout 3x - No False Positive)")
    passed += 1

    # CASE 9: Quote callout with 1 item (Valid - No False Positive)
    slide_c9 = {
        "slide_id": "c9",
        "assertion_title": "Thông điệp của Chủ tịch HĐQT",
        "archetype": "quote_callout",
        "atoms": [
            {"title": "Trích dẫn", "text": "Đổi mới sáng tạo là sức sống của tổ chức."}
        ]
    }
    findings_c9 = agent.audit([slide_c9])
    assert len(findings_c9) == 0, f"Case 9 Failed: False positive on quote_callout: {[f.issue for f in findings_c9]}"
    print("✔ [PASSED] Case 9 (Quote Callout with 1 Item - No False Positive)")
    passed += 1

    # CASE 10: Auto-Remediation Converts grid_2x2 (with 2 items) to split_comparison
    slide_c10 = {
        "slide_id": "c10",
        "title": "So sánh trước và sau triển khai",
        "archetype": "grid_2x2",
        "atoms": [
            {"title": "Trước triển khai", "text": "Thời gian xử lý 48 giờ"},
            {"title": "Sau triển khai", "text": "Thời gian xử lý 2 giờ"}
        ]
    }
    findings_c10 = agent.audit([slide_c10])
    assert len(findings_c10) >= 1, "Case 10 Failed: Expected findings for remediation"
    remediated = agent.auto_remediate([slide_c10], findings_c10)
    assert remediated[0]["archetype"] == "split_comparison", f"Remediation did not select split_comparison: {remediated[0]['archetype']}"
    re_audit = agent.audit(remediated)
    assert len(re_audit) == 0, f"Case 10 Failed: Re-audit found residual archetype errors: {[f.issue for f in re_audit]}"
    print("✔ [PASSED] Case 10 (Auto-Remediation Repairs Archetype & Passes Re-Audit)")
    passed += 1

    print("-" * 60)
    print(f"Total Score: {passed}/{total} ({passed/total*100:.1f}%)")
    print("=" * 60)
    assert passed == total, f"Adversarial matrix failed: {passed}/{total}"


if __name__ == "__main__":
    test_agent11_adversarial_matrix()

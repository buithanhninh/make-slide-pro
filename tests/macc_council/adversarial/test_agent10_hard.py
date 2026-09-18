"""
tests/macc_council/adversarial/test_agent10_hard.py
Adversarial Stress Test Matrix for Agent 10: MasterPedagogicalRewriter.
Validates pedagogical structure, schema-agnostic title detection, primary claim bridging, and self-healing synthesis.
"""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from scripts.macc_council.gate3_micro_pedagogy.agent10_master_rewriter import MasterPedagogicalRewriter
from scripts.macc_council.models import Severity


def test_agent10_adversarial_matrix():
    print("=" * 60)
    print("RUNNING ADVERSARIAL STRESS TEST MATRIX FOR AGENT 10")
    print("=" * 60)

    agent = MasterPedagogicalRewriter()
    passed = 0
    total = 10

    # CASE 1: Slide completely missing any title (P0)
    slide_c1 = {
        "slide_id": "c1",
        "archetype": "card_grid",
        "atoms": [
            {"title": "Mục 1", "text": "Nội dung chi tiết."}
        ]
    }
    findings_c1 = agent.audit([slide_c1])
    assert len(findings_c1) >= 1 and any(f.severity == Severity.P0 and "tiêu đề" in f.issue.lower() for f in findings_c1), "Case 1 Failed: Completely missing title not caught as P0"
    print("✔ [PASSED] Case 1 (Completely Missing Title - P0 Caught)")
    passed += 1

    # CASE 2: Slide with 'title' instead of 'assertion_title' (Valid Schema Agnostic - No False Positive P0)
    slide_c2 = {
        "slide_id": "c2",
        "title": "Mạng lưới phân phối mở rộng thêm 15 chi nhánh mới trên toàn quốc",
        "primary_claim": "Chiến lược phủ rộng điểm bán trực tiếp thúc đẩy sản lượng tiêu thụ quý 3.",
        "archetype": "card_grid",
        "atoms": [
            {"title": "Hà Nội", "text": "Khai trương 5 chi nhánh tại các quận trung tâm."}
        ]
    }
    findings_c2 = agent.audit([slide_c2])
    assert not any(f.severity == Severity.P0 for f in findings_c2), f"Case 2 Failed: False positive P0 on valid 'title': {[f.issue for f in findings_c2]}"
    print("✔ [PASSED] Case 2 (Schema-Agnostic 'title' Field - No False Positive P0)")
    passed += 1

    # CASE 3: Content slide missing primary_claim (P2)
    slide_c3 = {
        "slide_id": "c3",
        "assertion_title": "Tối ưu hóa logistics giúp cắt giảm 20% chi phí vận hành kho bãi",
        "archetype": "card_grid",
        "atoms": [
            {"title": "Tự động hóa", "text": "Triển khai robot AGV tại trung tâm phân loại hàng hóa."}
        ]
    }
    findings_c3 = agent.audit([slide_c3])
    assert len(findings_c3) >= 1 and any("primary_claim" in f.issue.lower() or "luận điểm" in f.issue.lower() for f in findings_c3), "Case 3 Failed: Missing primary_claim missed"
    print("✔ [PASSED] Case 3 (Missing Primary Claim on Content Slide - P2 Caught)")
    passed += 1

    # CASE 4: title_hero slide exempt from primary_claim requirement (Valid - No False Positive)
    slide_c4 = {
        "slide_id": "c4",
        "assertion_title": "Báo cáo Chiến lược Kinh doanh và Phát triển Bền vững 2025",
        "archetype": "title_hero"
    }
    findings_c4 = agent.audit([slide_c4])
    assert len(findings_c4) == 0, f"Case 4 Failed: False positive on title_hero slide: {[f.issue for f in findings_c4]}"
    print("✔ [PASSED] Case 4 (Title Hero Slide Exemption - No False Positive)")
    passed += 1

    # CASE 5: quote_callout slide exempt from primary_claim requirement (Valid - No False Positive)
    slide_c5 = {
        "slide_id": "c5",
        "assertion_title": "Lời khẳng định từ Tổng Giám đốc",
        "archetype": "quote_callout",
        "quote": "Chất lượng sản phẩm và sự hài lòng của khách hàng là thước đo cao nhất."
    }
    findings_c5 = agent.audit([slide_c5])
    assert len(findings_c5) == 0, f"Case 5 Failed: False positive on quote_callout slide: {[f.issue for f in findings_c5]}"
    print("✔ [PASSED] Case 5 (Quote Callout Slide Exemption - No False Positive)")
    passed += 1

    # CASE 6: Title ending with an improper period (P2 Hygiene)
    slide_c6 = {
        "slide_id": "c6",
        "assertion_title": "Lợi nhuận ròng tăng trưởng 35% so với cùng kỳ năm trước.",
        "primary_claim": "Động lực đến từ việc cắt giảm chi phí trung gian.",
        "archetype": "card_grid",
        "atoms": [{"title": "Q3", "text": "Chi tiết số liệu."}]
    }
    findings_c6 = agent.audit([slide_c6])
    assert len(findings_c6) >= 1 and any("chấm" in f.issue.lower() or "period" in f.issue.lower() or "kết thúc" in f.issue.lower() for f in findings_c6), "Case 6 Failed: Title ending with period missed"
    print("✔ [PASSED] Case 6 (Title Ending With Improper Period - P2 Caught)")
    passed += 1

    # CASE 7: Fully formed flawless pedagogical slide (Valid - No False Positive)
    slide_c7 = {
        "slide_id": "c7",
        "assertion_title": "Tăng cường đầu tư R&D tạo lập rào cản công nghệ vững chắc",
        "primary_claim": "Ngân sách nghiên cứu đạt 8% doanh thu giúp ra mắt 3 dòng sản phẩm mới.",
        "archetype": "card_grid",
        "atoms": [
            {"title": "Chip bán dẫn", "text": "Hoàn thiện thiết kế vi xử lý AI thế hệ thứ hai."},
            {"title": "Phần mềm", "text": "Tối ưu hóa thuật toán biên giảm 40% độ trễ xử lý."}
        ]
    }
    findings_c7 = agent.audit([slide_c7])
    assert len(findings_c7) == 0, f"Case 7 Failed: False positive on perfect pedagogical slide: {[f.issue for f in findings_c7]}"
    print("✔ [PASSED] Case 7 (Fully Formed Pedagogical Slide - No False Positive)")
    passed += 1

    # CASE 8: Schema Robustness with generic cards
    slide_c8 = {
        "slide_id": "c8",
        "title": "Chuyển dịch cơ cấu lao động thúc đẩy năng suất ngành chế biến chế tạo",
        "cards": [
            {"headline": "Đào tạo nghề", "description": "Tập trung nâng cao tay nghề kỹ thuật số."}
        ]
    }
    findings_c8 = agent.audit([slide_c8])
    # Should flag missing primary_claim (P2) but NOT missing title (P0)
    assert not any(f.severity == Severity.P0 for f in findings_c8), "Case 8 Failed: Wrongly flagged missing title on cards schema"
    assert any(f.severity == Severity.P2 for f in findings_c8), "Case 8 Failed: Expected P2 for missing primary_claim"
    print("✔ [PASSED] Case 8 (Schema Robustness with Cards - Correct P2 & No P0)")
    passed += 1

    # CASE 9: Auto-Remediation of Missing Title and Primary Claim
    slide_c9 = {
        "slide_id": "c9",
        "section": "Chiến lược",
        "archetype": "card_grid",
        "atoms": [
            {"title": "Mở rộng thị trường", "text": "Tiếp cận 3 thị trường xuất khẩu trọng điểm tại khu vực ASEAN."}
        ]
    }
    findings_c9 = agent.audit([slide_c9])
    assert len(findings_c9) >= 1, "Case 9 Failed: Expected findings for unformed slide"
    remediated = agent.auto_remediate([slide_c9], findings_c9)
    rem_slide = remediated[0]
    assert rem_slide.get("assertion_title") and len(rem_slide["assertion_title"].split()) >= 4, f"Title not synthesized: {rem_slide.get('assertion_title')}"
    assert rem_slide.get("primary_claim"), "Primary claim not synthesized"
    print("✔ [PASSED] Case 9 (Auto-Remediation Synthesizes Title & Primary Claim)")
    passed += 1

    # CASE 10: Auto-Remediation Cleans Title Period and Synchronizes Schema
    slide_c10 = {
        "slide_id": "c10",
        "title": "Doanh thu năm 2024 vượt kế hoạch 15%.",
        "primary_claim": "Đóng góp chủ yếu từ phân khúc khách hàng doanh nghiệp.",
        "archetype": "card_grid",
        "atoms": [{"title": "B2B", "text": "Doanh số tăng 25%."}]
    }
    findings_c10 = agent.audit([slide_c10])
    remediated = agent.auto_remediate([slide_c10], findings_c10)
    rem_slide = remediated[0]
    assert not rem_slide["assertion_title"].endswith("."), f"Trailing period not stripped: {rem_slide['assertion_title']}"
    assert rem_slide["assertion_title"] == rem_slide["title"], "assertion_title and title out of sync"
    re_audit = agent.audit(remediated)
    assert len(re_audit) == 0, f"Case 10 Failed: Residual issues after auto-remediation: {[f.issue for f in re_audit]}"
    print("✔ [PASSED] Case 10 (Auto-Remediation Cleans Period & Synchronizes Title Schema)")
    passed += 1

    print("-" * 60)
    print(f"Total Score: {passed}/{total} ({passed/total*100:.1f}%)")
    print("=" * 60)
    assert passed == total, f"Adversarial matrix failed: {passed}/{total}"


if __name__ == "__main__":
    test_agent10_adversarial_matrix()

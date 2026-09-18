"""
tests/macc_council/adversarial/test_agent03_hard.py
Adversarial Stress Test Matrix for Agent 03: NarrativeArcDirector.
10 ruthless edge cases:
1. Abrupt ending on raw data table without CTA
2. Long deck (>= 6 slides) missing executive agenda
3. Non-MECE section jumping (A -> B -> A)
4. Problem-only deck (Complication without Resolution)
5. Solution-only deck (Abrupt solution without context)
6. First slide is complex data matrix without thesis
7. Clean SCQA presentation (0 False Positives)
8. Short memo deck (2 slides - No false agenda alarm)
9. Auto-remediation generates conclusion slide
10. Auto-remediation generates executive agenda slide
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from scripts.macc_council.gate2_macro_narrative import NarrativeArcDirector
from scripts.macc_council.models import Severity


def run_all_adversarial_tests():
    agent = NarrativeArcDirector()
    results = {}

    # Case 1: Abrupt ending
    deck_1 = {
        "slides": [
            {"slide_id": "s1", "archetype": "title_hero", "assertion_title": "Chiến lược AI 2025"},
            {"slide_id": "s2", "section": "Thực trạng", "assertion_title": "Bối cảnh thị trường"},
            {"slide_id": "s3", "section": "Chi phí", "archetype": "table_dense", "assertion_title": "Bảng số liệu chi phí phụ lục"}
        ]
    }
    f1 = agent.audit(deck_1)
    results["Case 1 (Abrupt Ending)"] = any("Kết luận" in f.issue or "Call to Action" in f.issue for f in f1)

    # Case 2: Long deck missing agenda
    deck_2 = {
        "slides": [
            {"slide_id": "s1", "archetype": "title_hero", "assertion_title": "Chiến lược"},
            {"slide_id": "s2", "assertion_title": "Slide 2"},
            {"slide_id": "s3", "assertion_title": "Slide 3"},
            {"slide_id": "s4", "assertion_title": "Slide 4"},
            {"slide_id": "s5", "assertion_title": "Slide 5"},
            {"slide_id": "s6", "assertion_title": "Slide 6"},
            {"slide_id": "s7", "archetype": "conclusion_cta", "assertion_title": "Kết luận & Hành động"}
        ]
    }
    f2 = agent.audit(deck_2)
    results["Case 2 (Long Deck Missing Agenda)"] = any("Mục lục" in f.issue or "Agenda" in f.issue for f in f2)

    # Case 3: Non-MECE section jumping
    deck_3 = {
        "slides": [
            {"slide_id": "s1", "section": "Mở đầu", "assertion_title": "Giới thiệu"},
            {"slide_id": "s2", "section": "Tài chính", "assertion_title": "Doanh thu"},
            {"slide_id": "s3", "section": "Nhân sự", "assertion_title": "Đội ngũ"},
            {"slide_id": "s4", "section": "Tài chính", "assertion_title": "Chi phí phát sinh"},
            {"slide_id": "s5", "section": "Kết luận", "archetype": "conclusion_cta", "assertion_title": "Tổng kết"}
        ]
    }
    f3 = agent.audit(deck_3)
    results["Case 3 (Non-MECE Section Jumping)"] = any("nhảy cóc" in f.issue.lower() or "non-mece" in f.issue.lower() for f in f3)

    # Case 4: Problem-only deck (All problems, no solution)
    deck_4 = {
        "slides": [
            {"slide_id": "s1", "archetype": "title_hero", "assertion_title": "Báo cáo Thực trạng"},
            {"slide_id": "s2", "section": "Bối cảnh", "assertion_title": "Bối cảnh khó khăn"},
            {"slide_id": "s3", "section": "Thách thức", "assertion_title": "Khủng hoảng dòng tiền"},
            {"slide_id": "s4", "section": "Thách thức", "assertion_title": "Tỷ lệ khách hàng rời bỏ tăng cao"},
            {"slide_id": "s5", "section": "Thách thức", "assertion_title": "Đứt gãy chuỗi cung ứng"}
        ]
    }
    f4 = agent.audit(deck_4)
    results["Case 4 (Problem Only - Missing Resolution)"] = any("giải pháp" in f.issue.lower() or "kết luận" in f.issue.lower() for f in f4)

    # Case 5: Solution-only deck (Abrupt solution without context)
    deck_5 = {
        "slides": [
            {"slide_id": "s1", "archetype": "title_hero", "assertion_title": "Phần mềm ERP V8"},
            {"slide_id": "s2", "section": "Giải pháp", "assertion_title": "Module Kế toán nâng cao"},
            {"slide_id": "s3", "section": "Giải pháp", "assertion_title": "Module Kho vận thông minh"},
            {"slide_id": "s4", "section": "Giải pháp", "assertion_title": "Module Bán hàng đa kênh"},
            {"slide_id": "s5", "archetype": "conclusion_cta", "assertion_title": "Kế hoạch triển khai"}
        ]
    }
    f5 = agent.audit(deck_5)
    results["Case 5 (Solution Only - Missing Problem/Context)"] = any("bối cảnh" in f.issue.lower() or "thực trạng" in f.issue.lower() for f in f5)

    # Case 6: First slide is complex data matrix without thesis
    deck_6 = {
        "slides": [
            {"slide_id": "s1", "archetype": "table_dense", "assertion_title": "Bảng số liệu thô chi nhánh"},
            {"slide_id": "s2", "archetype": "conclusion_cta", "assertion_title": "Kết luận"}
        ]
    }
    f6 = agent.audit(deck_6)
    results["Case 6 (First Slide Dense Table)"] = any("Mở đầu" in f.issue for f in f6)

    # Case 7: Clean SCQA presentation (0 False Positives)
    deck_7 = {
        "slides": [
            {"slide_id": "s1", "archetype": "title_hero", "assertion_title": "Chiến lược Phát triển Bán dẫn 2030"},
            {"slide_id": "s2", "archetype": "agenda_list", "assertion_title": "Khung nội dung chiến lược"},
            {"slide_id": "s3", "section": "Bối cảnh", "assertion_title": "Việt Nam có vị trí địa kinh tế thuận lợi"},
            {"slide_id": "s4", "section": "Thách thức", "assertion_title": "Thiếu hụt 50.000 kỹ sư vi mạch chất lượng cao"},
            {"slide_id": "s5", "section": "Giải pháp", "assertion_title": "Triển khai liên minh đào tạo đại học - doanh nghiệp"},
            {"slide_id": "s6", "archetype": "conclusion_cta", "section": "Kết luận", "assertion_title": "Lộ trình 3 giai đoạn kiến tạo năng lực quốc gia"}
        ]
    }
    f7 = agent.audit(deck_7)
    results["Case 7 (Clean SCQA - No False Positive)"] = len(f7) == 0

    # Case 8: Short memo deck (2 slides - No false agenda alarm)
    deck_8 = {
        "slides": [
            {"slide_id": "s1", "archetype": "title_hero", "assertion_title": "Thông báo nội bộ"},
            {"slide_id": "s2", "archetype": "conclusion_cta", "assertion_title": "Hướng dẫn thực hiện"}
        ]
    }
    f8 = agent.audit(deck_8)
    results["Case 8 (Short Memo - No False Agenda)"] = len(f8) == 0

    # Case 9: Auto-remediation generates conclusion slide
    deck_9 = {
        "slides": [
            {"slide_id": "s1", "archetype": "title_hero", "assertion_title": "Kế hoạch quý 4"},
            {"slide_id": "s2", "archetype": "3_cards", "assertion_title": "Chi tiết công việc"}
        ]
    }
    f9 = agent.audit(deck_9)
    rem9 = agent.auto_remediate(deck_9, f9)
    results["Case 9 (Auto-Remediate Conclusion)"] = rem9["slides"][-1]["archetype"] == "conclusion_cta"

    # Case 10: Auto-remediation generates agenda slide
    deck_10 = {
        "slides": [
            {"slide_id": "s1", "archetype": "title_hero", "assertion_title": "Báo cáo thường niên"},
            {"slide_id": "s2", "section": "Kinh doanh", "assertion_title": "Thị trường"},
            {"slide_id": "s3", "section": "Tài chính", "assertion_title": "Lợi nhuận"},
            {"slide_id": "s4", "section": "Nhân sự", "assertion_title": "Tuyển dụng"},
            {"slide_id": "s5", "section": "Công nghệ", "assertion_title": "Hạ tầng"},
            {"slide_id": "s6", "section": "Rủi ro", "assertion_title": "Kiểm toán"},
            {"slide_id": "s7", "archetype": "conclusion_cta", "assertion_title": "Tổng kết"}
        ]
    }
    f10 = agent.audit(deck_10)
    rem10 = agent.auto_remediate(deck_10, f10)
    has_agenda_now = any(s.get("archetype") == "agenda_list" or "mục lục" in s.get("assertion_title", "").lower() for s in rem10["slides"][:3])
    results["Case 10 (Auto-Remediate Agenda)"] = has_agenda_now

    return results


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING ADVERSARIAL STRESS TEST MATRIX FOR AGENT 03")
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

"""
tests/macc_council/adversarial/test_agent08_hard.py
Adversarial Stress Test Matrix for Agent 08: AssertionCognitiveArbiter.
Validates Sentence Headline Rule, Cognitive Load (<=4 cards), Word Density (<=40 words), and Auto-Remediation.
"""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from scripts.macc_council.gate3_micro_pedagogy.agent08_assertion_cognitive import AssertionCognitiveArbiter
from scripts.macc_council.models import Severity


def test_agent08_adversarial_matrix():
    print("=" * 60)
    print("RUNNING ADVERSARIAL STRESS TEST MATRIX FOR AGENT 08")
    print("=" * 60)

    agent = AssertionCognitiveArbiter()
    passed = 0
    total = 10

    # CASE 1: Lazy topic title "Tổng quan" on content slide (P1)
    slide_c1 = {
        "slide_id": "c1",
        "title": "Tổng quan",
        "archetype": "card_grid",
        "content_items": [
            {"title": "Mục 1", "body": "Nội dung tóm tắt sơ bộ."}
        ]
    }
    findings_c1 = agent.audit([slide_c1])
    assert len(findings_c1) >= 1 and any("nhãn chủ đề" in f.issue.lower() or "tiêu đề" in f.issue.lower() for f in findings_c1), "Case 1 Failed: Lazy topic title 'Tổng quan' missed"
    print("✔ [PASSED] Case 1 (Lazy Topic Title 'Tổng quan' - P1 Caught)")
    passed += 1

    # CASE 2: Passive noun phrase title <= 3 words "Báo cáo tài chính" (P1)
    slide_c2 = {
        "slide_id": "c2",
        "assertion_title": "Báo cáo tài chính",
        "archetype": "metric_callout",
        "atoms": [
            {"title": "Q3", "text": "Số liệu doanh thu quý 3."}
        ]
    }
    findings_c2 = agent.audit([slide_c2])
    assert len(findings_c2) >= 1 and any("nhãn chủ đề" in f.issue.lower() or "tiêu đề" in f.issue.lower() for f in findings_c2), "Case 2 Failed: Short passive title 'Báo cáo tài chính' missed"
    print("✔ [PASSED] Case 2 (Passive Noun Label 'Báo cáo tài chính' - P1 Caught)")
    passed += 1

    # CASE 3: Valid full Assertion Headline (Valid - No False Positive)
    slide_c3 = {
        "slide_id": "c3",
        "assertion_title": "Doanh thu quý 3 tăng trưởng 24% nhờ mở rộng mạng lưới phân phối B2B",
        "archetype": "card_grid",
        "atoms": [
            {"title": "Động lực chính", "text": "Kênh đối tác doanh nghiệp tăng trưởng vượt bậc 45% so với cùng kỳ."}
        ]
    }
    findings_c3 = agent.audit([slide_c3])
    assert len(findings_c3) == 0, f"Case 3 Failed: False positive on valid assertion headline: {[f.issue for f in findings_c3]}"
    print("✔ [PASSED] Case 3 (Valid Full Assertion Headline - No False Positive)")
    passed += 1

    # CASE 4: Title Hero slide exemption (Valid - No False Positive)
    slide_c4 = {
        "slide_id": "c4",
        "title": "Hội nghị Chiến lược Chuyển đổi số 2025",
        "archetype": "title_hero",
        "content_items": []
    }
    findings_c4 = agent.audit([slide_c4])
    assert len(findings_c4) == 0, f"Case 4 Failed: False positive on title hero slide: {[f.issue for f in findings_c4]}"
    print("✔ [PASSED] Case 4 (Title Hero Exemption - No False Positive)")
    passed += 1

    # CASE 5: Cognitive Overload with > 4 atoms (P1)
    slide_c5 = {
        "slide_id": "c5",
        "assertion_title": "Hệ sinh thái sản phẩm mở rộng đồng bộ trên cả sáu lĩnh vực then chốt",
        "archetype": "card_grid",
        "atoms": [
            {"title": f"Mảng {i}", "text": f"Mô tả chi tiết cho cấu phần thứ {i}."} for i in range(1, 7)
        ]
    }
    findings_c5 = agent.audit([slide_c5])
    assert len(findings_c5) >= 1 and any("quá tải nhận thức" in f.issue.lower() or "vượt mức" in f.issue.lower() for f in findings_c5), "Case 5 Failed: 6 atoms cognitive overload missed"
    print("✔ [PASSED] Case 5 (Cognitive Overload 6 Atoms - P1 Caught)")
    passed += 1

    # CASE 6: Cognitive Overload with generic schema cards (P1)
    slide_c6 = {
        "slide_id": "c6",
        "title": "Doanh nghiệp triển khai đồng loạt 5 chương trình hành động trong quý tới",
        "archetype": "card_grid",
        "cards": [
            {"headline": f"Chương trình {i}", "description": f"Kế hoạch triển khai hành động {i}."} for i in range(1, 6)
        ]
    }
    findings_c6 = agent.audit([slide_c6])
    assert len(findings_c6) >= 1 and any("quá tải nhận thức" in f.issue.lower() or "vượt mức" in f.issue.lower() for f in findings_c6), "Case 6 Failed: 5 cards in generic schema missed"
    print("✔ [PASSED] Case 6 (Cognitive Overload 5 Cards Schema-Agnostic - P1 Caught)")
    passed += 1

    # CASE 7: Valid Cognitive Load (3 or 4 cards - No False Positive)
    slide_c7 = {
        "slide_id": "c7",
        "assertion_title": "Tập trung ba trụ cột công nghệ tạo đột phá năng suất cho toàn bộ tổ chức",
        "archetype": "card_grid",
        "atoms": [
            {"title": f"Trụ cột {i}", "text": f"Nội dung trọng tâm trụ cột công nghệ {i}."} for i in range(1, 4)
        ]
    }
    findings_c7 = agent.audit([slide_c7])
    assert len(findings_c7) == 0, f"Case 7 Failed: False positive on 3 cards: {[f.issue for f in findings_c7]}"
    print("✔ [PASSED] Case 7 (Healthy 3 Atoms - No False Positive)")
    passed += 1

    # CASE 8: Wall-of-text atom > 40 words (P2)
    long_text = "Dự án chuyển đổi số toàn diện của chúng tôi đã trải qua rất nhiều giai đoạn từ khảo sát hiện trạng hạ tầng ban đầu, lựa chọn các giải pháp phần mềm phù hợp, đào tạo cán bộ công nhân viên, cho đến việc tích hợp các hệ thống quản trị dữ liệu lớn trên nền tảng điện toán đám mây hiện đại nhằm mục tiêu giảm thiểu chi phí vận hành một cách bền vững."
    assert len(long_text.split()) > 40, f"Setup error: text only has {len(long_text.split())} words"
    slide_c8 = {
        "slide_id": "c8",
        "assertion_title": "Tối ưu hóa hệ thống vận hành mang lại hiệu quả vượt trội cho doanh nghiệp",
        "archetype": "card_grid",
        "atoms": [
            {"title": "Giai đoạn 1", "text": long_text}
        ]
    }
    findings_c8 = agent.audit([slide_c8])
    assert len(findings_c8) >= 1 and any("quá dài" in f.issue.lower() or "từ" in f.issue.lower() for f in findings_c8), "Case 8 Failed: Wall-of-text atom (>40 words) missed"
    print("✔ [PASSED] Case 8 (Wall-of-Text Atom > 40 Words - P2 Caught)")
    passed += 1

    # CASE 9: Concise atom <= 40 words (Valid - No False Positive)
    slide_c9 = {
        "slide_id": "c9",
        "assertion_title": "Hiện đại hóa hạ tầng mạng giúp tăng 30% tốc độ truy xuất dữ liệu",
        "archetype": "card_grid",
        "atoms": [
            {"title": "Hạ tầng", "text": "Nâng cấp băng thông lên 10Gbps và chuyển đổi 80% máy chủ vật lý lên môi trường đám mây."}
        ]
    }
    findings_c9 = agent.audit([slide_c9])
    assert len(findings_c9) == 0, f"Case 9 Failed: False positive on concise atom: {[f.issue for f in findings_c9]}"
    print("✔ [PASSED] Case 9 (Concise Atom <= 40 Words - No False Positive)")
    passed += 1

    # CASE 10: Auto-Remediation Trims Overload & Enhances Lazy Title
    slide_c10 = {
        "slide_id": "c10",
        "title": "Các giải pháp",
        "archetype": "card_grid",
        "atoms": [
            {"title": f"Giải pháp {i}", "text": f"Chi tiết giải pháp thứ {i}."} for i in range(1, 7)
        ]
    }
    findings_c10 = agent.audit([slide_c10])
    assert len(findings_c10) >= 2, f"Case 10 Failed: Expected findings for remediation, got {len(findings_c10)}"
    remediated = agent.auto_remediate([slide_c10], findings_c10)
    rem_slide = remediated[0]
    # Check atoms trimmed to <= 4
    assert len(rem_slide.get("atoms", [])) <= 4, f"Atoms not trimmed to 4: {len(rem_slide.get('atoms', []))}"
    # Check speaker notes received overflow
    assert "Bổ sung thêm" in rem_slide.get("speaker_notes", ""), "Speaker notes missing overflow atoms"
    # Check title enhanced beyond lazy label
    rem_title = rem_slide.get("assertion_title") or rem_slide.get("title")
    assert rem_title.lower() != "các giải pháp" and len(rem_title.split()) > 3, f"Title not enhanced: {rem_title}"
    print("✔ [PASSED] Case 10 (Auto-Remediation Resolves Overload & Enhances Title)")
    passed += 1

    print("-" * 60)
    print(f"Total Score: {passed}/{total} ({passed/total*100:.1f}%)")
    print("=" * 60)
    assert passed == total, f"Adversarial matrix failed: {passed}/{total}"


if __name__ == "__main__":
    test_agent08_adversarial_matrix()

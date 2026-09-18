"""
tests/macc_council/test_full_council_e2e.py
End-to-End Integration Test for MACC-QA V8.0: 16-Agent Omniscient Council.
Simulates a multi-round dialectical review and auto-remediation loop on an adversarial presentation deck.
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from scripts.macc_council import MultiRoundCouncilOrchestrator, Severity


def test_full_council_convergence():
    orchestrator = MultiRoundCouncilOrchestrator()

    source_text = (
        "Năm 2024, doanh nghiệp đạt doanh thu 1.500 tỷ VNĐ và tốc độ tăng trưởng 18.5%. "
        "Chiến lược giai đoạn 2025-2030 tập trung vào chuyển đổi số và bán dẫn."
    )

    adversarial_deck = {
        "slides": [
            {
                "slide_id": "slide_01",
                "assertion_title": "Báo cáo Chiến lược Công nghệ Bán dẫn 2025",
                "primary_claim": "Định hướng phát triển ngành công nghệ cao quốc gia.",
                "archetype": "title_hero"
            },
            {
                "slide_id": "slide_02",
                "section": "Thực trạng",
                "assertion_title": "Tổng quan",  # Agent 8: Lazy Topic Label
                "primary_claim": "Doanh thu năm 2024: 1.500 tỷ VNĐ và tăng trưởng 18.5%.",
                "archetype": "split_comparison",
                "atoms": [
                    {
                        "title": "Bảo mật",
                        "text": "Liên hệ trưởng dự án qua CCCD: 001095012345 hoặc SĐT: 0912345678."  # Agent 2: PII Leak
                    },
                    {
                        "title": "Hiệu năng",
                        "text": "Phần mềm tốt nhất thị trường với bảo mật tuyệt đối."  # Agent 9: Superlative
                    }
                ]
            },
            {
                "slide_id": "slide_03",
                "section": "Mô hình toán học",
                "assertion_title": "Mô hình tối ưu hóa chi phí sản xuất vi mạch",
                "primary_claim": r"Công thức toán học: $\frac{A + B}{C$ mang lại giá trị cao.",  # Agent 6: Unbalanced Math
                "archetype": "quote_callout",
                "atoms": [
                    {
                        "title": "Thuật toán",
                        "text": "Trong kỷ nguyên số ngày nay công nghệ đóng vai trò vô cùng quan trọng trong việc tăng tốc."  # Agent 7: AI cliché
                    }
                ]
            },
            {
                "slide_id": "slide_04",
                "section": "Thị phần",
                "assertion_title": "Cơ cấu doanh thu theo phân khúc và",  # Agent 13: Orphan word 'và'
                "primary_claim": "Phân bổ thị phần phân khúc doanh nghiệp và cá nhân.",
                "archetype": "3_cards",
                "chart": {
                    "type": "pie",
                    "data": [50, 40, 30]  # Agent 12: Sum = 120% != 100%, missing unit
                },
                "transition": "morph",
                "morph_shapes": ["chart_box"]  # Agent 15: Missing !!...!!
            }
            # Slide 5 missing -> Agent 3: Abrupt ending (missing conclusion CTA)
        ]
    }

    print("\n--- Starting Multi-Round Dialectical Convergence Loop ---")

    rounds_logged = []

    def on_round(round_idx, report):
        rounds_logged.append((round_idx, report.final_score, report.p0_count, report.p1_count))
        print(
            f"Round {round_idx}: Score={report.final_score:.1f}, "
            f"P0={report.p0_count}, P1={report.p1_count}, P2={report.p2_count}, "
            f"Certified={report.certified}"
        )

    final_report = orchestrator.run_convergence_loop(
        target=adversarial_deck,
        context={"source_text": source_text},
        max_rounds=5,
        on_round_callback=on_round
    )

    print("\n--- Final Council Audit Report ---")
    print(f"Total Rounds Run: {len(rounds_logged)}")
    print(f"Final Certified Status: {final_report.certified}")
    print(f"Final Quality Score: {final_report.final_score}/100")
    print(f"Remaining P0 Defects: {final_report.p0_count}")
    print(f"Remaining P1 Defects: {final_report.p1_count}")
    print(f"Remaining P2 Defects: {final_report.p2_count}")

    # Assertions
    assert len(rounds_logged) >= 1, "Must run at least 1 round"
    # Verify first round had defects
    assert rounds_logged[0][2] >= 1 or rounds_logged[0][3] >= 1, "Initial deck must have defects"

    # Verify final convergence
    assert final_report.p0_count == 0, f"Must have 0 P0 defects, found {final_report.p0_count}"
    assert final_report.p1_count == 0, f"Must have 0 P1 defects, found {final_report.p1_count}"
    assert final_report.final_score >= 99.5, f"Score must be >= 99.5, got {final_report.final_score}"
    assert final_report.certified is True, "Deck must be certified zero-defect!"

    # Verify remediated slides content
    rem_slides = final_report.remediated_slides
    assert rem_slides is not None, "Remediated slides must be returned"
    assert len(rem_slides) >= 5, "Conclusion slide must be appended to fix abrupt ending"
    assert rem_slides[-1]["archetype"] == "conclusion_cta", "Last slide must be conclusion_cta"

    print("\n🎉 Full Council E2E Dialectical Convergence Test Passed 100%!")


if __name__ == "__main__":
    test_full_council_convergence()

"""
tests/macc_council/test_chaos_concurrency.py
Chaos and Concurrency test suite for MACC-QA V8.0 MultiRoundCouncilOrchestrator.
Validates:
1. Thread safety and determinism of parallel gate audits.
2. Concurrent multi-deck convergence under thread pool stress.
3. Chaos and malformed payload resilience across all 16 agents.
"""

import sys
import copy
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from scripts.macc_council import MultiRoundCouncilOrchestrator, Severity


def _create_sample_deck(deck_id: int):
    return {
        "deck_title": f"Deck Benchmark {deck_id}",
        "slides": [
            {
                "slide_id": f"s_{deck_id}_01",
                "assertion_title": "Báo cáo Chiến lược Công nghệ Bán dẫn 2025",
                "primary_claim": "Định hướng phát triển ngành công nghệ cao quốc gia.",
                "archetype": "title_hero"
            },
            {
                "slide_id": f"s_{deck_id}_02",
                "section": "Thực trạng",
                "assertion_title": "Tổng quan",
                "primary_claim": "Doanh thu năm 2024: 1.500 tỷ VNĐ và tăng trưởng 18.5%.",
                "archetype": "split_comparison",
                "atoms": [
                    {
                        "title": "Bảo mật",
                        "text": "Liên hệ trưởng dự án qua CCCD: 001095012345 hoặc SĐT: 0912345678."
                    },
                    {
                        "title": "Hiệu năng",
                        "text": "Phần mềm tốt nhất thị trường với bảo mật tuyệt đối."
                    }
                ]
            },
            {
                "slide_id": f"s_{deck_id}_03",
                "section": "Mô hình",
                "assertion_title": "Mô hình chi phí sản xuất",
                "primary_claim": r"Công thức toán học: $\frac{A + B}{C$ mang lại giá trị cao.",
                "archetype": "quote_callout",
                "atoms": [
                    {
                        "title": "Thuật toán",
                        "text": "Trong kỷ nguyên số ngày nay công nghệ đóng vai trò vô cùng quan trọng."
                    }
                ]
            },
            {
                "slide_id": f"s_{deck_id}_04",
                "section": "Thị phần",
                "assertion_title": "Cơ cấu doanh thu theo phân khúc và",
                "primary_claim": "Phân bổ thị phần phân khúc doanh nghiệp.",
                "archetype": "3_cards",
                "chart": {
                    "type": "pie",
                    "data": [50, 40, 30]
                },
                "transition": "morph",
                "morph_shapes": ["chart_box"]
            }
        ]
    }


def test_parallel_audit_determinism():
    """Verify that parallel audits yield identical results across multiple executions."""
    orchestrator = MultiRoundCouncilOrchestrator()
    deck = _create_sample_deck(1)
    context = {"source_text": "Doanh thu 1.500 tỷ VNĐ năm 2024."}

    # Run round 1
    report1, _ = orchestrator.run_round(deck, context, auto_remediate=False)
    # Run round 2 on fresh copy
    report2, _ = orchestrator.run_round(deck, context, auto_remediate=False)

    assert report1.final_score == report2.final_score
    assert report1.p0_count == report2.p0_count
    assert report1.p1_count == report2.p1_count
    assert report1.p2_count == report2.p2_count
    assert len(report1.all_findings) == len(report2.all_findings)


def test_concurrent_multi_deck_stress():
    """Verify that multiple decks can be converged concurrently without race conditions."""
    orchestrator = MultiRoundCouncilOrchestrator()
    num_decks = 4
    context = {"source_text": "Năm 2024, doanh nghiệp đạt doanh thu 1.500 tỷ VNĐ và tăng trưởng 18.5%."}

    def converge_worker(deck_id: int):
        deck = _create_sample_deck(deck_id)
        report = orchestrator.run_convergence_loop(
            target=deck,
            context=context,
            max_rounds=5
        )
        return deck_id, report

    start_time = time.perf_counter()
    with ThreadPoolExecutor(max_workers=num_decks) as executor:
        futures = [executor.submit(converge_worker, i) for i in range(1, num_decks + 1)]
        results = [f.result() for f in as_completed(futures)]
    elapsed = time.perf_counter() - start_time

    assert len(results) == num_decks
    for deck_id, rep in results:
        assert rep.certified is True, f"Deck {deck_id} failed certification: score={rep.final_score}"
        assert rep.p0_count == 0
        assert rep.p1_count == 0
        assert rep.final_score >= 99.5

    print(f"Concurrent stress test: {num_decks} decks converged in {elapsed:.2f}s")


def test_chaos_payload_resilience():
    """Verify that corrupted and irregular payloads do not crash the council."""
    orchestrator = MultiRoundCouncilOrchestrator()

    chaos_decks = [
        # Completely empty deck
        {"slides": []},
        # Deck with None and strange data types
        {
            "slides": [
                {
                    "slide_id": "chaos_1",
                    "title": None,
                    "assertion_title": "",
                    "atoms": None,
                    "table_data": {"headers": None, "rows": None}
                }
            ]
        },
        # Extreme string length and unicode symbols
        {
            "slides": [
                {
                    "slide_id": "chaos_2",
                    "title": "A" * 5000,
                    "assertion_title": "\u25b6 \u2014 \ud83d\ude80 " * 200,
                    "atoms": [{"title": "X", "text": "\x00\x01\x02 test"}]
                }
            ]
        }
    ]

    for idx, c_deck in enumerate(chaos_decks):
        # Must execute without raising unhandled exceptions
        report, remediated = orchestrator.run_round(c_deck, context={}, auto_remediate=True)
        assert isinstance(report.final_score, (int, float))
        assert report.p0_count >= 0


def test_parallel_audit_fault_isolation():
    """Verify that a crashing agent inside _parallel_audit is isolated as a P0 finding without crashing the council."""
    orchestrator = MultiRoundCouncilOrchestrator()
    BrokenAgent = type(
        "BrokenMockAgent",
        (),
        {
            "name": "ChaosCrashingAgent",
            "gate": "Gate 1",
            "audit": lambda *a, **kw: 1 / 0
        }
    )
    b1 = BrokenAgent()
    b2 = BrokenAgent()
    findings_list = orchestrator._parallel_audit([b1, b2], target={"slides": []})

    assert len(findings_list) == 2
    for f_list in findings_list:
        assert len(f_list) == 1
        f = f_list[0]
        assert f.severity == Severity.P0
        assert "ChaosCrashingAgent" in f.issue
        assert "ZeroDivisionError" in f.issue


def test_nested_frac_and_interval_resilience():
    """Verify that mathematically complex nested LaTeX and intervals do not cause false positive P0/P1 rejections."""
    orchestrator = MultiRoundCouncilOrchestrator()
    deck = {
        "slides": [
            {
                "slide_id": "math_01",
                "assertion_title": "Mô Hình Tối Ưu Hóa Hàm Số Trong Không Gian Mở",
                "primary_claim": r"Giá trị nghiệm hội tụ trong khoảng $[0, 1)$ với công thức $\frac{1}{\frac{a}{b}}$.",
                "archetype": "quote_callout",
                "atoms": [
                    {
                        "title": "Nghiệm hội tụ",
                        "text": r"Phân tích cận trên và cận dưới trong miền xác định mở."
                    }
                ]
            },
            {
                "slide_id": "math_02",
                "assertion_title": "Tổng Kết Định Hướng Phát Triển",
                "primary_claim": "Đồng bộ hóa các giải pháp chiến lược.",
                "archetype": "conclusion_cta"
            }
        ]
    }
    report, _ = orchestrator.run_round(deck, context={"source_text": ""}, auto_remediate=False)
    # Neither $[0, 1)$ nor $\frac{1}{\frac{a}{b}}$ should trigger P0/P1 syntax errors
    math_syntax_findings = [
        f for f in report.all_findings
        if f.agent == "MathematicalOMMLValidator" and f.severity in (Severity.P0, Severity.P1)
    ]
    assert len(math_syntax_findings) == 0, f"Found unexpected math syntax errors: {math_syntax_findings}"

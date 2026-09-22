"""
tests/macc_council/adversarial_critique_probe.py
Adversarial Forensic Probe & Performance Benchmark for MACC-QA V8.0 Council.
Executes 5 deep empirical experiments to uncover architectural gaps and failure modes.
"""

import sys
import time
import copy
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from scripts.macc_council.orchestrator import MultiRoundCouncilOrchestrator
from scripts.macc_council.models import Severity, AgentFinding


def probe_deduplication_and_casing():
    """Probe 1: Verify case-sensitivity and duplication behavior in Agent 16 arbitrate_findings."""
    print("\n--- [PROBE 1] Deduplication & Case Sensitivity in Agent 16 ---")
    orchestrator = MultiRoundCouncilOrchestrator()
    judge = orchestrator.agent16

    findings = [
        AgentFinding(
            agent="SourceFidelityFactChecker",
            gate="Gate 1",
            slide_id="slide_01",
            severity=Severity.P2,
            issue="Nguồn mở rộng",
            rationale="Test",
            suggestion="Test",
            original_value="100 Triệu"
        ),
        AgentFinding(
            agent="SourceFidelityFactChecker",
            gate="Gate 1",
            slide_id="slide_01",
            severity=Severity.P2,
            issue="Nguồn mở rộng",
            rationale="Test",
            suggestion="Test",
            original_value="100 triệu"
        ),
        AgentFinding(
            agent="SourceFidelityFactChecker",
            gate="Gate 1",
            slide_id="slide_01",
            severity=Severity.P2,
            issue="Nguồn mở rộng",
            rationale="Test",
            suggestion="Test",
            original_value="100 Triệu "  # trailing space
        ),
    ]

    arbitrated = judge.arbitrate_findings(findings)
    print(f"Input findings: {len(findings)}, Output after arbitration: {len(arbitrated)}")
    values = [f.original_value for f in arbitrated]
    print(f"Remaining values: {values}")
    return len(findings), len(arbitrated)


def probe_p2_barrier_and_oscillation():
    """Probe 2: P2 Warning Barrier vs Zero-Defect Threshold & Oscillation."""
    print("\n--- [PROBE 2] P2 Warning Barrier vs Zero-Defect Threshold & Oscillation ---")
    orchestrator = MultiRoundCouncilOrchestrator()

    # Create a deck where only a P2 finding exists that cannot be auto-remediated (e.g. valid external source footer)
    deck_with_external_footer = {
        "slides": [
            {
                "slide_id": "slide_01",
                "assertion_title": "Bối Cảnh Dân Số Việt Nam Đạt 100 Triệu Người",
                "primary_claim": "Quy mô dân số Việt Nam đã vượt ngưỡng 100 triệu người.",
                "source_footer": "Tổng cục Thống kê - Kết quả Tổng điều tra",
                "archetype": "title_hero"
            },
            {
                "slide_id": "slide_02",
                "assertion_title": "Chiến Lược Hành Động Trọng Tâm",
                "primary_claim": "Thực hiện đồng bộ các giải pháp chiến lược.",
                "archetype": "conclusion_cta"
            }
        ]
    }
    # Canonical text does NOT contain 100 triệu, so it relies on source_footer
    context = {"source_text": "Tài liệu đào tạo dân số học đại cương."}

    report = orchestrator.run_convergence_loop(deck_with_external_footer, context=context, max_rounds=5)
    print(f"Total Rounds Run: {report.total_rounds}")
    print(f"Final Score: {report.final_score}")
    print(f"Certified: {report.certified}")
    print(f"P0: {report.p0_count}, P1: {report.p1_count}, P2: {report.p2_count}")
    return report


def probe_high_concurrency_stress():
    """Probe 3: 32 Concurrent Council Audits to detect race conditions or state leaks."""
    print("\n--- [PROBE 3] 32 Concurrent Council Audits Stress Bench ---")
    orchestrator = MultiRoundCouncilOrchestrator()
    num_threads = 32

    deck = {
        "slides": [
            {
                "slide_id": "s1",
                "assertion_title": "Doanh Thu Đạt 1.500 Tỷ VNĐ Năm 2024",
                "primary_claim": "Tăng trưởng kinh doanh ổn định.",
                "archetype": "title_hero"
            },
            {
                "slide_id": "s2",
                "assertion_title": "Tổng Kết Định Hướng Phát Triển",
                "primary_claim": "Đồng bộ hóa các sáng kiến trọng điểm.",
                "archetype": "conclusion_cta"
            }
        ]
    }
    context = {"source_text": "Năm 2024 doanh thu đạt 1.500 tỷ VNĐ."}

    errors = []
    t0 = time.perf_counter()

    def worker(i):
        try:
            r, _ = orchestrator.run_round(deck, context=context, auto_remediate=False)
            return r.final_score
        except Exception as e:
            errors.append((i, str(e)))
            return None

    with ThreadPoolExecutor(max_workers=16) as pool:
        scores = list(pool.map(worker, range(num_threads)))

    elapsed = time.perf_counter() - t0
    print(f"Completed {num_threads} concurrent audits in {elapsed:.3f}s")
    print(f"Errors: {len(errors)}")
    print(f"Unique scores: {set(scores)}")
    return len(errors), elapsed


def probe_deepcopy_overhead_profile():
    """Probe 4: Profile deepcopy time vs compute time on 14-slide realistic deck."""
    print("\n--- [PROBE 4] Deepcopy Overhead vs Computation Time Profiling ---")
    benchmark_file = Path("Du_An_Outputs/Bai_1__Nhap_mon_DSH/slide-blueprints.json")
    if not benchmark_file.exists():
        print("Skipped: benchmark file not found")
        return

    with open(benchmark_file, "r", encoding="utf-8") as f:
        deck = json.load(f)

    # Measure 100 deepcopies
    t0 = time.perf_counter()
    for _ in range(100):
        _ = copy.deepcopy(deck)
    t_copy = (time.perf_counter() - t0) / 100

    orchestrator = MultiRoundCouncilOrchestrator()
    t0 = time.perf_counter()
    for _ in range(10):
        _ = orchestrator.run_round(deck, context={}, auto_remediate=False)
    t_round = (time.perf_counter() - t0) / 10

    print(f"14-slide deck single deepcopy time: {t_copy * 1000:.2f}ms")
    print(f"14-slide deck complete 16-agent audit round: {t_round * 1000:.2f}ms")
    print(f"Deepcopy ratio of single audit round: {(t_copy / t_round) * 100:.1f}%")


if __name__ == "__main__":
    print("=" * 70)
    print("MACC-QA V8.0 FORENSIC EXPERIMENTS & INDEPENDENT AUDIT BENCH")
    print("=" * 70)
    probe_deduplication_and_casing()
    probe_p2_barrier_and_oscillation()
    probe_high_concurrency_stress()
    probe_deepcopy_overhead_profile()
    print("\n" + "=" * 70)
    print("[SUCCESS] All 4 Probes Executed.")
    print("=" * 70)

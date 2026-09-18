"""
tests/macc_council/adversarial/test_agent16_hard.py
Adversarial Stress Test Matrix for Agent 16: SupremeConsensusJudge.
Validates Pareto trade-off arbitration, strict Zero-Defect certification (>=99.5), oscillation dampening, and synthesis.
"""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from scripts.macc_council.gate5_supreme_arbitration.agent16_supreme_judge import SupremeConsensusJudge
from scripts.macc_council.models import AgentFinding, GateReport, Severity


def test_agent16_adversarial_matrix():
    print("=" * 60)
    print("RUNNING ADVERSARIAL STRESS TEST MATRIX FOR AGENT 16")
    print("=" * 60)

    judge = SupremeConsensusJudge()
    passed = 0
    total = 10

    # CASE 1: Flawless Deck - Zero Defect Certification
    empty_gate_reports = {
        f"Gate {i}": GateReport(gate_name=f"Gate {i}", passed=True, findings=[]) for i in range(1, 6)
    }
    report_c1 = judge.evaluate_council(empty_gate_reports, total_rounds=1)
    assert report_c1.certified is True, "Case 1 Failed: Clean deck not certified"
    assert report_c1.final_score == 100.0, f"Case 1 Failed: Score not 100.0: {report_c1.final_score}"
    assert report_c1.p0_count == 0 and report_c1.p1_count == 0 and report_c1.p2_count == 0
    print("✔ [PASSED] Case 1 (Flawless Deck - Certified True & Score 100.0)")
    passed += 1

    # CASE 2: P0 Blocker Rejection
    p0_finding = AgentFinding(
        agent="SourceFidelityFactChecker",
        gate="Gate 1",
        slide_id="s1",
        severity=Severity.P0,
        issue="Số liệu giả mạo nghiêm trọng",
        rationale="P0 Blocker",
        suggestion="Xóa hoặc sửa",
        evidence="120%"
    )
    gr_c2 = {
        "Gate 1": GateReport(gate_name="Gate 1", passed=False, findings=[p0_finding]),
        "Gate 2": GateReport(gate_name="Gate 2", passed=True, findings=[])
    }
    report_c2 = judge.evaluate_council(gr_c2)
    assert report_c2.certified is False, "Case 2 Failed: Deck with P0 was certified"
    assert report_c2.final_score <= 85.0, f"Case 2 Failed: Score too high: {report_c2.final_score}"
    assert report_c2.p0_count == 1
    print("✔ [PASSED] Case 2 (P0 Blocker Rejection - Certified False)")
    passed += 1

    # CASE 3: P1 Integrity Rejection
    p1_finding = AgentFinding(
        agent="DomainPedagogyScholar",
        gate="Gate 3",
        slide_id="s2",
        severity=Severity.P1,
        issue="Sai lệch đơn vị đo lường",
        rationale="P1 Integrity issue",
        suggestion="Sửa đơn vị",
        evidence="tỷ USD"
    )
    gr_c3 = {
        "Gate 3": GateReport(gate_name="Gate 3", passed=False, findings=[p1_finding])
    }
    report_c3 = judge.evaluate_council(gr_c3)
    assert report_c3.certified is False, "Case 3 Failed: Deck with P1 was certified"
    assert report_c3.final_score == 95.0, f"Case 3 Failed: Expected score 95.0, got {report_c3.final_score}"
    assert report_c3.p1_count == 1
    print("✔ [PASSED] Case 3 (P1 Integrity Rejection - Certified False)")
    passed += 1

    # CASE 4: P2 Hygiene Rejection (Score 99.0 < 99.5)
    p2_finding = AgentFinding(
        agent="TypographyWidowOrphanSentinel",
        gate="Gate 4",
        slide_id="s3",
        severity=Severity.P2,
        issue="Từ mồ côi rớt dòng",
        rationale="P2 Hygiene issue",
        suggestion="Thêm non-breaking space",
        evidence="năm"
    )
    gr_c4 = {
        "Gate 4": GateReport(gate_name="Gate 4", passed=False, findings=[p2_finding])
    }
    report_c4 = judge.evaluate_council(gr_c4)
    assert report_c4.certified is False, "Case 4 Failed: Deck with 99.0 score certified (must be >= 99.5)"
    assert report_c4.final_score == 99.0, f"Case 4 Failed: Expected 99.0, got {report_c4.final_score}"
    assert report_c4.p2_count == 1
    print("✔ [PASSED] Case 4 (P2 Hygiene Strict Penalty - Certified False at 99.0)")
    passed += 1

    # CASE 5: Deduplication of Identical Overlapping Findings
    dup_finding_1 = AgentFinding(
        agent="AgentA", gate="Gate 2", slide_id="s5", severity=Severity.P1,
        issue="Mâu thuẫn số liệu doanh thu", rationale="Trùng lặp", suggestion="Sửa",
        original_value="150 tỷ"
    )
    dup_finding_2 = AgentFinding(
        agent="AgentB", gate="Gate 2", slide_id="s5", severity=Severity.P1,
        issue="Mâu thuẫn số liệu doanh thu", rationale="Trùng lặp", suggestion="Sửa",
        original_value="150 tỷ"
    )
    arbitrated = judge.arbitrate_findings([dup_finding_1, dup_finding_2])
    assert len(arbitrated) == 1, f"Case 5 Failed: Failed to deduplicate identical findings: {len(arbitrated)}"
    print("✔ [PASSED] Case 5 (Deduplication of Identical Overlapping Findings - Passed)")
    passed += 1

    # CASE 6: Pareto Trade-off Arbitration (P0 Precedence over P2)
    f_p0 = AgentFinding(
        agent="CompliancePrivacyGuardian", gate="Gate 1", slide_id="s1", severity=Severity.P0,
        issue="Lộ khóa bí mật AWS", rationale="Bảo mật tuyệt đối", suggestion="Mask",
        original_value="AKIA123456789012"
    )
    f_p2 = AgentFinding(
        agent="TypographyWidowOrphanSentinel", gate="Gate 4", slide_id="s1", severity=Severity.P2,
        issue="Từ mồ côi", rationale="Trình bày", suggestion="Bind nbsp",
        original_value="AKIA123456789012"
    )
    arbitrated_c6 = judge.arbitrate_findings([f_p0, f_p2])
    assert any(f.severity == Severity.P0 for f in arbitrated_c6), "Case 6 Failed: P0 lost in arbitration"
    print("✔ [PASSED] Case 6 (Pareto Arbitration P0 Precedence - Passed)")
    passed += 1

    # CASE 7: Score Clamping (Catastrophic Deck Floor at 0.0)
    many_p0s = [
        AgentFinding(
            agent="Tester", gate="Gate 1", slide_id=f"s_{i}", severity=Severity.P0,
            issue=f"Catastrophic defect {i}", rationale="Fatal", suggestion="Fix",
            original_value=f"val_{i}"
        ) for i in range(20)  # 20 * 15 = 300 points deduction
    ]
    gr_c7 = {"Gate 1": GateReport(gate_name="Gate 1", passed=False, findings=many_p0s)}
    report_c7 = judge.evaluate_council(gr_c7)
    assert report_c7.final_score == 0.0, f"Case 7 Failed: Score not clamped to 0.0: {report_c7.final_score}"
    print("✔ [PASSED] Case 7 (Mathematical Score Floor Clamping at 0.0 - Passed)")
    passed += 1

    # CASE 8: Multi-Round Convergence Simulation
    # Round 1 uncertified, Round 2 remediated
    report_r1 = judge.evaluate_council(gr_c2, total_rounds=1)
    assert report_r1.certified is False
    report_r2 = judge.evaluate_council(empty_gate_reports, total_rounds=2)
    assert report_r2.certified is True and report_r2.total_rounds == 2
    print("✔ [PASSED] Case 8 (Multi-Round Convergence Simulation - Passed)")
    passed += 1

    # CASE 9: Oscillation & Deadlock Detection Helper
    round_history = [
        [("s1", Severity.P1, "layout")],
        [("s1", Severity.P1, "layout")],
        [("s1", Severity.P1, "layout")]
    ]
    is_oscillating = judge.detect_oscillation(round_history)
    assert is_oscillating is True, "Case 9 Failed: Oscillation pattern not detected"
    print("✔ [PASSED] Case 9 (Oscillation & Deadlock Detection - Passed)")
    passed += 1

    # CASE 10: Complete Council Gate Aggregation Integrity
    gr_c10 = {
        f"Gate {i}": GateReport(gate_name=f"Gate {i}", passed=True, findings=[]) for i in range(1, 6)
    }
    report_c10 = judge.evaluate_council(gr_c10, total_rounds=3, remediated_slides=[{"slide_id": "s1"}])
    assert len(report_c10.gate_reports) == 5, f"Case 10 Failed: Expected 5 gate reports, got {len(report_c10.gate_reports)}"
    assert report_c10.remediated_slides is not None and len(report_c10.remediated_slides) == 1
    assert report_c10.certified is True
    print("✔ [PASSED] Case 10 (Complete Council Gate Aggregation Integrity - Passed)")
    passed += 1

    print("-" * 60)
    print(f"Total Score: {passed}/{total} ({passed/total*100:.1f}%)")
    print("=" * 60)
    assert passed == total, f"Adversarial matrix failed: {passed}/{total}"


if __name__ == "__main__":
    test_agent16_adversarial_matrix()

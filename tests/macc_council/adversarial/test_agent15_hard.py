"""
tests/macc_council/adversarial/test_agent15_hard.py
Adversarial Stress Test Matrix for Agent 15: MotionChoreographer.
Validates PowerPoint Morph naming (!!shape!!), 60 FPS duration limits, slide 1 morph guards, and auto-remediation.
"""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from scripts.macc_council.gate4_spatial_motion.agent15_motion_choreographer import MotionChoreographer
from scripts.macc_council.models import Severity


def test_agent15_adversarial_matrix():
    print("=" * 60)
    print("RUNNING ADVERSARIAL STRESS TEST MATRIX FOR AGENT 15")
    print("=" * 60)

    agent = MotionChoreographer()
    passed = 0
    total = 10

    # CASE 1: Morph shape missing double exclamation marks (P1)
    slide_c1 = {
        "slide_id": "c1",
        "title": "Chuyển cảnh biến hình",
        "transition": "morph",
        "morph_shapes": ["hero_badge"]
    }
    findings_c1 = agent.audit([{}, slide_c1])  # slide 2
    assert len(findings_c1) >= 1 and any("morph" in f.issue.lower() and "quy cách" in f.issue.lower() for f in findings_c1), "Case 1 Failed: Unwrapped morph shape missed"
    print("✔ [PASSED] Case 1 (Unwrapped Morph Shape 'hero_badge' - P1 Caught)")
    passed += 1

    # CASE 2: Morph shape in dict format missing !! (P1)
    slide_c2 = {
        "slide_id": "c2",
        "title": "Biến đổi thẻ số liệu",
        "transition": "morph",
        "shapes": [
            {"name": "kpi_card", "morph": True}
        ]
    }
    findings_c2 = agent.audit([{}, slide_c2])
    assert len(findings_c2) >= 1 and any("kpi_card" in f.issue or "quy cách" in f.issue.lower() for f in findings_c2), "Case 2 Failed: Morph shape in dict format missed"
    print("✔ [PASSED] Case 2 (Morph Shape in Dict Format - P1 Caught)")
    passed += 1

    # CASE 3: Properly formatted morph shape !!hero_badge!! (Valid - No False Positive)
    slide_c3 = {
        "slide_id": "c3",
        "title": "Biến hình hoàn hảo",
        "transition": "morph",
        "morph_shapes": ["!!hero_badge!!"]
    }
    findings_c3 = agent.audit([{}, slide_c3])
    assert len(findings_c3) == 0, f"Case 3 Failed: False positive on !!hero_badge!!: {[f.issue for f in findings_c3]}"
    print("✔ [PASSED] Case 3 (Properly Formatted '!!hero_badge!!' - No False Positive)")
    passed += 1

    # CASE 4: First slide having transition: "morph" (P2)
    slide_c4 = {
        "slide_id": "c4",
        "title": "Slide mở đầu",
        "transition": "morph"
    }
    findings_c4 = agent.audit([slide_c4])  # index 0
    assert len(findings_c4) >= 1 and any("đầu tiên" in f.issue.lower() or "slide 1" in f.issue.lower() for f in findings_c4), "Case 4 Failed: Slide 1 morph transition missed"
    print("✔ [PASSED] Case 4 (First Slide Morph Transition Guard - P2 Caught)")
    passed += 1

    # CASE 5: Transition duration too slow > 2.5s (3.5s) (P2)
    slide_c5 = {
        "slide_id": "c5",
        "title": "Chuyển cảnh chậm chạp",
        "transition": "fade",
        "transition_duration": 3.5
    }
    findings_c5 = agent.audit([{}, slide_c5])
    assert len(findings_c5) >= 1 and any("chậm" in f.issue.lower() or "2.5s" in f.issue for f in findings_c5), "Case 5 Failed: Too slow transition duration missed"
    print("✔ [PASSED] Case 5 (Too Slow Transition Duration 3.5s - P2 Caught)")
    passed += 1

    # CASE 6: Transition duration too fast < 0.3s (0.1s) (P2)
    slide_c6 = {
        "slide_id": "c6",
        "title": "Chuyển cảnh giật cục",
        "transition": "fade",
        "transition_duration": 0.1
    }
    findings_c6 = agent.audit([{}, slide_c6])
    assert len(findings_c6) >= 1 and any("ngắn" in f.issue.lower() or "0.3s" in f.issue for f in findings_c6), "Case 6 Failed: Too fast transition duration missed"
    print("✔ [PASSED] Case 6 (Too Fast Transition Duration 0.1s - P2 Caught)")
    passed += 1

    # CASE 7: Optimal transition duration 1.0s (Valid - No False Positive)
    slide_c7 = {
        "slide_id": "c7",
        "title": "Nhịp điệu mượt mà",
        "transition": "fade",
        "transition_duration": 1.0
    }
    findings_c7 = agent.audit([{}, slide_c7])
    assert len(findings_c7) == 0, f"Case 7 Failed: False positive on 1.0s transition: {[f.issue for f in findings_c7]}"
    print("✔ [PASSED] Case 7 (Optimal Duration 1.0s - No False Positive)")
    passed += 1

    # CASE 8: Standard push transition (Valid - No False Positive)
    slide_c8 = {
        "slide_id": "c8",
        "title": "Chuyển cảnh dạng đẩy",
        "transition": "push",
        "transition_duration": 0.8
    }
    findings_c8 = agent.audit([{}, slide_c8])
    assert len(findings_c8) == 0, f"Case 8 Failed: False positive on standard push: {[f.issue for f in findings_c8]}"
    print("✔ [PASSED] Case 8 (Standard Push Transition - No False Positive)")
    passed += 1

    # CASE 9: Multiple morph shapes with mixed naming
    slide_c9 = {
        "slide_id": "c9",
        "title": "Biến hình hỗn hợp",
        "transition": "morph",
        "morph_shapes": ["!!valid_shape!!", "bad_shape"]
    }
    findings_c9 = agent.audit([{}, slide_c9])
    assert len(findings_c9) == 1 and "bad_shape" in findings_c9[0].issue, f"Case 9 Failed: Mixed morph shapes not filtered accurately: {[f.issue for f in findings_c9]}"
    print("✔ [PASSED] Case 9 (Mixed Morph Shapes Isolation - Exactly 1 Caught)")
    passed += 1

    # CASE 10: Auto-Remediation Fixes Shapes, Slide 1 Morph, and Duration
    slide_c10_1 = {
        "slide_id": "c10_1",
        "title": "Trang bìa",
        "transition": "morph",
        "transition_duration": 4.0
    }
    slide_c10_2 = {
        "slide_id": "c10_2",
        "title": "Trang chi tiết",
        "transition": "morph",
        "transition_duration": 0.1,
        "morph_shapes": ["kpi_circle"],
        "shapes": [{"name": "bar_item", "morph": True}]
    }
    findings_c10 = agent.audit([slide_c10_1, slide_c10_2])
    assert len(findings_c10) >= 3, f"Case 10 Failed: Expected at least 3 findings, got {len(findings_c10)}"
    remediated = agent.auto_remediate([slide_c10_1, slide_c10_2], findings_c10)
    # Check slide 1 transition fixed to fade
    assert remediated[0]["transition"] == "fade", f"Slide 1 transition not changed from morph: {remediated[0]['transition']}"
    assert remediated[0]["transition_duration"] == 1.0, f"Slide 1 duration not normalized: {remediated[0]['transition_duration']}"
    # Check slide 2 shapes fixed
    assert "!!kpi_circle!!" in remediated[1]["morph_shapes"], f"morph_shapes not wrapped: {remediated[1]['morph_shapes']}"
    assert remediated[1]["shapes"][0]["name"] == "!!bar_item!!", f"shapes dict name not wrapped: {remediated[1]['shapes']}"
    assert remediated[1]["transition_duration"] == 1.0, f"Slide 2 duration not normalized: {remediated[1]['transition_duration']}"
    re_audit = agent.audit(remediated)
    assert len(re_audit) == 0, f"Case 10 Failed: Residual issues after auto-remediation: {[f.issue for f in re_audit]}"
    print("✔ [PASSED] Case 10 (Auto-Remediation Normalizes Motion & Passes Re-Audit)")
    passed += 1

    print("-" * 60)
    print(f"Total Score: {passed}/{total} ({passed/total*100:.1f}%)")
    print("=" * 60)
    assert passed == total, f"Adversarial matrix failed: {passed}/{total}"


if __name__ == "__main__":
    test_agent15_adversarial_matrix()

# -*- coding: utf-8 -*-
"""
tests/test_mas_v9_closed_loop.py
End-to-End Integration test for Make Slide Pro V9.0 Multi-Agent Closed-Loop Self-Healing System (MAS-CLSH).
Simulates discovery of defects, root-cause diagnosis, blueprint healing, and convergence verification.
"""

from scripts.mas_engine_v9 import (
    ContentGroundingAgent,
    InterSlideKineticMorphAgent,
    LayoutTypographyAgent,
    DataVizMathArchetypeAgent,
    RootCauseDiagnosticAgent,
    SlideAuditResult,
    DefectIssue,
)


def test_closed_loop_self_healing_convergence():
    # 1. Simulate a defective slide blueprint (Round 1)
    defective_bp = {
        "slide_id": "SLIDE_03",
        "transition": "wipe",  # Defect 1: Non-morph
        "transition_duration": 0.5,
        "content": {
            "assertion_title": "Quy Trình Quản Trị Dân Số Cấp Cơ Sở (",  # Defect 2: Dangling paren
            "cards": [
                {
                    "title": "Khuyến Nghị Áp Dụng: Vận dụng đồng bộ (",  # Defect 3: Cliché + dangling paren
                    "points": ["Triển khai điểm 1", "Triển khai điểm 2 ("],
                }
            ],
        },
    }

    content_agent = ContentGroundingAgent()
    motion_agent = InterSlideKineticMorphAgent()
    diagnostic_agent = RootCauseDiagnosticAgent()

    # --- ROUND 1 AUDIT ---
    # Audit content
    text_chunks = [
        defective_bp["content"]["assertion_title"],
        defective_bp["content"]["cards"][0]["title"],
        defective_bp["content"]["cards"][0]["points"][0],
        defective_bp["content"]["cards"][0]["points"][1],
    ]
    c_score_r1, c_defects_r1 = content_agent.inspect_text_strings(3, text_chunks)
    assert c_score_r1 < 60.0
    assert any(d.severity == "P0" for d in c_defects_r1)

    # Audit motion
    m_score_r1, m_defects_r1 = motion_agent.inspect_deck_transitions(
        slide_index=3,
        total_slides=50,
        entry_effect=3855,  # Wipe
        duration=0.5,
        timeline_triggers=[1, 1],
        has_atomic_groups=False,
    )
    assert m_score_r1 < 70.0
    assert any(d.severity == "P0" for d in m_defects_r1)

    all_defects_r1 = c_defects_r1 + m_defects_r1
    assert len(all_defects_r1) >= 3

    # --- ROOT-CAUSE DIAGNOSIS & REMEDIATION ---
    directives = diagnostic_agent.diagnose_slide(
        slide_index=3, defects=all_defects_r1, current_blueprint=defective_bp
    )
    assert len(directives) >= 2

    # Synthesize healed blueprint
    healed_bp = dict(defective_bp)
    for d in directives:
        if d.updated_blueprint:
            if d.target_domain == "CONTENT":
                healed_bp["content"] = d.updated_blueprint["content"]
            elif d.target_domain == "MOTION":
                healed_bp["transition"] = d.updated_blueprint["transition"]
                healed_bp["transition_duration"] = d.updated_blueprint["transition_duration"]
                healed_bp["atomic_card"] = True
                healed_bp["safe_group"] = True

    # --- ROUND 2 RE-AUDIT (POST-HEALING) ---
    healed_text_chunks = [
        healed_bp["content"]["assertion_title"],
        healed_bp["content"]["cards"][0]["title"],
        healed_bp["content"]["cards"][0]["points"][0],
        healed_bp["content"]["cards"][0]["points"][1],
    ]
    c_score_r2, c_defects_r2 = content_agent.inspect_text_strings(3, healed_text_chunks)
    # Check that dangling parens and clichés are gone
    assert not any(d.severity == "P0" for d in c_defects_r2)
    assert c_score_r2 >= 90.0

    # Check motion is now Morph (3954, 0.85s)
    m_score_r2, m_defects_r2 = motion_agent.inspect_deck_transitions(
        slide_index=3,
        total_slides=50,
        entry_effect=3954,  # Morph
        duration=0.85,
        timeline_triggers=[2, 1],  # Card 0 WithPrev, Card 1 OnClick
        has_atomic_groups=True,
    )
    assert m_score_r2 == 100.0
    assert len(m_defects_r2) == 0

    # Final Convergence Assessment
    converged_overall = (c_score_r2 * 0.5) + (m_score_r2 * 0.5)
    assert converged_overall >= 95.0
    print(f"\n[Test Result] Closed-loop self-healing converged from R1 ({c_score_r1:.1f}/{m_score_r1:.1f}) to R2 ({c_score_r2:.1f}/{m_score_r2:.1f})!")

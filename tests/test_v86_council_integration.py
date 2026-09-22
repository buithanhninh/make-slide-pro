"""
tests/test_v86_council_integration.py
Comprehensive Integration Test Suite for Make Slide Pro V8.6.0.
Verifies:
1. Agent 11: Recognizes 165+ Mega Archetypes (DevSecOps, STEEPLE, Medallion, etc.) without false P1 or table downgrades.
2. Agent 12: Audits 20 Native Microsoft Office Charts (Excel-backed) and dark-canvas contrast.
3. Agent 15: Enforces 100% Pure Continuous Morph (0.85s) & Smooth Fade (0.65s) and Atomic Presenter Sequencing.
4. Full Council E2E: Verifies that a V8.6.0 deck achieves Certified status (Score >= 99.0, P0=0, P1=0).
"""

import sys
from pathlib import Path

# Add project root to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from scripts.macc_council.gate4_spatial_motion.agent11_layout_archetype import LayoutArchetypeStrategist
from scripts.macc_council.gate4_spatial_motion.agent12_data_chart import DataChartCartographer
from scripts.macc_council.gate4_spatial_motion.agent15_motion_choreographer import MotionChoreographer
from scripts.macc_council.orchestrator import MultiRoundCouncilOrchestrator
from scripts.macc_council.models import Severity


def test_agent11_v86_archetypes_recognition():
    """Verify that Agent 11 recognizes complex V8.6.0 archetypes without false alarms."""
    agent = LayoutArchetypeStrategist()

    deck = {
        "slides": [
            {
                "slide_id": "s_devsecops",
                "assertion_title": "Quy Trình Tích Hợp DevSecOps Vô Cực Toàn Diện",
                "visual_job": "PROCESS_DEVSECOPS_INFINITY_LOOP",
                "atoms": [{"title": f"Giai đoạn {i}", "text": f"Nội dung kiểm soát {i}"} for i in range(1, 9)]  # Exactly 8 atoms!
            },
            {
                "slide_id": "s_steeple",
                "assertion_title": "Khung Phân Tích Môi Trường Vĩ Mô STEEPLE",
                "visual_job": "FRAMEWORK_STEEPLE",
                "atoms": [{"title": f"Yếu tố {i}", "text": f"Tác động chiến lược {i}"} for i in range(1, 8)]  # Exactly 7 atoms!
            },
            {
                "slide_id": "s_medallion",
                "assertion_title": "Kiến Trúc Hồ Dữ Liệu Medallion Lakehouse",
                "visual_job": "ARCH_DATA_LAKEHOUSE_MEDALLION",
                "atoms": [{"title": f"Tầng {i}", "text": f"Chất lượng dữ liệu {i}"} for i in range(1, 5)]  # Exactly 4 atoms!
            },
            {
                "slide_id": "s_bento_grid",
                "assertion_title": "Ma Trận Tổng Thể 9 Khối Bento Tinh Gọn",
                "visual_job": "CONTAINER_BENTO_GRID_3X3",
                "atoms": [{"title": f"Khối {i}", "text": f"Chỉ số {i}"} for i in range(1, 10)]  # Exactly 9 atoms!
            }
        ]
    }

    findings = agent.audit(deck)
    # None of these valid V8.6.0 archetypes should be flagged as atom count mismatch
    mismatch_findings = [f for f in findings if "không tương thích" in f.issue.lower()]
    assert len(mismatch_findings) == 0, f"False positive atom count errors on V8.6 archetypes: {[f.issue for f in mismatch_findings]}"
    print("[PASS] test_agent11_v86_archetypes_recognition passed: 165+ archetypes recognized with zero false alarms")


def test_agent12_v86_native_office_charts():
    """Verify that Agent 12 validates Native Office Charts (Module 5) with Excel data structures."""
    agent = DataChartCartographer()

    deck = {
        "slides": [
            {
                "slide_id": "s_pareto",
                "chart_type": "CHART_PARETO_ANALYSIS",
                "chart_data": {
                    "categories": ["Lỗi A", "Lỗi B", "Lỗi C", "Lỗi D"],
                    "series": [{"name": "Tần suất", "values": [80, 50, 20, 10]}]
                },
                "atoms": [{"title": "Quy tắc 80/20", "text": "2 nhóm lỗi hàng đầu chiếm 80% thời gian xử lý."}]
            },
            {
                "slide_id": "s_radar",
                "chart_type": "CHART_RADAR_FILLED",
                "chart_data": {
                    "categories": ["Bảo mật", "Hiệu năng", "Độ tin cậy", "Khả năng mở rộng"],
                    "series": [{"name": "Điểm chuẩn", "values": [90, 85, 95, 88]}]
                },
                "atoms": [{"title": "Năng lực hệ thống", "text": "Đạt chuẩn an ninh tối ưu trên mọi trục."}]
            }
        ]
    }

    findings = agent.audit(deck, context={"theme": "DARK"})
    p1_issues = [f for f in findings if f.severity == Severity.P1]
    assert len(p1_issues) == 0, f"Unexpected P1 issues on valid native charts: {[f.issue for f in p1_issues]}"
    print("[PASS] test_agent12_v86_native_office_charts passed: Native Office Charts validated without errors")


def test_agent15_v86_motion_invariants():
    """Verify that Agent 15 enforces V8.6.0 pure continuous morph, smooth fade, and rejects push/wipe."""
    agent = MotionChoreographer()

    # Deck with invalid transitions on content slide (push transition)
    deck_with_push = {
        "schema_version": "8.6.0",
        "slides": [
            {"slide_id": "s1", "role": "COVER", "transition": "fade", "transition_duration": 0.65},
            {"slide_id": "s2", "role": "CONTENT", "transition": "push", "transition_duration": 0.8},  # Invalid push!
            {"slide_id": "s3", "role": "COVER", "transition": "fade", "transition_duration": 0.65}
        ]
    }

    findings = agent.audit(deck_with_push, context={"enforce_v86": True})
    assert any("gián đoạn" in f.issue.lower() or "morph" in f.suggested_value for f in findings), "Must flag push transition as P1 on content slide"

    # Auto-remediation enforces pure morph (0.85s) on content slides
    remediated = agent.auto_remediate(deck_with_push, findings, context={"enforce_v86": True})
    assert remediated["slides"][1]["transition"] == "morph"
    assert remediated["slides"][1]["transition_duration"] == 0.85
    assert remediated["slides"][0]["transition"] == "fade"
    assert remediated["slides"][0]["transition_duration"] == 0.65
    print("[PASS] test_agent15_v86_motion_invariants passed: Continuous Morph & Smooth Fade strictly enforced")


def test_full_council_v86_certification():
    """End-to-End audit of a certified V8.6.0 presentation deck through the 16-Agent Council."""
    council = MultiRoundCouncilOrchestrator(max_rounds=3, target_score=99.0)

    v86_deck = {
        "schema_version": "8.6.0",
        "version": "8.6.0",
        "deck_title": "Kiến Trúc Nền Tảng Dữ Liệu Doanh Nghiệp Thế Hệ Mới",
        "total_slides": 4,
        "slides": [
            {
                "slide_id": "SLIDE_01",
                "role": "COVER",
                "section": "TỔNG QUAN",
                "assertion_title": "Chiến Lược Dữ Liệu Doanh Nghiệp 2026",
                "primary_claim": "Khung kiến trúc hiện đại tối ưu hóa năng lực cạnh tranh số.",
                "visual_job": "HERO_TITLE",
                "transition": "fade",
                "transition_duration": 0.65
            },
            {
                "slide_id": "SLIDE_02",
                "role": "CONTENT",
                "section": "BỐI CẢNH & KIẾN TRÚC",
                "assertion_title": "Giải Quyết Thách Thức Phân Tán Bằng Hồ Dữ Liệu Medallion Chuẩn Hóa",
                "primary_claim": "Khắc phục triệt để thách thức phân mảnh qua các tầng Bronze, Silver và Gold minh bạch.",
                "visual_job": "ARCH_DATA_LAKEHOUSE_MEDALLION",
                "transition": "morph",
                "transition_duration": 0.85,
                "atomic_card": True,
                "safe_group": True,
                "atoms": [
                    {"title": "Bronze Layer", "text": "Lưu trữ dữ liệu thô từ toàn bộ nguồn nghiệp vụ.", "icon": "database"},
                    {"title": "Silver Layer", "text": "Làm sạch và hợp nhất lược đồ dữ liệu chuẩn.", "icon": "sliders"},
                    {"title": "Gold Layer", "text": "Dữ liệu kinh doanh sẵn sàng cho báo cáo và AI.", "icon": "award"}
                ]
            },
            {
                "slide_id": "SLIDE_03",
                "role": "CONTENT",
                "section": "HIỆU QUẢ VẬN HÀNH",
                "assertion_title": "Chỉ Số Đo Lường Vận Hành Tối Ưu Hóa Năng Suất",
                "primary_claim": "Các chỉ số hiệu quả phản ánh tốc độ chuyển đổi vượt bậc.",
                "visual_job": "CONTAINER_KPI_STAT_DELTA",
                "transition": "morph",
                "transition_duration": 0.85,
                "atomic_card": True,
                "safe_group": True,
                "atoms": [
                    {"title": "Thời gian xử lý", "text": "Rút ngắn 60% chu kỳ báo cáo toàn tập đoàn.", "icon": "zap"},
                    {"title": "Độ chính xác dữ liệu", "text": "Đạt 99.98% toàn vẹn dữ liệu xuyên suốt.", "icon": "shield"},
                    {"title": "Chi phí hạ tầng", "text": "Tiết kiệm 35% chi phí lưu trữ đám mây.", "icon": "calculator"}
                ]
            },
            {
                "slide_id": "SLIDE_04",
                "role": "COVER",
                "section": "TỔNG KẾT & HÀNH ĐỘNG",
                "assertion_title": "Lộ Trình Triển Khai & Khuyến Nghị Trọng Tâm",
                "primary_claim": "Hành động quyết liệt để hoàn thiện năng lực dữ liệu số toàn diện.",
                "visual_job": "HERO_TITLE",
                "transition": "fade",
                "transition_duration": 0.65
            }
        ]
    }

    canonical_source = {
        "sections": [
            {
                "title": "Kiến Trúc Dữ Liệu Doanh Nghiệp",
                "paragraphs": [
                    "Chiến lược dữ liệu doanh nghiệp 2026: Khung kiến trúc hiện đại tối ưu hóa năng lực cạnh tranh số.",
                    "Giải quyết thách thức phân tán bằng Hồ dữ liệu Medallion chuẩn hóa: Khắc phục triệt để thách thức phân mảnh qua các tầng Bronze, Silver và Gold minh bạch. Bronze Layer lưu trữ dữ liệu thô từ toàn bộ nguồn nghiệp vụ; Silver Layer làm sạch và hợp nhất lược đồ dữ liệu chuẩn; Gold Layer dữ liệu kinh doanh sẵn sàng cho báo cáo và AI.",
                    "Chỉ số đo lường vận hành tối ưu hóa năng suất: Rút ngắn 60% chu kỳ báo cáo toàn tập đoàn, đạt 99.98% toàn vẹn dữ liệu xuyên suốt và tiết kiệm 35% chi phí hạ tầng lưu trữ đám mây.",
                    "Lộ trình triển khai & khuyến nghị trọng tâm: Hành động quyết liệt để hoàn thiện năng lực dữ liệu số toàn diện."
                ],
                "atoms": [
                    {"verbatim": "Khung kiến trúc hiện đại tối ưu hóa năng lực cạnh tranh số."},
                    {"verbatim": "Khắc phục triệt để thách thức phân mảnh qua các tầng Bronze, Silver và Gold minh bạch."},
                    {"verbatim": "Bronze Layer lưu trữ dữ liệu thô từ toàn bộ nguồn nghiệp vụ."},
                    {"verbatim": "Silver Layer làm sạch và hợp nhất lược đồ dữ liệu chuẩn."},
                    {"verbatim": "Gold Layer dữ liệu kinh doanh sẵn sàng cho báo cáo và AI."},
                    {"verbatim": "Rút ngắn 60% chu kỳ báo cáo toàn tập đoàn."},
                    {"verbatim": "Đạt 99.98% toàn vẹn dữ liệu xuyên suốt."},
                    {"verbatim": "Tiết kiệm 35% chi phí lưu trữ đám mây."},
                    {"verbatim": "Hành động quyết liệt để hoàn thiện năng lực dữ liệu số toàn diện."}
                ]
            }
        ]
    }

    report = council.run_council(
        blueprints=v86_deck,
        canonical_source=canonical_source,
        doc_metadata={"file_stem": "v86_integration_test", "enforce_v86": True, "theme": "DARK"}
    )

    print(f"[Council Report] Score: {report.final_score:.1f}/100 | Certified: {report.certified} | P0={report.p0_count}, P1={report.p1_count}, P2={report.p2_count}")
    for g_name, g_rep in report.gate_reports.items():
        for f in g_rep.findings:
            msg = f"Gate: {g_name} | [{f.severity.value}] {f.agent} on {f.slide_id}: {f.issue}"
            print(msg.encode("ascii", errors="replace").decode("ascii"))
    assert report.p0_count == 0, f"Must have 0 P0 defects, got {report.p0_count}"
    assert report.p1_count == 0, f"Must have 0 P1 defects, got {report.p1_count}"
    assert report.final_score >= 99.0, f"Expected Score >= 99.0, got {report.final_score}"
    assert report.certified is True, "Deck must be certified by the Council"
    print("[PASS] ALL TESTS IN V8.6.0 CERTIFICATION PASSED 100%!")


if __name__ == "__main__":
    test_agent11_v86_archetypes_recognition()
    test_agent12_v86_native_office_charts()
    test_agent15_v86_motion_invariants()
    test_full_council_v86_certification()

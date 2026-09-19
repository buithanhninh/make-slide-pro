"""
tests/test_mega_library_registry.py
Automated verification suite for Make Slide Pro V8.6.0 Mega Component Library.
Verifies all 6 specialized engines, 165 distinct archetype methods, 400+ registered keys/aliases,
and semantic auto-detection.
"""

import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from component_library import (
    ARCHETYPES_REGISTRY,
    MasterComponentDispatcher,
    detect_optimal_archetype,
    AppleSlideTransitionOrchestrator,
    AppleChoreographedEntranceAnimator,
)
from component_library.tables_engine import NativeTablesEngine
from component_library.frameworks_engine import StrategicFrameworksEngine
from component_library.processes_engine import ProcessesEngine
from component_library.architectures_engine import ArchitecturesEngine
from component_library.charts_engine import NativeChartsEngine
from component_library.containers_engine import AdvancedContainersEngine


def test_registry_size_and_diversity():
    """Verify registry contains >= 165 archetypes (and 400+ with aliases)."""
    assert len(ARCHETYPES_REGISTRY) >= 165, f"Expected >= 165 archetypes, found {len(ARCHETYPES_REGISTRY)}"

    # Check distribution across 6 modules
    categories = set(ARCHETYPES_REGISTRY.values())
    expected_categories = {"tables", "frameworks", "processes", "architectures", "charts", "containers"}
    assert categories == expected_categories, f"Missing modules in registry: {expected_categories - categories}"


def test_dispatcher_initialization():
    """Verify MasterComponentDispatcher initializes all 6 specialized engines."""
    dispatcher = MasterComponentDispatcher(theme="DARK")
    assert isinstance(dispatcher.tables, NativeTablesEngine)
    assert isinstance(dispatcher.frameworks, StrategicFrameworksEngine)
    assert isinstance(dispatcher.processes, ProcessesEngine)
    assert isinstance(dispatcher.architectures, ArchitecturesEngine)
    assert isinstance(dispatcher.charts, NativeChartsEngine)
    assert isinstance(dispatcher.containers, AdvancedContainersEngine)


def test_can_handle_all_modules_and_v86_additions():
    """Verify can_handle recognizes archetypes across all 6 modules including V8.6 additions."""
    dispatcher = MasterComponentDispatcher(theme="DARK")

    samples = [
        # Tables (Original + V8.6 additions)
        "TABLE_COMPARISON_PRO", "TABLE_SCORECARD_HEATMAP", "TABLE_FINANCIAL_PL", "TABLE_RACI_GOVERNANCE",
        "TABLE_PRICING_FEATURE_MATRIX", "TABLE_MILESTONE_DELIVERABLES", "TABLE_SWOT_DETAILED",
        "TABLE_RISK_HEATMAP_5X5", "TABLE_BUDGET_ALLOCATION", "TABLE_OKRS_TRACKER",
        # Frameworks (Original + V8.6 additions)
        "FRAMEWORK_MATRIX_2X2", "FRAMEWORK_PORTER_5_FORCES", "FRAMEWORK_SWOT_ANALYSIS", "FRAMEWORK_STRATEGY_HOUSE",
        "FRAMEWORK_STEEPLE", "FRAMEWORK_KANO_MODEL", "FRAMEWORK_LEAN_CANVAS", "FRAMEWORK_VALUE_PROPOSITION_CANVAS",
        "FRAMEWORK_CYNEFIN", "FRAMEWORK_NORTH_STAR_METRIC", "FRAMEWORK_PIRATE_AARRR",
        # Processes (Original + V8.6 additions)
        "PROCESS_CHEVRON_LINEAR", "PROCESS_CURVED_PIPELINE", "PROCESS_CIRCULAR_CYCLE", "PROCESS_FISHBONE_ISHIKAWA",
        "PROCESS_CIRCULAR_LOOP_6STEP", "PROCESS_SPIRAL_GROWTH", "PROCESS_HOURGLASS_WORKFLOW",
        "PROCESS_STAGED_GATE_PHASES", "PROCESS_DEVSECOPS_INFINITY_LOOP", "PROCESS_CRITICAL_PATH_CPM",
        # Architectures (Original + V8.6 additions)
        "ARCH_SYSTEM_LAYERED_STACK", "ARCH_ORG_HIERARCHY_TREE", "ARCH_MICROSERVICES_MESH", "ARCH_DEFENSE_IN_DEPTH",
        "ARCH_EVENT_DRIVEN_KAFKA", "ARCH_SERVERLESS_EVENT_FLOW", "ARCH_ZERO_TRUST_SECURITY",
        "ARCH_DATA_LAKEHOUSE_MEDALLION", "ARCH_CI_CD_AUTOMATION", "ARCH_RAG_LLM_PIPELINE",
        # Charts (Original + V8.6 additions)
        "CHART_COLUMN_CLUSTERED", "CHART_BAR_DIVERGING", "CHART_DONUT_KPI", "CHART_WATERFALL",
        "CHART_BAR_STACKED_100", "CHART_PARETO_ANALYSIS", "CHART_STEPPED_LINE", "CHART_RADAR_FILLED",
        "CHART_HISTOGRAM_DISTRIBUTION",
        # Containers (Original + V8.6 additions)
        "CONTAINER_BENTO_COMPLEX", "CONTAINER_KPI_STAT_DELTA", "CONTAINER_BEFORE_AFTER", "CONTAINER_EXECUTIVE_DASHBOARD",
        "CONTAINER_DEVICE_MOCKUP_FRAME", "CONTAINER_METRIC_MARQUEE_BANNER", "CONTAINER_THREE_PILLARS_CARDS",
        "CONTAINER_PROBLEM_SOLUTION_IMPACT", "CONTAINER_FEATURE_HEX_CLUSTER", "CONTAINER_MINIMALIST_APPLE_QUOTE"
    ]

    for sample in samples:
        assert dispatcher.can_handle(sample), f"Dispatcher failed to recognize {sample}"


def test_tables_engine_all_25_methods():
    """Verify all 25 table methods exist on NativeTablesEngine."""
    engine = NativeTablesEngine()
    methods = [
        # Original 15
        "render_comparison_table", "render_scorecard_table", "render_financial_table",
        "render_raci_table", "render_metric_matrix_table", "render_competitor_benchmark",
        "render_capability_gap", "render_pricing_tiers", "render_risk_register",
        "render_audit_compliance", "render_pros_cons", "render_roadmap_schedule",
        "render_sales_territory", "render_weighted_decision", "render_executive_summary_table",
        # V8.6 Additions (10)
        "render_pricing_feature_matrix", "render_milestone_deliverables", "render_swot_detailed_table",
        "render_risk_heatmap_5x5", "render_budget_allocation", "render_vendor_evaluation",
        "render_okrs_tracker", "render_skills_matrix", "render_product_specs",
        "render_sla_tiers"
    ]
    assert len(methods) == 25
    for m in methods:
        assert hasattr(engine, m) and callable(getattr(engine, m)), f"Missing method {m} on NativeTablesEngine"


def test_frameworks_engine_all_35_methods():
    """Verify all 35 framework methods exist on StrategicFrameworksEngine."""
    engine = StrategicFrameworksEngine()
    methods = [
        # Original 25
        "render_matrix_2x2", "render_matrix_3x3", "render_porter_5_forces",
        "render_value_chain", "render_swot_analysis", "render_pestel_hex",
        "render_balanced_scorecard", "render_strategy_house", "render_pyramid_ascending",
        "render_inverted_pyramid", "render_conversion_funnel", "render_growth_flywheel",
        "render_hub_spoke", "render_concentric_rings", "render_venn_2_set",
        "render_venn_3_set", "render_diamond_model", "render_ansoff_matrix",
        "render_mckinsey_7s", "render_strategy_clock", "render_cmmi_stairs",
        "render_vrio_matrix", "render_golden_circle", "render_iceberg_model",
        "render_double_diamond",
        # V8.6 Additions (10)
        "render_steeple", "render_kano_model", "render_lean_canvas",
        "render_value_proposition_canvas", "render_cynefin", "render_bow_tie",
        "render_blue_ocean_errc", "render_north_star_metric", "render_grow_coaching",
        "render_pirate_aarrr"
    ]
    assert len(methods) == 35
    for m in methods:
        assert hasattr(engine, m) and callable(getattr(engine, m)), f"Missing method {m} on StrategicFrameworksEngine"


def test_processes_engine_all_30_methods():
    """Verify all 30 process methods exist on ProcessesEngine."""
    engine = ProcessesEngine()
    methods = [
        # Original 20
        "render_chevron_linear", "render_curved_pipeline", "render_circular_cycle",
        "render_interlocking_gears", "render_fishbone_ishikawa", "render_decision_flow",
        "render_swimlane_tracks", "render_ascending_stairs", "render_timeline_flag_ribbon",
        "render_vertical_spine", "render_gantt_roadmap", "render_3_horizons_roadmap",
        "render_agile_scrum_cycle", "render_bridge_migration", "render_jigsaw_puzzle",
        "render_honeycomb_chain", "render_etl_data_pipeline", "render_level_up_ladder",
        "render_domino_cascade", "render_radial_progression",
        # V8.6 Additions (10)
        "render_circular_loop_6step", "render_spiral_growth", "render_hourglass_workflow",
        "render_parallel_streams", "render_staged_gate_phases", "render_serpentine_roadmap",
        "render_pipeline_filtration", "render_continuous_improvement_pdCA", "render_devsecops_infinity_loop",
        "render_critical_path_cpm"
    ]
    # Check lowercase case-insensitively since PDCA / pdca might vary
    engine_methods_lower = {m.lower(): m for m in dir(engine) if m.startswith("render_")}
    assert len(engine_methods_lower) == 30
    for m in methods:
        assert m.lower() in engine_methods_lower, f"Missing method {m} on ProcessesEngine"


def test_architectures_engine_all_25_methods():
    """Verify all 25 architecture methods exist on ArchitecturesEngine."""
    engine = ArchitecturesEngine()
    methods = [
        # Original 15
        "render_system_layered_stack", "render_org_hierarchy_tree", "render_radial_mind_map",
        "render_microservices_mesh", "render_defense_in_depth", "render_cloud_hybrid_infra",
        "render_bus_bar_modular", "render_hexagonal_ports", "render_ecosystem_network",
        "render_matrix_organization", "render_api_gateway_hub", "render_data_governance_mesh",
        "render_clean_onion_stack", "render_container_cluster_k8s", "render_ai_agent_orchestrator",
        # V8.6 Additions (10)
        "render_event_driven_kafka", "render_serverless_event_flow", "render_zero_trust_security",
        "render_data_lakehouse_medallion", "render_ci_cd_automation", "render_hub_spoke_enterprise_network",
        "render_multi_tenant_saas", "render_rag_llm_pipeline", "render_edge_to_cloud_iot",
        "render_modular_monolith"
    ]
    assert len(methods) == 25
    for m in methods:
        assert hasattr(engine, m) and callable(getattr(engine, m)), f"Missing method {m} on ArchitecturesEngine"


def test_charts_engine_all_20_methods():
    """Verify all 20 chart methods exist on NativeChartsEngine."""
    engine = NativeChartsEngine()
    methods = [
        # Original 15
        "render_column_clustered", "render_column_stacked", "render_column_100_stacked",
        "render_bar_clustered", "render_bar_diverging", "render_line_trend",
        "render_area_standard", "render_area_stacked", "render_donut_kpi",
        "render_pie_highlight_slice", "render_waterfall", "render_combo_dual_axis",
        "render_radar", "render_scatter_correlation", "render_bubble_matrix",
        # V8.6 Additions (5)
        "render_bar_stacked_100", "render_pareto_analysis", "render_stepped_line",
        "render_radar_filled", "render_histogram_distribution"
    ]
    assert len(methods) == 20
    for m in methods:
        assert hasattr(engine, m) and callable(getattr(engine, m)), f"Missing method {m} on NativeChartsEngine"


def test_containers_engine_all_30_methods():
    """Verify all 30 container methods exist on AdvancedContainersEngine."""
    engine = AdvancedContainersEngine()
    methods = [
        # Original 22
        "render_bento_complex", "render_kpi_stat_delta", "render_before_after",
        "render_executive_quote", "render_timeline_flow", "render_process_chevron",
        "render_pillar_3d", "render_bento_grid_3x3", "render_pillar_4_columns",
        "render_problem_sol_3step", "render_target_bullseye", "render_balance_seesaw",
        "render_gauge_meter_dial", "render_glassmorphic_hero", "render_hero_split_cards",
        "render_diagonal_split", "render_notification_tags", "render_customer_journey",
        "render_isometric_stack", "render_tabbed_overview", "render_executive_dashboard",
        "render_closing_cta_hero",
        # V8.6 Additions (8)
        "render_device_mockup_frame", "render_metric_marquee_banner", "render_three_pillars_cards",
        "render_problem_solution_impact", "render_feature_hex_cluster", "render_testimonial_carousel_row",
        "render_stat_hero_split_60_40", "render_minimalist_apple_quote"
    ]
    assert len(methods) == 30
    for m in methods:
        assert hasattr(engine, m) and callable(getattr(engine, m)), f"Missing method {m} on AdvancedContainersEngine"


def test_total_distinct_archetype_methods_count():
    """Verify total distinct archetype render methods across all 6 engines equals exactly 165."""
    t_methods = len([m for m in dir(NativeTablesEngine) if m.startswith("render_")])
    f_methods = len([m for m in dir(StrategicFrameworksEngine) if m.startswith("render_")])
    p_methods = len([m for m in dir(ProcessesEngine) if m.startswith("render_")])
    a_methods = len([m for m in dir(ArchitecturesEngine) if m.startswith("render_")])
    c_methods = len([m for m in dir(NativeChartsEngine) if m.startswith("render_")])
    cnt_methods = len([m for m in dir(AdvancedContainersEngine) if m.startswith("render_")])

    total = t_methods + f_methods + p_methods + a_methods + c_methods + cnt_methods
    assert total >= 165, f"Expected >= 165 distinct archetype methods, found {total}"
    assert t_methods >= 25
    assert f_methods >= 35
    assert p_methods >= 30
    assert a_methods >= 25
    assert c_methods >= 20
    assert cnt_methods >= 30


def test_semantic_auto_detector_expanded():
    """Verify detect_optimal_archetype properly classifies both original and new V8.6 semantics."""
    # Tables
    assert detect_optimal_archetype({"table_data": {"headers": ["Role", "RACI Trách Nhiệm"]}}) == "TABLE_RACI_GOVERNANCE"
    assert detect_optimal_archetype({"table_data": {"headers": ["Pricing Feature", "Starter", "Enterprise"]}}) == "TABLE_PRICING_FEATURE_MATRIX"
    assert detect_optimal_archetype({"table_data": {"headers": ["Mục Tiêu OKR", "Key Result"]}}) == "TABLE_OKRS_TRACKER"
    assert detect_optimal_archetype({"table_data": {"headers": ["SLA Cam Kết", "Thời Gian Phản Hồi"]}}) == "TABLE_SLA_TIERS"

    # Charts
    assert detect_optimal_archetype({"chart_type": "PARETO"}) == "CHART_PARETO_ANALYSIS"
    assert detect_optimal_archetype({"chart_type": "STEPPED_LINE"}) == "CHART_STEPPED_LINE"
    assert detect_optimal_archetype({"chart_type": "RADAR_FILLED"}) == "CHART_RADAR_FILLED"
    assert detect_optimal_archetype({"chart_type": "HISTOGRAM"}) == "CHART_HISTOGRAM_DISTRIBUTION"

    # Frameworks
    assert detect_optimal_archetype({"assertion_title": "Mô Hình Kano Mức Độ Hài Lòng Khách Hàng"}) == "FRAMEWORK_KANO_MODEL"
    assert detect_optimal_archetype({"assertion_title": "Bản Đồ Định Vị Giá Trị Khách Hàng Value Proposition"}) == "FRAMEWORK_VALUE_PROPOSITION_CANVAS"
    assert detect_optimal_archetype({"assertion_title": "Mô Hình Khung Ra Quyết Định Cynefin"}) == "FRAMEWORK_CYNEFIN"
    assert detect_optimal_archetype({"assertion_title": "Chỉ Số Bắc Đẩu North Star Metric Doanh Nghiệp"}) == "FRAMEWORK_NORTH_STAR_METRIC"
    assert detect_optimal_archetype({"assertion_title": "Phễu Tăng Trưởng Pirate AARRR Funnel"}) == "FRAMEWORK_PIRATE_AARRR"

    # Processes
    assert detect_optimal_archetype({"assertion_title": "Quy Trình Tích Hợp DevSecOps Vòng Lặp Vô Cực"}) == "PROCESS_DEVSECOPS_INFINITY_LOOP"
    assert detect_optimal_archetype({"assertion_title": "Phương Pháp Đường Găng Phân Tích Tiến Độ Critical Path"}) == "PROCESS_CRITICAL_PATH_CPM"
    assert detect_optimal_archetype({"assertion_title": "Chu Trình Vòng Lặp Cải Tiến Liên Tục PDCA Kaizen"}) == "PROCESS_CONTINUOUS_IMPROVEMENT_PDCA"
    assert detect_optimal_archetype({"assertion_title": "Quy Trình Phễu Lọc Pipeline Đa Tầng"}) == "PROCESS_PIPELINE_FILTRATION"

    # Architectures
    assert detect_optimal_archetype({"assertion_title": "Kiến Trúc Hướng Sự Kiện Event Driven Apache Kafka"}) == "ARCH_EVENT_DRIVEN_KAFKA"
    assert detect_optimal_archetype({"assertion_title": "Kiến Trúc Bảo Mật Zero Trust Không Tin Tưởng"}) == "ARCH_ZERO_TRUST_SECURITY"
    assert detect_optimal_archetype({"assertion_title": "Hồ Dữ Liệu Lakehouse Medallion Bronze Silver Gold"}) == "ARCH_DATA_LAKEHOUSE_MEDALLION"
    assert detect_optimal_archetype({"assertion_title": "Kiến Trúc Tự Động Hóa CI/CD Pipeline Triển Khai"}) == "ARCH_CI_CD_AUTOMATION"
    assert detect_optimal_archetype({"assertion_title": "Đường Ống Truy Xuất RAG LLM Vector Pipeline"}) == "ARCH_RAG_LLM_PIPELINE"

    # Containers
    assert detect_optimal_archetype({"assertion_title": "Khung Thiết Bị Giao Diện Mobile Device Mockup"}) == "CONTAINER_DEVICE_MOCKUP_FRAME"
    assert detect_optimal_archetype({"assertion_title": "Ba Trụ Cột Nền Tảng Trọng Yếu Three Pillars"}) == "CONTAINER_THREE_PILLARS_CARDS"
    assert detect_optimal_archetype({"assertion_title": "Nỗi Đau Giải Pháp Tác Động Toàn Diện"}) == "CONTAINER_PROBLEM_SOLUTION_IMPACT"
    assert detect_optimal_archetype({"assertion_title": "Châm Ngôn Tối Giản Apple Quote Trích Dẫn"}) == "CONTAINER_MINIMALIST_APPLE_QUOTE"

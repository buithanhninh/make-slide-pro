"""
tests/test_mega_library_registry.py
Automated verification suite for Make Slide Pro V8.5.0 Mega Component Library.
Verifies all 6 specialized engines, 110+ registered archetypes, and semantic auto-detection.
"""

import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from component_library import (
    ARCHETYPES_REGISTRY,
    MasterComponentDispatcher,
    detect_optimal_archetype
)
from component_library.tables_engine import NativeTablesEngine
from component_library.frameworks_engine import StrategicFrameworksEngine
from component_library.processes_engine import ProcessesEngine
from component_library.architectures_engine import ArchitecturesEngine
from component_library.charts_engine import NativeChartsEngine
from component_library.containers_engine import AdvancedContainersEngine


def test_registry_size_and_diversity():
    """Verify registry contains at least 110 archetype identifiers."""
    assert len(ARCHETYPES_REGISTRY) >= 110, f"Expected >= 110 archetypes, found {len(ARCHETYPES_REGISTRY)}"

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


def test_can_handle_all_modules():
    """Verify can_handle recognizes archetypes across all 6 modules."""
    dispatcher = MasterComponentDispatcher(theme="DARK")

    samples = [
        # Tables
        "TABLE_COMPARISON_PRO", "TABLE_SCORECARD_HEATMAP", "TABLE_FINANCIAL_PL", "TABLE_RACI_GOVERNANCE",
        # Frameworks
        "FRAMEWORK_MATRIX_2X2", "FRAMEWORK_PORTER_5_FORCES", "FRAMEWORK_SWOT_ANALYSIS", "FRAMEWORK_STRATEGY_HOUSE",
        # Processes
        "PROCESS_CHEVRON_LINEAR", "PROCESS_CURVED_PIPELINE", "PROCESS_CIRCULAR_CYCLE", "PROCESS_FISHBONE_ISHIKAWA",
        # Architectures
        "ARCH_SYSTEM_LAYERED_STACK", "ARCH_ORG_HIERARCHY_TREE", "ARCH_MICROSERVICES_MESH", "ARCH_DEFENSE_IN_DEPTH",
        # Charts
        "CHART_COLUMN_CLUSTERED", "CHART_BAR_DIVERGING", "CHART_DONUT_KPI", "CHART_WATERFALL",
        # Containers
        "CONTAINER_BENTO_COMPLEX", "CONTAINER_KPI_STAT_DELTA", "CONTAINER_BEFORE_AFTER", "CONTAINER_EXECUTIVE_DASHBOARD"
    ]

    for sample in samples:
        assert dispatcher.can_handle(sample), f"Dispatcher failed to recognize {sample}"


def test_tables_engine_methods():
    """Verify 15 table methods exist on NativeTablesEngine."""
    engine = NativeTablesEngine()
    methods = [
        "render_comparison_table", "render_scorecard_table", "render_financial_table",
        "render_raci_table", "render_metric_matrix_table", "render_competitor_benchmark",
        "render_capability_gap", "render_pricing_tiers", "render_risk_register",
        "render_audit_compliance", "render_pros_cons", "render_roadmap_schedule",
        "render_sales_territory", "render_weighted_decision", "render_executive_summary_table"
    ]
    for m in methods:
        assert hasattr(engine, m) and callable(getattr(engine, m)), f"Missing method {m} on NativeTablesEngine"


def test_frameworks_engine_methods():
    """Verify 25 framework methods exist on StrategicFrameworksEngine."""
    engine = StrategicFrameworksEngine()
    methods = [
        "render_matrix_2x2", "render_matrix_3x3", "render_porter_5_forces",
        "render_value_chain", "render_swot_analysis", "render_pestel_hex",
        "render_balanced_scorecard", "render_strategy_house", "render_pyramid_ascending",
        "render_inverted_pyramid", "render_conversion_funnel", "render_growth_flywheel",
        "render_hub_spoke", "render_concentric_rings", "render_venn_2_set",
        "render_venn_3_set", "render_diamond_model", "render_ansoff_matrix",
        "render_mckinsey_7s", "render_strategy_clock", "render_cmmi_stairs",
        "render_vrio_matrix", "render_golden_circle", "render_iceberg_model",
        "render_double_diamond"
    ]
    for m in methods:
        assert hasattr(engine, m) and callable(getattr(engine, m)), f"Missing method {m} on StrategicFrameworksEngine"


def test_processes_engine_methods():
    """Verify 20 process methods exist on ProcessesEngine."""
    engine = ProcessesEngine()
    methods = [
        "render_chevron_linear", "render_curved_pipeline", "render_circular_cycle",
        "render_interlocking_gears", "render_fishbone_ishikawa", "render_decision_flow",
        "render_swimlane_tracks", "render_ascending_stairs", "render_timeline_flag_ribbon",
        "render_vertical_spine", "render_gantt_roadmap", "render_3_horizons_roadmap",
        "render_agile_scrum_cycle", "render_bridge_migration", "render_jigsaw_puzzle",
        "render_honeycomb_chain", "render_etl_data_pipeline", "render_level_up_ladder",
        "render_domino_cascade", "render_radial_progression"
    ]
    for m in methods:
        assert hasattr(engine, m) and callable(getattr(engine, m)), f"Missing method {m} on ProcessesEngine"


def test_architectures_engine_methods():
    """Verify 15 architecture methods exist on ArchitecturesEngine."""
    engine = ArchitecturesEngine()
    methods = [
        "render_system_layered_stack", "render_org_hierarchy_tree", "render_radial_mind_map",
        "render_microservices_mesh", "render_defense_in_depth", "render_cloud_hybrid_infra",
        "render_bus_bar_modular", "render_hexagonal_ports", "render_ecosystem_network",
        "render_matrix_organization", "render_api_gateway_hub", "render_data_governance_mesh",
        "render_clean_onion_stack", "render_container_cluster_k8s", "render_ai_agent_orchestrator"
    ]
    for m in methods:
        assert hasattr(engine, m) and callable(getattr(engine, m)), f"Missing method {m} on ArchitecturesEngine"


def test_charts_engine_methods():
    """Verify 15 chart methods exist on NativeChartsEngine."""
    engine = NativeChartsEngine()
    methods = [
        "render_column_clustered", "render_column_stacked", "render_column_100_stacked",
        "render_bar_clustered", "render_bar_diverging", "render_line_trend",
        "render_area_standard", "render_area_stacked", "render_donut_kpi",
        "render_pie_highlight_slice", "render_waterfall", "render_combo_dual_axis",
        "render_radar", "render_scatter_correlation", "render_bubble_matrix"
    ]
    for m in methods:
        assert hasattr(engine, m) and callable(getattr(engine, m)), f"Missing method {m} on NativeChartsEngine"


def test_containers_engine_methods():
    """Verify 20+ container methods exist on AdvancedContainersEngine."""
    engine = AdvancedContainersEngine()
    methods = [
        "render_bento_complex", "render_kpi_stat_delta", "render_before_after",
        "render_executive_quote", "render_timeline_flow", "render_process_chevron",
        "render_pillar_3d", "render_bento_grid_3x3", "render_pillar_4_columns",
        "render_problem_sol_3step", "render_target_bullseye", "render_balance_seesaw",
        "render_gauge_meter_dial", "render_glassmorphic_hero", "render_hero_split_cards",
        "render_diagonal_split", "render_notification_tags", "render_customer_journey",
        "render_isometric_stack", "render_tabbed_overview", "render_executive_dashboard",
        "render_closing_cta_hero"
    ]
    for m in methods:
        assert hasattr(engine, m) and callable(getattr(engine, m)), f"Missing method {m} on AdvancedContainersEngine"


def test_semantic_auto_detector():
    """Verify detect_optimal_archetype properly classifies different slide semantics."""
    # 1. Table
    assert detect_optimal_archetype({"table_data": {"headers": ["Role", "RACI Trách Nhiệm"]}}) == "TABLE_RACI_GOVERNANCE"
    assert detect_optimal_archetype({"table_data": {"headers": ["Hạng Mục", "Doanh Thu", "Lợi Nhuận EBITDA"]}}) == "TABLE_FINANCIAL_PL"
    assert detect_optimal_archetype({"table_data": {"headers": ["Rủi Ro", "Xác Suất", "Thiệt Hại"]}}) == "TABLE_RISK_REGISTER"

    # 2. Chart
    assert detect_optimal_archetype({"chart_type": "DIVERGING_PYRAMID"}) == "CHART_BAR_DIVERGING_PYRAMID"
    assert detect_optimal_archetype({"chart_type": "DONUT_KPI"}) == "CHART_DONUT_KPI_CENTER"
    assert detect_optimal_archetype({"chart_type": "WATERFALL"}) == "CHART_WATERFALL_BRIDGE"

    # 3. Strategy Frameworks
    assert detect_optimal_archetype({"assertion_title": "Ma Trận 2x2 Đánh Giá Cơ Hội"}) == "FRAMEWORK_MATRIX_2X2"
    assert detect_optimal_archetype({"assertion_title": "Mô Hình 5 Áp Lực Cạnh Tranh Porter"}) == "FRAMEWORK_PORTER_5_FORCES"
    assert detect_optimal_archetype({"assertion_title": "Phân Tích SWOT Doanh Nghiệp"}) == "FRAMEWORK_SWOT_ANALYSIS"
    assert detect_optimal_archetype({"assertion_title": "Ngôi Nhà Chiến Lược 2030"}) == "FRAMEWORK_STRATEGY_HOUSE"

    # 4. Processes
    assert detect_optimal_archetype({"assertion_title": "Sơ Đồ Xương Cá Ishikawa Phân Tích Lỗi"}) == "PROCESS_FISHBONE_ISHIKAWA"
    assert detect_optimal_archetype({"assertion_title": "Chu Trình Vòng Tuần Hoàn PDCA"}) == "PROCESS_CIRCULAR_CYCLE"
    assert detect_optimal_archetype({"assertion_title": "Pipeline Xử Lý Dữ Liệu ETL"}) == "PROCESS_ETL_DATA_PIPELINE"

    # 5. Architectures
    assert detect_optimal_archetype({"assertion_title": "Kiến Trúc Phân Tầng Hệ Thống"}) == "ARCH_SYSTEM_LAYERED_STACK"
    assert detect_optimal_archetype({"assertion_title": "Mạng Lưới Microservices Đa Nền Tảng"}) == "ARCH_MICROSERVICES_MESH"
    assert detect_optimal_archetype({"assertion_title": "Hạ Tầng Đám Mây Lai Hybrid Cloud"}) == "ARCH_CLOUD_HYBRID_INFRA"

    # 6. Containers
    assert detect_optimal_archetype({"assertion_title": "Chuỗi 3 Bước Vấn Đề - Hệ Quả - Giải Pháp"}) == "CONTAINER_PROBLEM_SOL_3STEP"
    assert detect_optimal_archetype({"assertion_title": "Bảng Điều Khiển Tổng Giám Đốc Executive"}) == "CONTAINER_EXECUTIVE_DASHBOARD"
    assert detect_optimal_archetype({"assertion_title": "Kêu Gọi Hành Động Trải Nghiệm Ngay"}) == "CONTAINER_CLOSING_CTA_HERO"

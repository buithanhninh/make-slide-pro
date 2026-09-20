"""
scripts/component_library/__init__.py
Mega Component Library for Make Slide Pro V8.5.0.
Provides 110+ world-class presentation archetypes across 6 specialized modules:
- Module 1: 15 Native Data & Decision Tables (Excel-backed)
- Module 2: 25 Classic Strategic Frameworks (Pure Vector Shapes)
- Module 3: 20 Process, Flow & Mechanism Diagrams
- Module 4: 15 System, Technology & Hierarchy Architectures
- Module 5: 15 100% Native Microsoft Office Charts (Excel-backed)
- Module 6: 22 Advanced Keynote Containers, Bento Grids & Visual Accents
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional

from .tables_engine import NativeTablesEngine
from .frameworks_engine import StrategicFrameworksEngine
from .processes_engine import ProcessesEngine
from .architectures_engine import ArchitecturesEngine
from .charts_engine import NativeChartsEngine
from .containers_engine import AdvancedContainersEngine
from .motion_engine import AppleSlideTransitionOrchestrator, AppleChoreographedEntranceAnimator

# Master Registry of 165+ Archetypes and Aliases
ARCHETYPES_REGISTRY = {
    # -------------------------------------------------------------
    # MODULE 1: NATIVE TABLES (15 Archetypes + Aliases)
    # -------------------------------------------------------------
    "TABLE_COMPARISON_PRO": "tables",
    "TABLE_COMPARISON": "tables",
    "COMPARISON_TABLE": "tables",
    "TABLE_SCORECARD_HEATMAP": "tables",
    "TABLE_SCORECARD": "tables",
    "SCORECARD": "tables",
    "TABLE_FINANCIAL_PL": "tables",
    "TABLE_FINANCIAL": "tables",
    "FINANCIAL_TABLE": "tables",
    "TABLE_RACI_GOVERNANCE": "tables",
    "TABLE_RACI": "tables",
    "RACI_MATRIX": "tables",
    "TABLE_METRIC_MATRIX": "tables",
    "DATA_TABLE": "tables",
    "TABLE": "tables",
    "TABLE_MATRIX": "tables",
    "TABLE_COMPETITOR_BENCHMARK": "tables",
    "COMPETITOR_BENCHMARK": "tables",
    "TABLE_CAPABILITY_GAP": "tables",
    "CAPABILITY_GAP": "tables",
    "TABLE_PRICING_TIERS": "tables",
    "PRICING_TIERS": "tables",
    "TABLE_RISK_REGISTER": "tables",
    "RISK_REGISTER": "tables",
    "TABLE_AUDIT_COMPLIANCE": "tables",
    "AUDIT_COMPLIANCE": "tables",
    "TABLE_PROS_CONS": "tables",
    "PROS_CONS_TABLE": "tables",
    "TABLE_ROADMAP_SCHEDULE": "tables",
    "ROADMAP_SCHEDULE": "tables",
    "TABLE_SALES_TERRITORY": "tables",
    "SALES_TERRITORY": "tables",
    "TABLE_WEIGHTED_DECISION": "tables",
    "WEIGHTED_DECISION": "tables",
    "TABLE_EXECUTIVE_SUMMARY": "tables",
    "EXECUTIVE_SUMMARY_TABLE": "tables",
    "TABLE_PRICING_FEATURE_MATRIX": "tables",
    "PRICING_FEATURE_MATRIX": "tables",
    "TABLE_MILESTONE_DELIVERABLES": "tables",
    "MILESTONE_DELIVERABLES": "tables",
    "TABLE_SWOT_DETAILED": "tables",
    "SWOT_DETAILED_TABLE": "tables",
    "TABLE_RISK_HEATMAP_5X5": "tables",
    "RISK_HEATMAP_5X5": "tables",
    "TABLE_BUDGET_ALLOCATION": "tables",
    "BUDGET_ALLOCATION": "tables",
    "TABLE_VENDOR_EVALUATION": "tables",
    "VENDOR_EVALUATION": "tables",
    "TABLE_OKRS_TRACKER": "tables",
    "OKRS_TRACKER": "tables",
    "TABLE_EMPLOYEE_SKILLS_MATRIX": "tables",
    "EMPLOYEE_SKILLS_MATRIX": "tables",
    "TABLE_PRODUCT_SPECS": "tables",
    "PRODUCT_SPECS": "tables",
    "TABLE_SLA_TIERS": "tables",
    "SLA_TIERS": "tables",

    # -------------------------------------------------------------
    # MODULE 2: STRATEGIC FRAMEWORKS (35 Archetypes + Aliases)
    # -------------------------------------------------------------
    "FRAMEWORK_MATRIX_2X2": "frameworks",
    "MATRIX_2X2": "frameworks",
    "2X2_MATRIX": "frameworks",
    "FRAMEWORK_MATRIX_3X3": "frameworks",
    "MATRIX_3X3": "frameworks",
    "GE_MCKINSEY_9BOX": "frameworks",
    "FRAMEWORK_PORTER_5_FORCES": "frameworks",
    "PORTER_5_FORCES": "frameworks",
    "FIVE_FORCES": "frameworks",
    "FRAMEWORK_VALUE_CHAIN": "frameworks",
    "VALUE_CHAIN": "frameworks",
    "FRAMEWORK_SWOT_ANALYSIS": "frameworks",
    "SWOT_ANALYSIS": "frameworks",
    "SWOT": "frameworks",
    "FRAMEWORK_PESTEL_HEX": "frameworks",
    "PESTEL_HEX": "frameworks",
    "PESTEL": "frameworks",
    "FRAMEWORK_BALANCED_SCORECARD": "frameworks",
    "BALANCED_SCORECARD": "frameworks",
    "BSC": "frameworks",
    "FRAMEWORK_STRATEGY_HOUSE": "frameworks",
    "STRATEGY_HOUSE": "frameworks",
    "HOUSE": "frameworks",
    "TEMPLE": "frameworks",
    "FRAMEWORK_PYRAMID_ASCENDING": "frameworks",
    "FRAMEWORK_PYRAMID": "frameworks",
    "PYRAMID": "frameworks",
    "PYRAMID_ASCENDING": "frameworks",
    "FRAMEWORK_INVERTED_PYRAMID": "frameworks",
    "INVERTED_PYRAMID": "frameworks",
    "FRAMEWORK_CONVERSION_FUNNEL": "frameworks",
    "FRAMEWORK_FUNNEL": "frameworks",
    "FUNNEL": "frameworks",
    "CONVERSION_FUNNEL": "frameworks",
    "FRAMEWORK_GROWTH_FLYWHEEL": "frameworks",
    "FRAMEWORK_FLYWHEEL": "frameworks",
    "FLYWHEEL": "frameworks",
    "GROWTH_FLYWHEEL": "frameworks",
    "FRAMEWORK_HUB_SPOKE": "frameworks",
    "HUB_SPOKE": "frameworks",
    "HUB_AND_SPOKE": "frameworks",
    "FRAMEWORK_CONCENTRIC_RINGS": "frameworks",
    "CONCENTRIC_RINGS": "frameworks",
    "FRAMEWORK_VENN_2_SET": "frameworks",
    "FRAMEWORK_VENN": "frameworks",
    "VENN": "frameworks",
    "VENN_DIAGRAM": "frameworks",
    "FRAMEWORK_VENN_3_SET": "frameworks",
    "VENN_3_SET": "frameworks",
    "FRAMEWORK_DIAMOND_MODEL": "frameworks",
    "DIAMOND_MODEL": "frameworks",
    "PORTER_DIAMOND": "frameworks",
    "FRAMEWORK_ANSOFF_MATRIX": "frameworks",
    "ANSOFF_MATRIX": "frameworks",
    "ANSOFF": "frameworks",
    "FRAMEWORK_MCKINSEY_7S": "frameworks",
    "MCKINSEY_7S": "frameworks",
    "7S_MODEL": "frameworks",
    "FRAMEWORK_STRATEGY_CLOCK": "frameworks",
    "STRATEGY_CLOCK": "frameworks",
    "BOWMAN_CLOCK": "frameworks",
    "FRAMEWORK_CMMI_STAIRS": "frameworks",
    "CMMI_STAIRS": "frameworks",
    "MATURITY_LADDER": "frameworks",
    "FRAMEWORK_VRIO_MATRIX": "frameworks",
    "VRIO_MATRIX": "frameworks",
    "VRIO": "frameworks",
    "FRAMEWORK_GOLDEN_CIRCLE": "frameworks",
    "GOLDEN_CIRCLE": "frameworks",
    "SIMON_SINEK_CIRCLE": "frameworks",
    "FRAMEWORK_ICEBERG_MODEL": "frameworks",
    "ICEBERG_MODEL": "frameworks",
    "ICEBERG": "frameworks",
    "FRAMEWORK_DOUBLE_DIAMOND": "frameworks",
    "DOUBLE_DIAMOND": "frameworks",
    "DESIGN_THINKING_DIAMOND": "frameworks",
    "FRAMEWORK_ROADMAP_GANTT": "frameworks",
    "ROADMAP_GANTT": "frameworks",
    "HORIZONS": "frameworks",
    "FRAMEWORK_SWIMLANE": "frameworks",
    "SWIMLANE": "frameworks",
    "FRAMEWORK_STEEPLE": "frameworks",
    "STEEPLE": "frameworks",
    "FRAMEWORK_KANO_MODEL": "frameworks",
    "KANO_MODEL": "frameworks",
    "FRAMEWORK_LEAN_CANVAS": "frameworks",
    "LEAN_CANVAS": "frameworks",
    "FRAMEWORK_VALUE_PROPOSITION_CANVAS": "frameworks",
    "VALUE_PROPOSITION_CANVAS": "frameworks",
    "FRAMEWORK_CYNEFIN": "frameworks",
    "CYNEFIN": "frameworks",
    "FRAMEWORK_BOW_TIE": "frameworks",
    "BOW_TIE": "frameworks",
    "FRAMEWORK_BLUE_OCEAN_ERRC": "frameworks",
    "BLUE_OCEAN_ERRC": "frameworks",
    "ERRC_GRID": "frameworks",
    "FRAMEWORK_NORTH_STAR_METRIC": "frameworks",
    "NORTH_STAR_METRIC": "frameworks",
    "FRAMEWORK_GROW_COACHING": "frameworks",
    "GROW_COACHING": "frameworks",
    "FRAMEWORK_PIRATE_AARRR": "frameworks",
    "PIRATE_AARRR": "frameworks",
    "AARRR_FUNNEL": "frameworks",

    # -------------------------------------------------------------
    # MODULE 3: PROCESSES & MECHANISMS (30 Archetypes + Aliases)
    # -------------------------------------------------------------
    "PROCESS_CHEVRON_LINEAR": "processes",
    "CHEVRON_LINEAR": "processes",
    "PROCESS_CHEVRON": "processes",
    "CHEVRON_FLOW": "processes",
    "PROCESS_CURVED_PIPELINE": "processes",
    "CURVED_PIPELINE": "processes",
    "S_CURVE_PIPELINE": "processes",
    "PROCESS_CIRCULAR_CYCLE": "processes",
    "CIRCULAR_CYCLE": "processes",
    "PDCA_CYCLE": "processes",
    "PROCESS_INTERLOCKING_GEARS": "processes",
    "INTERLOCKING_GEARS": "processes",
    "GEARS_MECHANISM": "processes",
    "PROCESS_FISHBONE_ISHIKAWA": "processes",
    "FISHBONE_ISHIKAWA": "processes",
    "ISHIKAWA_DIAGRAM": "processes",
    "CAUSE_AND_EFFECT": "processes",
    "PROCESS_DECISION_FLOW": "processes",
    "DECISION_FLOW": "processes",
    "DECISION_TREE": "processes",
    "PROCESS_SWIMLANE_TRACKS": "processes",
    "SWIMLANE_TRACKS": "processes",
    "PROCESS_ASCENDING_STAIRS": "processes",
    "ASCENDING_STAIRS": "processes",
    "STAIRCASE_PROGRESSION": "processes",
    "PROCESS_TIMELINE_FLAG_RIBBON": "processes",
    "TIMELINE_FLAG_RIBBON": "processes",
    "FLAG_RIBBON": "processes",
    "PROCESS_VERTICAL_SPINE": "processes",
    "VERTICAL_SPINE": "processes",
    "VERTICAL_TIMELINE": "processes",
    "PROCESS_GANTT_ROADMAP": "processes",
    "GANTT_ROADMAP": "processes",
    "PROJECT_GANTT": "processes",
    "PROCESS_3_HORIZONS_ROADMAP": "processes",
    "THREE_HORIZONS": "processes",
    "MCKINSEY_3_HORIZONS": "processes",
    "PROCESS_AGILE_SCRUM_CYCLE": "processes",
    "AGILE_SCRUM_CYCLE": "processes",
    "SCRUM_SPRINT": "processes",
    "PROCESS_BRIDGE_MIGRATION": "processes",
    "BRIDGE_MIGRATION": "processes",
    "AS_IS_TO_BE_BRIDGE": "processes",
    "PROCESS_JIGSAW_PUZZLE": "processes",
    "JIGSAW_PUZZLE": "processes",
    "PUZZLE_PIECES": "processes",
    "PROCESS_HONEYCOMB_CHAIN": "processes",
    "HONEYCOMB_CHAIN": "processes",
    "HEXAGON_FLOW": "processes",
    "PROCESS_ETL_DATA_PIPELINE": "processes",
    "ETL_DATA_PIPELINE": "processes",
    "DATA_PIPELINE_FLOW": "processes",
    "PROCESS_LEVEL_UP_LADDER": "processes",
    "LEVEL_UP_LADDER": "processes",
    "COMPETENCY_LADDER": "processes",
    "PROCESS_DOMINO_CASCADE": "processes",
    "DOMINO_CASCADE": "processes",
    "CHAIN_REACTION": "processes",
    "PROCESS_RADIAL_PROGRESSION": "processes",
    "RADIAL_PROGRESSION": "processes",
    "PROCESS_CIRCULAR_LOOP_6STEP": "processes",
    "CIRCULAR_LOOP_6STEP": "processes",
    "PROCESS_SPIRAL_GROWTH": "processes",
    "SPIRAL_GROWTH": "processes",
    "PROCESS_HOURGLASS_WORKFLOW": "processes",
    "HOURGLASS_WORKFLOW": "processes",
    "PROCESS_PARALLEL_STREAMS": "processes",
    "PARALLEL_STREAMS": "processes",
    "PROCESS_STAGED_GATE_PHASES": "processes",
    "STAGED_GATE_PHASES": "processes",
    "STAGE_GATE": "processes",
    "PROCESS_SERPENTINE_ROADMAP": "processes",
    "SERPENTINE_ROADMAP": "processes",
    "S_ROADMAP": "processes",
    "PROCESS_PIPELINE_FILTRATION": "processes",
    "PIPELINE_FILTRATION": "processes",
    "PROCESS_CONTINUOUS_IMPROVEMENT_PDCA": "processes",
    "CONTINUOUS_IMPROVEMENT_PDCA": "processes",
    "PDCA_IMPROVEMENT": "processes",
    "PROCESS_DEVSECOPS_INFINITY_LOOP": "processes",
    "DEVSECOPS_INFINITY_LOOP": "processes",
    "DEVSECOPS_LOOP": "processes",
    "PROCESS_CRITICAL_PATH_CPM": "processes",
    "CRITICAL_PATH_CPM": "processes",
    "PERT_CPM": "processes",

    # -------------------------------------------------------------
    # MODULE 4: SYSTEM & ARCHITECTURES (25 Archetypes + Aliases)
    # -------------------------------------------------------------
    "ARCH_SYSTEM_LAYERED_STACK": "architectures",
    "SYSTEM_LAYERED_STACK": "architectures",
    "LAYERED_ARCHITECTURE": "architectures",
    "ARCH_ORG_HIERARCHY_TREE": "architectures",
    "ORG_HIERARCHY_TREE": "architectures",
    "ORGANIZATION_CHART": "architectures",
    "ARCH_RADIAL_MIND_MAP": "architectures",
    "RADIAL_MIND_MAP": "architectures",
    "MIND_MAP": "architectures",
    "ARCH_MICROSERVICES_MESH": "architectures",
    "MICROSERVICES_MESH": "architectures",
    "SERVICE_MESH": "architectures",
    "ARCH_DEFENSE_IN_DEPTH": "architectures",
    "DEFENSE_IN_DEPTH": "architectures",
    "SECURITY_SHIELD_LAYERS": "architectures",
    "ARCH_CLOUD_HYBRID_INFRA": "architectures",
    "CLOUD_HYBRID_INFRA": "architectures",
    "HYBRID_CLOUD": "architectures",
    "ARCH_BUS_BAR_MODULAR": "architectures",
    "BUS_BAR_MODULAR": "architectures",
    "EVENT_BUS_ARCHITECTURE": "architectures",
    "ARCH_HEXAGONAL_PORTS": "architectures",
    "HEXAGONAL_PORTS": "architectures",
    "PORTS_AND_ADAPTERS": "architectures",
    "ARCH_ECOSYSTEM_NETWORK": "architectures",
    "ECOSYSTEM_NETWORK": "architectures",
    "VALUE_NETWORK": "architectures",
    "ARCH_MATRIX_ORGANIZATION": "architectures",
    "MATRIX_ORGANIZATION": "architectures",
    "MATRIX_ORG": "architectures",
    "ARCH_API_GATEWAY_HUB": "architectures",
    "API_GATEWAY_HUB": "architectures",
    "GATEWAY_HUB": "architectures",
    "ARCH_DATA_GOVERNANCE_MESH": "architectures",
    "DATA_GOVERNANCE_MESH": "architectures",
    "DATA_MESH": "architectures",
    "ARCH_CLEAN_ONION_STACK": "architectures",
    "CLEAN_ONION_STACK": "architectures",
    "ONION_ARCHITECTURE": "architectures",
    "ARCH_CONTAINER_CLUSTER_K8S": "architectures",
    "CONTAINER_CLUSTER_K8S": "architectures",
    "K8S_CLUSTER": "architectures",
    "ARCH_AI_AGENT_ORCHESTRATOR": "architectures",
    "AI_AGENT_ORCHESTRATOR": "architectures",
    "AGENT_ORCHESTRATION": "architectures",
    "ARCH_EVENT_DRIVEN_KAFKA": "architectures",
    "EVENT_DRIVEN_KAFKA": "architectures",
    "KAFKA_STREAMING": "architectures",
    "ARCH_SERVERLESS_EVENT_FLOW": "architectures",
    "SERVERLESS_EVENT_FLOW": "architectures",
    "SERVERLESS_ARCHITECTURE": "architectures",
    "ARCH_ZERO_TRUST_SECURITY": "architectures",
    "ZERO_TRUST_SECURITY": "architectures",
    "ZERO_TRUST": "architectures",
    "ARCH_DATA_LAKEHOUSE_MEDALLION": "architectures",
    "DATA_LAKEHOUSE_MEDALLION": "architectures",
    "MEDALLION_LAKEHOUSE": "architectures",
    "ARCH_CI_CD_AUTOMATION": "architectures",
    "CI_CD_AUTOMATION": "architectures",
    "CI_CD_PIPELINE": "architectures",
    "ARCH_HUB_SPOKE_ENTERPRISE_NETWORK": "architectures",
    "HUB_SPOKE_ENTERPRISE_NETWORK": "architectures",
    "ENTERPRISE_HUB_SPOKE": "architectures",
    "ARCH_MULTI_TENANT_SAAS": "architectures",
    "MULTI_TENANT_SAAS": "architectures",
    "SAAS_MULTI_TENANT": "architectures",
    "ARCH_RAG_LLM_PIPELINE": "architectures",
    "RAG_LLM_PIPELINE": "architectures",
    "RAG_PIPELINE": "architectures",
    "ARCH_EDGE_TO_CLOUD_IOT": "architectures",
    "EDGE_TO_CLOUD_IOT": "architectures",
    "IOT_EDGE_TO_CLOUD": "architectures",
    "ARCH_MODULAR_MONOLITH": "architectures",
    "MODULAR_MONOLITH": "architectures",

    # -------------------------------------------------------------
    # MODULE 5: NATIVE OFFICE CHARTS (20 Archetypes + Aliases)
    # -------------------------------------------------------------
    "CHART_COLUMN_CLUSTERED": "charts",
    "COLUMN_CLUSTERED": "charts",
    "CHART_COLUMN_STACKED": "charts",
    "COLUMN_STACKED": "charts",
    "CHART_COLUMN_100_STACKED": "charts",
    "COLUMN_100_STACKED": "charts",
    "CHART_BAR_CLUSTERED": "charts",
    "BAR_CLUSTERED": "charts",
    "CHART_BAR_DIVERGING": "charts",
    "BAR_DIVERGING": "charts",
    "CHART_BAR_DIVERGING_PYRAMID": "charts",
    "POPULATION_PYRAMID_NATIVE": "charts",
    "CHART_LINE_TREND": "charts",
    "LINE_TREND": "charts",
    "CHART_LINE_WITH_MARKERS": "charts",
    "CHART_AREA_STANDARD": "charts",
    "AREA_STANDARD": "charts",
    "CHART_AREA_STACKED": "charts",
    "AREA_STACKED": "charts",
    "CHART_DONUT_KPI": "charts",
    "DONUT_KPI": "charts",
    "CHART_DONUT_KPI_CENTER": "charts",
    "CHART_PIE_HIGHLIGHT_SLICE": "charts",
    "PIE_HIGHLIGHT_SLICE": "charts",
    "PIE_EXPLODED": "charts",
    "CHART_WATERFALL": "charts",
    "WATERFALL": "charts",
    "CHART_WATERFALL_BRIDGE": "charts",
    "CHART_COMBO_DUAL_AXIS": "charts",
    "COMBO_DUAL_AXIS": "charts",
    "CHART_RADAR": "charts",
    "RADAR": "charts",
    "CHART_RADAR_CAPABILITY": "charts",
    "CHART_SCATTER_CORRELATION": "charts",
    "SCATTER_CORRELATION": "charts",
    "CHART_BUBBLE_MATRIX": "charts",
    "BUBBLE_MATRIX": "charts",
    "CHART_BAR_STACKED_100": "charts",
    "BAR_STACKED_100": "charts",
    "CHART_PARETO_ANALYSIS": "charts",
    "PARETO_ANALYSIS": "charts",
    "PARETO_CHART": "charts",
    "CHART_STEPPED_LINE": "charts",
    "STEPPED_LINE": "charts",
    "CHART_RADAR_FILLED": "charts",
    "RADAR_FILLED": "charts",
    "CHART_HISTOGRAM_DISTRIBUTION": "charts",
    "HISTOGRAM_DISTRIBUTION": "charts",
    "HISTOGRAM": "charts",

    # -------------------------------------------------------------
    # MODULE 6: KEYNOTE CONTAINERS & ACCENTS (30 Archetypes + Aliases)
    # -------------------------------------------------------------
    "CONTAINER_BENTO_COMPLEX": "containers",
    "BENTO_COMPLEX": "containers",
    "CONTAINER_BENTO_COMPLEX_4": "containers",
    "CONTAINER_BENTO_GRID_3X3": "containers",
    "BENTO_GRID_3X3": "containers",
    "CONTAINER_KPI_STAT_DELTA": "containers",
    "KPI_STAT_DELTA": "containers",
    "CONTAINER_BEFORE_AFTER": "containers",
    "BEFORE_AFTER": "containers",
    "CONTRAST_SPLIT": "containers",
    "CONTAINER_BEFORE_AFTER_SPLIT": "containers",
    "CONTAINER_EXECUTIVE_QUOTE": "containers",
    "EXECUTIVE_QUOTE": "containers",
    "QUOTE_BANNER": "containers",
    "CONTAINER_TIMELINE_FLOW": "containers",
    "TIMELINE_FLOW": "containers",
    "CONTAINER_PILLAR_3D": "containers",
    "PILLAR_3D": "containers",
    "THREE_PILLARS": "containers",
    "CONTAINER_PILLAR_3_COLUMNS": "containers",
    "CONTAINER_PILLAR_4_COLUMNS": "containers",
    "PILLAR_4_COLUMNS": "containers",
    "FOUR_PILLARS": "containers",
    "CONTAINER_PROBLEM_SOL_3STEP": "containers",
    "PROBLEM_SOL_3STEP": "containers",
    "PROBLEM_SOLUTION_STEP": "containers",
    "CONTAINER_TARGET_BULLSEYE": "containers",
    "TARGET_BULLSEYE": "containers",
    "BULLSEYE": "containers",
    "CONTAINER_BALANCE_SEESAW": "containers",
    "BALANCE_SEESAW": "containers",
    "SEESAW": "containers",
    "CONTAINER_GAUGE_METER_DIAL": "containers",
    "GAUGE_METER_DIAL": "containers",
    "SPEEDOMETER": "containers",
    "CONTAINER_GLASSMORPHIC_HERO": "containers",
    "GLASSMORPHIC_HERO": "containers",
    "CONTAINER_HERO_SPLIT_CARDS": "containers",
    "HERO_SPLIT_CARDS": "containers",
    "CONTAINER_DIAGONAL_SPLIT": "containers",
    "DIAGONAL_SPLIT": "containers",
    "CONTAINER_NOTIFICATION_TAGS": "containers",
    "NOTIFICATION_TAGS": "containers",
    "CONTAINER_CUSTOMER_JOURNEY": "containers",
    "CUSTOMER_JOURNEY": "containers",
    "CONTAINER_ISOMETRIC_STACK": "containers",
    "ISOMETRIC_STACK": "containers",
    "CONTAINER_TABBED_OVERVIEW": "containers",
    "TABBED_OVERVIEW": "containers",
    "CONTAINER_EXECUTIVE_DASHBOARD": "containers",
    "EXECUTIVE_DASHBOARD": "containers",
    "CONTAINER_CLOSING_CTA_HERO": "containers",
    "CLOSING_CTA_HERO": "containers",
    "CLOSING_CTA": "containers",
    "CONTAINER_DEVICE_MOCKUP_FRAME": "containers",
    "DEVICE_MOCKUP_FRAME": "containers",
    "MOCKUP_FRAME": "containers",
    "CONTAINER_METRIC_MARQUEE_BANNER": "containers",
    "METRIC_MARQUEE_BANNER": "containers",
    "MARQUEE_BANNER": "containers",
    "CONTAINER_THREE_PILLARS_CARDS": "containers",
    "THREE_PILLARS_CARDS": "containers",
    "CONTAINER_PROBLEM_SOLUTION_IMPACT": "containers",
    "PROBLEM_SOLUTION_IMPACT": "containers",
    "PROBLEM_SOL_IMPACT": "containers",
    "CONTAINER_FEATURE_HEX_CLUSTER": "containers",
    "FEATURE_HEX_CLUSTER": "containers",
    "HEX_CLUSTER": "containers",
    "CONTAINER_TESTIMONIAL_CAROUSEL_ROW": "containers",
    "TESTIMONIAL_CAROUSEL_ROW": "containers",
    "TESTIMONIALS_ROW": "containers",
    "CONTAINER_STAT_HERO_SPLIT_60_40": "containers",
    "STAT_HERO_SPLIT_60_40": "containers",
    "STAT_SPLIT_60_40": "containers",
    "CONTAINER_MINIMALIST_APPLE_QUOTE": "containers",
    "MINIMALIST_APPLE_QUOTE": "containers",
    "APPLE_QUOTE": "containers"
}


class MasterComponentDispatcher:
    """
    Central router that coordinates all 110+ presentation archetypes,
    managing Native Tables, Vector Frameworks, Processes, Architectures,
    Office Charts, and Keynote Containers.
    """
    def __init__(self, theme: str = "DARK", tokens: Optional[Dict[str, Any]] = None):
        self.theme = theme.upper()
        self.tokens = tokens or {}
        self.tables = NativeTablesEngine(theme=self.theme, tokens=self.tokens)
        self.frameworks = StrategicFrameworksEngine(theme=self.theme, tokens=self.tokens)
        self.processes = ProcessesEngine(theme=self.theme, tokens=self.tokens)
        self.architectures = ArchitecturesEngine(theme=self.theme, tokens=self.tokens)
        self.charts = NativeChartsEngine(theme=self.theme, tokens=self.tokens)
        self.containers = AdvancedContainersEngine(theme=self.theme, tokens=self.tokens)

    def can_handle(self, visual_job: str) -> bool:
        vj_clean = str(visual_job).upper().strip()
        return vj_clean in ARCHETYPES_REGISTRY

    def render(self, slide: Any, spec: Dict[str, Any], visual_job: str, left: float, top: float, width: float, height: float) -> Optional[List[Any]]:
        vj = str(visual_job).upper().strip()

        # ----------------- 1. NATIVE TABLES (15) -----------------
        if vj in {"TABLE_COMPARISON_PRO", "TABLE_COMPARISON", "COMPARISON_TABLE"}:
            res = self.tables.render_comparison_table(slide, spec, left, top, width, height)
            return [res] if res else []
        elif vj in {"TABLE_SCORECARD_HEATMAP", "TABLE_SCORECARD", "SCORECARD"}:
            res = self.tables.render_scorecard_table(slide, spec, left, top, width, height)
            return [res] if res else []
        elif vj in {"TABLE_FINANCIAL_PL", "TABLE_FINANCIAL", "FINANCIAL_TABLE"}:
            res = self.tables.render_financial_table(slide, spec, left, top, width, height)
            return [res] if res else []
        elif vj in {"TABLE_RACI_GOVERNANCE", "TABLE_RACI", "RACI_MATRIX"}:
            res = self.tables.render_raci_table(slide, spec, left, top, width, height)
            return [res] if res else []
        elif vj in {"TABLE_METRIC_MATRIX", "DATA_TABLE", "TABLE", "TABLE_MATRIX"}:
            res = self.tables.render_metric_matrix_table(slide, spec, left, top, width, height)
            return [res] if res else []
        elif vj in {"TABLE_COMPETITOR_BENCHMARK", "COMPETITOR_BENCHMARK"}:
            res = self.tables.render_competitor_benchmark(slide, spec, left, top, width, height)
            return [res] if res else []
        elif vj in {"TABLE_CAPABILITY_GAP", "CAPABILITY_GAP"}:
            res = self.tables.render_capability_gap(slide, spec, left, top, width, height)
            return [res] if res else []
        elif vj in {"TABLE_PRICING_TIERS", "PRICING_TIERS"}:
            res = self.tables.render_pricing_tiers(slide, spec, left, top, width, height)
            return [res] if res else []
        elif vj in {"TABLE_RISK_REGISTER", "RISK_REGISTER"}:
            res = self.tables.render_risk_register(slide, spec, left, top, width, height)
            return [res] if res else []
        elif vj in {"TABLE_AUDIT_COMPLIANCE", "AUDIT_COMPLIANCE"}:
            res = self.tables.render_audit_compliance(slide, spec, left, top, width, height)
            return [res] if res else []
        elif vj in {"TABLE_PROS_CONS", "PROS_CONS_TABLE"}:
            res = self.tables.render_pros_cons(slide, spec, left, top, width, height)
            return [res] if res else []
        elif vj in {"TABLE_ROADMAP_SCHEDULE", "ROADMAP_SCHEDULE"}:
            res = self.tables.render_roadmap_schedule(slide, spec, left, top, width, height)
            return [res] if res else []
        elif vj in {"TABLE_SALES_TERRITORY", "SALES_TERRITORY"}:
            res = self.tables.render_sales_territory(slide, spec, left, top, width, height)
            return [res] if res else []
        elif vj in {"TABLE_WEIGHTED_DECISION", "WEIGHTED_DECISION"}:
            res = self.tables.render_weighted_decision(slide, spec, left, top, width, height)
            return [res] if res else []
        elif vj in {"TABLE_EXECUTIVE_SUMMARY", "EXECUTIVE_SUMMARY_TABLE"}:
            res = self.tables.render_executive_summary_table(slide, spec, left, top, width, height)
            return [res] if res else []
        elif vj in {"TABLE_PRICING_FEATURE_MATRIX", "PRICING_FEATURE_MATRIX"}:
            res = self.tables.render_pricing_feature_matrix(slide, spec, left, top, width, height)
            return [res] if res else []
        elif vj in {"TABLE_MILESTONE_DELIVERABLES", "MILESTONE_DELIVERABLES"}:
            res = self.tables.render_milestone_deliverables(slide, spec, left, top, width, height)
            return [res] if res else []
        elif vj in {"TABLE_SWOT_DETAILED", "SWOT_DETAILED_TABLE"}:
            res = self.tables.render_swot_detailed_table(slide, spec, left, top, width, height)
            return [res] if res else []
        elif vj in {"TABLE_RISK_HEATMAP_5X5", "RISK_HEATMAP_5X5"}:
            res = self.tables.render_risk_heatmap_5x5(slide, spec, left, top, width, height)
            return [res] if res else []
        elif vj in {"TABLE_BUDGET_ALLOCATION", "BUDGET_ALLOCATION"}:
            res = self.tables.render_budget_allocation(slide, spec, left, top, width, height)
            return [res] if res else []
        elif vj in {"TABLE_VENDOR_EVALUATION", "VENDOR_EVALUATION"}:
            res = self.tables.render_vendor_evaluation(slide, spec, left, top, width, height)
            return [res] if res else []
        elif vj in {"TABLE_OKRS_TRACKER", "OKRS_TRACKER"}:
            res = self.tables.render_okrs_tracker(slide, spec, left, top, width, height)
            return [res] if res else []
        elif vj in {"TABLE_EMPLOYEE_SKILLS_MATRIX", "EMPLOYEE_SKILLS_MATRIX"}:
            res = self.tables.render_skills_matrix(slide, spec, left, top, width, height)
            return [res] if res else []
        elif vj in {"TABLE_PRODUCT_SPECS", "PRODUCT_SPECS"}:
            res = self.tables.render_product_specs(slide, spec, left, top, width, height)
            return [res] if res else []
        elif vj in {"TABLE_SLA_TIERS", "SLA_TIERS"}:
            res = self.tables.render_sla_tiers(slide, spec, left, top, width, height)
            return [res] if res else []

        # ----------------- 2. STRATEGIC FRAMEWORKS (35) -----------------
        elif vj in {"FRAMEWORK_MATRIX_2X2", "MATRIX_2X2", "2X2_MATRIX"}:
            return self.frameworks.render_matrix_2x2(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_MATRIX_3X3", "MATRIX_3X3", "GE_MCKINSEY_9BOX"}:
            return self.frameworks.render_matrix_3x3(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_PORTER_5_FORCES", "PORTER_5_FORCES", "FIVE_FORCES"}:
            return self.frameworks.render_porter_5_forces(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_VALUE_CHAIN", "VALUE_CHAIN"}:
            return self.frameworks.render_value_chain(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_SWOT_ANALYSIS", "SWOT_ANALYSIS", "SWOT"}:
            return self.frameworks.render_swot_analysis(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_PESTEL_HEX", "PESTEL_HEX", "PESTEL"}:
            return self.frameworks.render_pestel_hex(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_BALANCED_SCORECARD", "BALANCED_SCORECARD", "BSC"}:
            return self.frameworks.render_balanced_scorecard(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_STRATEGY_HOUSE", "STRATEGY_HOUSE", "HOUSE", "TEMPLE"}:
            return self.frameworks.render_strategy_house(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_PYRAMID_ASCENDING", "FRAMEWORK_PYRAMID", "PYRAMID", "PYRAMID_ASCENDING"}:
            return self.frameworks.render_pyramid_ascending(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_INVERTED_PYRAMID", "INVERTED_PYRAMID"}:
            return self.frameworks.render_inverted_pyramid(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_CONVERSION_FUNNEL", "FRAMEWORK_FUNNEL", "FUNNEL", "CONVERSION_FUNNEL"}:
            return self.frameworks.render_conversion_funnel(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_GROWTH_FLYWHEEL", "FRAMEWORK_FLYWHEEL", "FLYWHEEL", "GROWTH_FLYWHEEL"}:
            return self.frameworks.render_growth_flywheel(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_HUB_SPOKE", "HUB_SPOKE", "HUB_AND_SPOKE"}:
            return self.frameworks.render_hub_spoke(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_CONCENTRIC_RINGS", "CONCENTRIC_RINGS"}:
            return self.frameworks.render_concentric_rings(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_VENN_2_SET", "FRAMEWORK_VENN", "VENN", "VENN_DIAGRAM"}:
            return self.frameworks.render_venn_2_set(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_VENN_3_SET", "VENN_3_SET"}:
            return self.frameworks.render_venn_3_set(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_DIAMOND_MODEL", "DIAMOND_MODEL", "PORTER_DIAMOND"}:
            return self.frameworks.render_diamond_model(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_ANSOFF_MATRIX", "ANSOFF_MATRIX", "ANSOFF"}:
            return self.frameworks.render_ansoff_matrix(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_MCKINSEY_7S", "MCKINSEY_7S", "7S_MODEL"}:
            return self.frameworks.render_mckinsey_7s(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_STRATEGY_CLOCK", "STRATEGY_CLOCK", "BOWMAN_CLOCK"}:
            return self.frameworks.render_strategy_clock(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_CMMI_STAIRS", "CMMI_STAIRS", "MATURITY_LADDER"}:
            return self.frameworks.render_cmmi_stairs(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_VRIO_MATRIX", "VRIO_MATRIX", "VRIO"}:
            return self.frameworks.render_vrio_matrix(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_GOLDEN_CIRCLE", "GOLDEN_CIRCLE", "SIMON_SINEK_CIRCLE"}:
            return self.frameworks.render_golden_circle(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_ICEBERG_MODEL", "ICEBERG_MODEL", "ICEBERG"}:
            return self.frameworks.render_iceberg_model(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_DOUBLE_DIAMOND", "DOUBLE_DIAMOND", "DESIGN_THINKING_DIAMOND"}:
            return self.frameworks.render_double_diamond(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_STEEPLE", "STEEPLE"}:
            return self.frameworks.render_steeple(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_KANO_MODEL", "KANO_MODEL"}:
            return self.frameworks.render_kano_model(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_LEAN_CANVAS", "LEAN_CANVAS"}:
            return self.frameworks.render_lean_canvas(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_VALUE_PROPOSITION_CANVAS", "VALUE_PROPOSITION_CANVAS"}:
            return self.frameworks.render_value_proposition_canvas(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_CYNEFIN", "CYNEFIN"}:
            return self.frameworks.render_cynefin(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_BOW_TIE", "BOW_TIE"}:
            return self.frameworks.render_bow_tie(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_BLUE_OCEAN_ERRC", "BLUE_OCEAN_ERRC", "ERRC_GRID"}:
            return self.frameworks.render_blue_ocean_errc(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_NORTH_STAR_METRIC", "NORTH_STAR_METRIC"}:
            return self.frameworks.render_north_star_metric(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_GROW_COACHING", "GROW_COACHING"}:
            return self.frameworks.render_grow_coaching(slide, spec, left, top, width, height)
        elif vj in {"FRAMEWORK_PIRATE_AARRR", "PIRATE_AARRR", "AARRR_FUNNEL"}:
            return self.frameworks.render_pirate_aarrr(slide, spec, left, top, width, height)

        # ----------------- 3. PROCESSES & MECHANISMS (30) -----------------
        elif vj in {"PROCESS_CHEVRON_LINEAR", "CHEVRON_LINEAR", "PROCESS_CHEVRON", "CHEVRON_FLOW"}:
            return self.processes.render_chevron_linear(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_CURVED_PIPELINE", "CURVED_PIPELINE", "S_CURVE_PIPELINE"}:
            return self.processes.render_curved_pipeline(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_CIRCULAR_CYCLE", "CIRCULAR_CYCLE", "PDCA_CYCLE"}:
            return self.processes.render_circular_cycle(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_INTERLOCKING_GEARS", "INTERLOCKING_GEARS", "GEARS_MECHANISM"}:
            return self.processes.render_interlocking_gears(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_FISHBONE_ISHIKAWA", "FISHBONE_ISHIKAWA", "ISHIKAWA_DIAGRAM", "CAUSE_AND_EFFECT"}:
            return self.processes.render_fishbone_ishikawa(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_DECISION_FLOW", "DECISION_FLOW", "DECISION_TREE"}:
            return self.processes.render_decision_flow(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_SWIMLANE_TRACKS", "SWIMLANE_TRACKS", "FRAMEWORK_SWIMLANE", "SWIMLANE"}:
            return self.processes.render_swimlane_tracks(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_ASCENDING_STAIRS", "ASCENDING_STAIRS", "STAIRCASE_PROGRESSION"}:
            return self.processes.render_ascending_stairs(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_TIMELINE_FLAG_RIBBON", "TIMELINE_FLAG_RIBBON", "FLAG_RIBBON"}:
            return self.processes.render_timeline_flag_ribbon(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_VERTICAL_SPINE", "VERTICAL_SPINE", "VERTICAL_TIMELINE"}:
            return self.processes.render_vertical_spine(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_GANTT_ROADMAP", "GANTT_ROADMAP", "PROJECT_GANTT", "FRAMEWORK_ROADMAP_GANTT", "ROADMAP_GANTT"}:
            return self.processes.render_gantt_roadmap(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_3_HORIZONS_ROADMAP", "THREE_HORIZONS", "MCKINSEY_3_HORIZONS", "HORIZONS"}:
            return self.processes.render_3_horizons_roadmap(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_AGILE_SCRUM_CYCLE", "AGILE_SCRUM_CYCLE", "SCRUM_SPRINT"}:
            return self.processes.render_agile_scrum_cycle(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_BRIDGE_MIGRATION", "BRIDGE_MIGRATION", "AS_IS_TO_BE_BRIDGE"}:
            return self.processes.render_bridge_migration(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_JIGSAW_PUZZLE", "JIGSAW_PUZZLE", "PUZZLE_PIECES"}:
            return self.processes.render_jigsaw_puzzle(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_HONEYCOMB_CHAIN", "HONEYCOMB_CHAIN", "HEXAGON_FLOW"}:
            return self.processes.render_honeycomb_chain(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_ETL_DATA_PIPELINE", "ETL_DATA_PIPELINE", "DATA_PIPELINE_FLOW"}:
            return self.processes.render_etl_data_pipeline(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_LEVEL_UP_LADDER", "LEVEL_UP_LADDER", "COMPETENCY_LADDER"}:
            return self.processes.render_level_up_ladder(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_DOMINO_CASCADE", "DOMINO_CASCADE", "CHAIN_REACTION"}:
            return self.processes.render_domino_cascade(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_RADIAL_PROGRESSION", "RADIAL_PROGRESSION"}:
            return self.processes.render_radial_progression(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_CIRCULAR_LOOP_6STEP", "CIRCULAR_LOOP_6STEP"}:
            return self.processes.render_circular_loop_6step(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_SPIRAL_GROWTH", "SPIRAL_GROWTH"}:
            return self.processes.render_spiral_growth(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_HOURGLASS_WORKFLOW", "HOURGLASS_WORKFLOW"}:
            return self.processes.render_hourglass_workflow(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_PARALLEL_STREAMS", "PARALLEL_STREAMS"}:
            return self.processes.render_parallel_streams(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_STAGED_GATE_PHASES", "STAGED_GATE_PHASES", "STAGE_GATE"}:
            return self.processes.render_staged_gate_phases(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_SERPENTINE_ROADMAP", "SERPENTINE_ROADMAP", "S_ROADMAP"}:
            return self.processes.render_serpentine_roadmap(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_PIPELINE_FILTRATION", "PIPELINE_FILTRATION"}:
            return self.processes.render_pipeline_filtration(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_CONTINUOUS_IMPROVEMENT_PDCA", "CONTINUOUS_IMPROVEMENT_PDCA", "PDCA_IMPROVEMENT"}:
            return self.processes.render_continuous_improvement_pdca(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_DEVSECOPS_INFINITY_LOOP", "DEVSECOPS_INFINITY_LOOP", "DEVSECOPS_LOOP"}:
            return self.processes.render_devsecops_infinity_loop(slide, spec, left, top, width, height)
        elif vj in {"PROCESS_CRITICAL_PATH_CPM", "CRITICAL_PATH_CPM", "PERT_CPM"}:
            return self.processes.render_critical_path_cpm(slide, spec, left, top, width, height)

        # ----------------- 4. ARCHITECTURES (25) -----------------
        elif vj in {"ARCH_SYSTEM_LAYERED_STACK", "SYSTEM_LAYERED_STACK", "LAYERED_ARCHITECTURE"}:
            return self.architectures.render_system_layered_stack(slide, spec, left, top, width, height)
        elif vj in {"ARCH_ORG_HIERARCHY_TREE", "ORG_HIERARCHY_TREE", "ORGANIZATION_CHART"}:
            return self.architectures.render_org_hierarchy_tree(slide, spec, left, top, width, height)
        elif vj in {"ARCH_RADIAL_MIND_MAP", "RADIAL_MIND_MAP", "MIND_MAP"}:
            return self.architectures.render_radial_mind_map(slide, spec, left, top, width, height)
        elif vj in {"ARCH_MICROSERVICES_MESH", "MICROSERVICES_MESH", "SERVICE_MESH"}:
            return self.architectures.render_microservices_mesh(slide, spec, left, top, width, height)
        elif vj in {"ARCH_DEFENSE_IN_DEPTH", "DEFENSE_IN_DEPTH", "SECURITY_SHIELD_LAYERS"}:
            return self.architectures.render_defense_in_depth(slide, spec, left, top, width, height)
        elif vj in {"ARCH_CLOUD_HYBRID_INFRA", "CLOUD_HYBRID_INFRA", "HYBRID_CLOUD"}:
            return self.architectures.render_cloud_hybrid_infra(slide, spec, left, top, width, height)
        elif vj in {"ARCH_BUS_BAR_MODULAR", "BUS_BAR_MODULAR", "EVENT_BUS_ARCHITECTURE"}:
            return self.architectures.render_bus_bar_modular(slide, spec, left, top, width, height)
        elif vj in {"ARCH_HEXAGONAL_PORTS", "HEXAGONAL_PORTS", "PORTS_AND_ADAPTERS"}:
            return self.architectures.render_hexagonal_ports(slide, spec, left, top, width, height)
        elif vj in {"ARCH_ECOSYSTEM_NETWORK", "ECOSYSTEM_NETWORK", "VALUE_NETWORK"}:
            return self.architectures.render_ecosystem_network(slide, spec, left, top, width, height)
        elif vj in {"ARCH_MATRIX_ORGANIZATION", "MATRIX_ORGANIZATION", "MATRIX_ORG"}:
            return self.architectures.render_matrix_organization(slide, spec, left, top, width, height)
        elif vj in {"ARCH_API_GATEWAY_HUB", "API_GATEWAY_HUB", "GATEWAY_HUB"}:
            return self.architectures.render_api_gateway_hub(slide, spec, left, top, width, height)
        elif vj in {"ARCH_DATA_GOVERNANCE_MESH", "DATA_GOVERNANCE_MESH", "DATA_MESH"}:
            return self.architectures.render_data_governance_mesh(slide, spec, left, top, width, height)
        elif vj in {"ARCH_CLEAN_ONION_STACK", "CLEAN_ONION_STACK", "ONION_ARCHITECTURE"}:
            return self.architectures.render_clean_onion_stack(slide, spec, left, top, width, height)
        elif vj in {"ARCH_CONTAINER_CLUSTER_K8S", "CONTAINER_CLUSTER_K8S", "K8S_CLUSTER"}:
            return self.architectures.render_container_cluster_k8s(slide, spec, left, top, width, height)
        elif vj in {"ARCH_AI_AGENT_ORCHESTRATOR", "AI_AGENT_ORCHESTRATOR", "AGENT_ORCHESTRATION"}:
            return self.architectures.render_ai_agent_orchestrator(slide, spec, left, top, width, height)
        elif vj in {"ARCH_EVENT_DRIVEN_KAFKA", "EVENT_DRIVEN_KAFKA", "KAFKA_STREAMING"}:
            return self.architectures.render_event_driven_kafka(slide, spec, left, top, width, height)
        elif vj in {"ARCH_SERVERLESS_EVENT_FLOW", "SERVERLESS_EVENT_FLOW", "SERVERLESS_ARCHITECTURE"}:
            return self.architectures.render_serverless_event_flow(slide, spec, left, top, width, height)
        elif vj in {"ARCH_ZERO_TRUST_SECURITY", "ZERO_TRUST_SECURITY", "ZERO_TRUST"}:
            return self.architectures.render_zero_trust_security(slide, spec, left, top, width, height)
        elif vj in {"ARCH_DATA_LAKEHOUSE_MEDALLION", "DATA_LAKEHOUSE_MEDALLION", "MEDALLION_LAKEHOUSE"}:
            return self.architectures.render_data_lakehouse_medallion(slide, spec, left, top, width, height)
        elif vj in {"ARCH_CI_CD_AUTOMATION", "CI_CD_AUTOMATION", "CI_CD_PIPELINE"}:
            return self.architectures.render_ci_cd_automation(slide, spec, left, top, width, height)
        elif vj in {"ARCH_HUB_SPOKE_ENTERPRISE_NETWORK", "HUB_SPOKE_ENTERPRISE_NETWORK", "ENTERPRISE_HUB_SPOKE"}:
            return self.architectures.render_hub_spoke_enterprise_network(slide, spec, left, top, width, height)
        elif vj in {"ARCH_MULTI_TENANT_SAAS", "MULTI_TENANT_SAAS", "SAAS_MULTI_TENANT"}:
            return self.architectures.render_multi_tenant_saas(slide, spec, left, top, width, height)
        elif vj in {"ARCH_RAG_LLM_PIPELINE", "RAG_LLM_PIPELINE", "RAG_PIPELINE"}:
            return self.architectures.render_rag_llm_pipeline(slide, spec, left, top, width, height)
        elif vj in {"ARCH_EDGE_TO_CLOUD_IOT", "EDGE_TO_CLOUD_IOT", "IOT_EDGE_TO_CLOUD"}:
            return self.architectures.render_edge_to_cloud_iot(slide, spec, left, top, width, height)
        elif vj in {"ARCH_MODULAR_MONOLITH", "MODULAR_MONOLITH"}:
            return self.architectures.render_modular_monolith(slide, spec, left, top, width, height)

        # ----------------- 5. NATIVE OFFICE CHARTS (20) -----------------
        elif vj in {"CHART_COLUMN_CLUSTERED", "COLUMN_CLUSTERED"}:
            return self.charts.render_column_clustered(slide, spec, left, top, width, height)
        elif vj in {"CHART_COLUMN_STACKED", "COLUMN_STACKED"}:
            return self.charts.render_column_stacked(slide, spec, left, top, width, height)
        elif vj in {"CHART_COLUMN_100_STACKED", "COLUMN_100_STACKED"}:
            return self.charts.render_column_100_stacked(slide, spec, left, top, width, height)
        elif vj in {"CHART_BAR_CLUSTERED", "BAR_CLUSTERED"}:
            return self.charts.render_bar_clustered(slide, spec, left, top, width, height)
        elif vj in {"CHART_BAR_DIVERGING", "BAR_DIVERGING", "CHART_BAR_DIVERGING_PYRAMID", "POPULATION_PYRAMID_NATIVE"}:
            return self.charts.render_bar_diverging(slide, spec, left, top, width, height)
        elif vj in {"CHART_LINE_TREND", "LINE_TREND", "CHART_LINE_WITH_MARKERS"}:
            return self.charts.render_line_trend(slide, spec, left, top, width, height)
        elif vj in {"CHART_AREA_STANDARD", "AREA_STANDARD"}:
            return self.charts.render_area_standard(slide, spec, left, top, width, height)
        elif vj in {"CHART_AREA_STACKED", "AREA_STACKED"}:
            return self.charts.render_area_stacked(slide, spec, left, top, width, height)
        elif vj in {"CHART_DONUT_KPI", "DONUT_KPI", "CHART_DONUT_KPI_CENTER"}:
            return self.charts.render_donut_kpi(slide, spec, left, top, width, height)
        elif vj in {"CHART_PIE_HIGHLIGHT_SLICE", "PIE_HIGHLIGHT_SLICE", "PIE_EXPLODED"}:
            return self.charts.render_pie_highlight_slice(slide, spec, left, top, width, height)
        elif vj in {"CHART_WATERFALL", "WATERFALL", "CHART_WATERFALL_BRIDGE"}:
            return self.charts.render_waterfall(slide, spec, left, top, width, height)
        elif vj in {"CHART_COMBO_DUAL_AXIS", "COMBO_DUAL_AXIS"}:
            return self.charts.render_combo_dual_axis(slide, spec, left, top, width, height)
        elif vj in {"CHART_RADAR", "RADAR", "CHART_RADAR_CAPABILITY"}:
            return self.charts.render_radar(slide, spec, left, top, width, height)
        elif vj in {"CHART_SCATTER_CORRELATION", "SCATTER_CORRELATION"}:
            return self.charts.render_scatter_correlation(slide, spec, left, top, width, height)
        elif vj in {"CHART_BUBBLE_MATRIX", "BUBBLE_MATRIX"}:
            return self.charts.render_bubble_matrix(slide, spec, left, top, width, height)
        elif vj in {"CHART_BAR_STACKED_100", "BAR_STACKED_100"}:
            return self.charts.render_bar_stacked_100(slide, spec, left, top, width, height)
        elif vj in {"CHART_PARETO_ANALYSIS", "PARETO_ANALYSIS", "PARETO_CHART"}:
            return self.charts.render_pareto_analysis(slide, spec, left, top, width, height)
        elif vj in {"CHART_STEPPED_LINE", "STEPPED_LINE"}:
            return self.charts.render_stepped_line(slide, spec, left, top, width, height)
        elif vj in {"CHART_RADAR_FILLED", "RADAR_FILLED"}:
            return self.charts.render_radar_filled(slide, spec, left, top, width, height)
        elif vj in {"CHART_HISTOGRAM_DISTRIBUTION", "HISTOGRAM_DISTRIBUTION", "HISTOGRAM"}:
            return self.charts.render_histogram_distribution(slide, spec, left, top, width, height)

        # ----------------- 6. KEYNOTE CONTAINERS & ACCENTS (30) -----------------
        elif vj in {"CONTAINER_BENTO_COMPLEX", "BENTO_COMPLEX", "CONTAINER_BENTO_COMPLEX_4"}:
            return self.containers.render_bento_complex(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_BENTO_GRID_3X3", "BENTO_GRID_3X3"}:
            return self.containers.render_bento_grid_3x3(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_KPI_STAT_DELTA", "KPI_STAT_DELTA"}:
            return self.containers.render_kpi_stat_delta(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_BEFORE_AFTER", "BEFORE_AFTER", "CONTRAST_SPLIT", "CONTAINER_BEFORE_AFTER_SPLIT"}:
            return self.containers.render_before_after(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_EXECUTIVE_QUOTE", "EXECUTIVE_QUOTE", "QUOTE_BANNER"}:
            return self.containers.render_executive_quote(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_TIMELINE_FLOW", "TIMELINE_FLOW"}:
            return self.containers.render_timeline_flow(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_PILLAR_3D", "PILLAR_3D", "THREE_PILLARS", "CONTAINER_PILLAR_3_COLUMNS"}:
            return self.containers.render_pillar_3d(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_PILLAR_4_COLUMNS", "PILLAR_4_COLUMNS", "FOUR_PILLARS"}:
            return self.containers.render_pillar_4_columns(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_PROBLEM_SOL_3STEP", "PROBLEM_SOL_3STEP", "PROBLEM_SOLUTION_STEP"}:
            return self.containers.render_problem_sol_3step(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_TARGET_BULLSEYE", "TARGET_BULLSEYE", "BULLSEYE"}:
            return self.containers.render_target_bullseye(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_BALANCE_SEESAW", "BALANCE_SEESAW", "SEESAW"}:
            return self.containers.render_balance_seesaw(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_GAUGE_METER_DIAL", "GAUGE_METER_DIAL", "SPEEDOMETER"}:
            return self.containers.render_gauge_meter_dial(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_GLASSMORPHIC_HERO", "GLASSMORPHIC_HERO"}:
            return self.containers.render_glassmorphic_hero(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_HERO_SPLIT_CARDS", "HERO_SPLIT_CARDS"}:
            return self.containers.render_hero_split_cards(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_DIAGONAL_SPLIT", "DIAGONAL_SPLIT"}:
            return self.containers.render_diagonal_split(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_NOTIFICATION_TAGS", "NOTIFICATION_TAGS"}:
            return self.containers.render_notification_tags(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_CUSTOMER_JOURNEY", "CUSTOMER_JOURNEY"}:
            return self.containers.render_customer_journey(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_ISOMETRIC_STACK", "ISOMETRIC_STACK"}:
            return self.containers.render_isometric_stack(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_TABBED_OVERVIEW", "TABBED_OVERVIEW"}:
            return self.containers.render_tabbed_overview(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_EXECUTIVE_DASHBOARD", "EXECUTIVE_DASHBOARD"}:
            return self.containers.render_executive_dashboard(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_CLOSING_CTA_HERO", "CLOSING_CTA_HERO", "CLOSING_CTA"}:
            return self.containers.render_closing_cta_hero(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_DEVICE_MOCKUP_FRAME", "DEVICE_MOCKUP_FRAME", "MOCKUP_FRAME"}:
            return self.containers.render_device_mockup_frame(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_METRIC_MARQUEE_BANNER", "METRIC_MARQUEE_BANNER", "MARQUEE_BANNER"}:
            return self.containers.render_metric_marquee_banner(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_THREE_PILLARS_CARDS", "THREE_PILLARS_CARDS"}:
            return self.containers.render_three_pillars_cards(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_PROBLEM_SOLUTION_IMPACT", "PROBLEM_SOLUTION_IMPACT", "PROBLEM_SOL_IMPACT"}:
            return self.containers.render_problem_solution_impact(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_FEATURE_HEX_CLUSTER", "FEATURE_HEX_CLUSTER", "HEX_CLUSTER"}:
            return self.containers.render_feature_hex_cluster(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_TESTIMONIAL_CAROUSEL_ROW", "TESTIMONIAL_CAROUSEL_ROW", "TESTIMONIALS_ROW"}:
            return self.containers.render_testimonial_carousel_row(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_STAT_HERO_SPLIT_60_40", "STAT_HERO_SPLIT_60_40", "STAT_SPLIT_60_40"}:
            return self.containers.render_stat_hero_split_60_40(slide, spec, left, top, width, height)
        elif vj in {"CONTAINER_MINIMALIST_APPLE_QUOTE", "MINIMALIST_APPLE_QUOTE", "APPLE_QUOTE"}:
            return self.containers.render_minimalist_apple_quote(slide, spec, left, top, width, height)

        return None


def detect_optimal_archetype(slide_spec: Dict[str, Any]) -> str:
    """
    Exhaustive Semantic Pattern Recognizer for 110+ Archetypes.
    Inspects slide data, tables, charts, narrative atoms, and keywords
    to automatically assign the most sophisticated presentation archetype.
    """
    # 1. Check Table data
    if slide_spec.get("table_data"):
        t_data = slide_spec["table_data"]
        headers = [str(h).lower() for h in t_data.get("headers", [])]
        h_str = " ".join(headers)

        if "raci" in h_str or "trách nhiệm" in h_str or "accountable" in h_str:
            return "TABLE_RACI_GOVERNANCE"
        elif "sla" in h_str or "uptime" in h_str or "thời gian phản hồi" in h_str:
            return "TABLE_SLA_TIERS"
        elif "ngân sách" in h_str or "dự toán" in h_str or "capex" in h_str or "opex" in h_str:
            return "TABLE_BUDGET_ALLOCATION"
        elif "nhà thầu" in h_str or "nhà cung cấp" in h_str or "vendor" in h_str:
            return "TABLE_VENDOR_EVALUATION"
        elif "okr" in h_str or "mục tiêu then chốt" in h_str or "key result" in h_str:
            return "TABLE_OKRS_TRACKER"
        elif "kỹ năng" in h_str or "ma trận kỹ năng" in h_str or "skills" in h_str:
            return "TABLE_EMPLOYEE_SKILLS_MATRIX"
        elif "thông số" in h_str or "cấu hình" in h_str or "specs" in h_str:
            return "TABLE_PRODUCT_SPECS"
        elif "5x5" in h_str or "nhiệt 5x5" in h_str:
            return "TABLE_RISK_HEATMAP_5X5"
        elif "bàn giao" in h_str or "deliverable" in h_str:
            return "TABLE_MILESTONE_DELIVERABLES"
        elif "swot chi tiết" in h_str:
            return "TABLE_SWOT_DETAILED"
        elif "tính năng 4 gói" in h_str or "pricing feature" in h_str:
            return "TABLE_PRICING_FEATURE_MATRIX"
        elif "rủi ro" in h_str or "xác suất" in h_str or "thiệt hại" in h_str:
            return "TABLE_RISK_REGISTER"
        elif "doanh thu" in h_str or "lợi nhuận" in h_str or "ebitda" in h_str or "chi phí" in h_str:
            return "TABLE_FINANCIAL_PL"
        elif "giá" in h_str or "tier" in h_str or "gói" in h_str or "bản quyền" in h_str:
            return "TABLE_PRICING_TIERS"
        elif "đối thủ" in h_str or "benchmark" in h_str or "cạnh tranh" in h_str:
            return "TABLE_COMPETITOR_BENCHMARK"
        elif "khoảng trống" in h_str or "gap" in h_str or "năng lực" in h_str:
            return "TABLE_CAPABILITY_GAP"
        elif "tuân thủ" in h_str or "kiểm toán" in h_str or "audit" in h_str:
            return "TABLE_AUDIT_COMPLIANCE"
        elif "ưu điểm" in h_str or "nhược điểm" in h_str or "pros" in h_str or "cons" in h_str:
            return "TABLE_PROS_CONS"
        elif "tiến độ" in h_str or "milestone" in h_str or "sprint" in h_str:
            return "TABLE_ROADMAP_SCHEDULE"
        elif "khu vực" in h_str or "thị phần" in h_str or "doanh số" in h_str:
            return "TABLE_SALES_TERRITORY"
        elif "trọng số" in h_str or "weight" in h_str or "điểm số" in h_str:
            return "TABLE_WEIGHTED_DECISION"
        elif "tóm tắt" in h_str or "điều hành" in h_str or "chỉ số chính" in h_str:
            return "TABLE_EXECUTIVE_SUMMARY"
        elif "so sánh" in h_str or "giải pháp" in h_str or "tính năng" in h_str:
            return "TABLE_COMPARISON_PRO"
        elif "điểm" in h_str or "trạng thái" in h_str or "scorecard" in h_str:
            return "TABLE_SCORECARD_HEATMAP"
        return "TABLE_METRIC_MATRIX"

    # 2. Check Chart data
    if slide_spec.get("chart_data") or slide_spec.get("chart_type"):
        ctype = str(slide_spec.get("chart_type", "")).upper()
        if "PARETO" in ctype or "80/20" in ctype:
            return "CHART_PARETO_ANALYSIS"
        elif "STEPPED" in ctype or "BẬC THANG" in ctype:
            return "CHART_STEPPED_LINE"
        elif "RADAR_FILLED" in ctype or "FILLED_RADAR" in ctype:
            return "CHART_RADAR_FILLED"
        elif "HISTOGRAM" in ctype or "TẦN SUẤT" in ctype:
            return "CHART_HISTOGRAM_DISTRIBUTION"
        elif "BAR_STACKED_100" in ctype or ("100" in ctype and "BAR" in ctype):
            return "CHART_BAR_STACKED_100"
        elif "PYRAMID" in ctype or "DIVERGING" in ctype:
            return "CHART_BAR_DIVERGING_PYRAMID"
        elif "DONUT" in ctype or "DOUGHNUT" in ctype:
            return "CHART_DONUT_KPI_CENTER"
        elif "PIE" in ctype:
            return "CHART_PIE_HIGHLIGHT_SLICE"
        elif "TREND" in ctype or "LINE" in ctype:
            return "CHART_LINE_WITH_MARKERS"
        elif "WATERFALL" in ctype:
            return "CHART_WATERFALL_BRIDGE"
        elif "RADAR" in ctype or "SPIDER" in ctype:
            return "CHART_RADAR_CAPABILITY"
        elif "COMBO" in ctype:
            return "CHART_COMBO_DUAL_AXIS"
        elif "100" in ctype:
            return "CHART_COLUMN_100_STACKED"
        elif "STACKED" in ctype and "AREA" in ctype:
            return "CHART_AREA_STACKED"
        elif "AREA" in ctype:
            return "CHART_AREA_STANDARD"
        elif "BAR" in ctype:
            return "CHART_BAR_CLUSTERED"
        elif "SCATTER" in ctype:
            return "CHART_SCATTER_CORRELATION"
        elif "BUBBLE" in ctype:
            return "CHART_BUBBLE_MATRIX"
        return "CHART_COLUMN_CLUSTERED"

    # 3. Check Text Keywords in Title / Claim / Atoms
    full_text = (
        str(slide_spec.get("assertion_title", "")) + " " +
        str(slide_spec.get("primary_claim", "")) + " " +
        str(slide_spec.get("atoms", []))
    ).lower()

    # Strategic Frameworks Keywords
    if any(kw in full_text for kw in ["ma trận 2x2", "2x2", "quadrant", "eisenhower", "bcg"]):
        return "FRAMEWORK_MATRIX_2X2"
    elif any(kw in full_text for kw in ["9 ô", "3x3", "ge mckinsey", "sức hấp dẫn"]):
        return "FRAMEWORK_MATRIX_3X3"
    elif any(kw in full_text for kw in ["5 áp lực", "porter", "áp lực cạnh tranh"]):
        return "FRAMEWORK_PORTER_5_FORCES"
    elif any(kw in full_text for kw in ["chuỗi giá trị", "value chain", "hậu cần"]):
        return "FRAMEWORK_VALUE_CHAIN"
    elif any(kw in full_text for kw in ["swot", "điểm mạnh", "điểm yếu", "cơ hội", "thách thức"]):
        return "FRAMEWORK_SWOT_ANALYSIS"
    elif any(kw in full_text for kw in ["pestel", "pestle", "khung pestel", "mô hình pestel"]):
        return "FRAMEWORK_PESTEL_HEX"
    elif any(kw in full_text for kw in ["thẻ điểm cân bằng", "balanced scorecard", "bsc"]):
        return "FRAMEWORK_BALANCED_SCORECARD"
    elif any(kw in full_text for kw in ["ngôi nhà", "strategy house", "móng nhà", "tầm nhìn chiến lược"]):
        return "FRAMEWORK_STRATEGY_HOUSE"
    elif any(kw in full_text for kw in ["tháp ngược", "inverted pyramid"]):
        return "FRAMEWORK_INVERTED_PYRAMID"
    elif any(kw in full_text for kw in ["tháp", "pyramid", "maslow", "tháp phân cấp", "tháp nhu cầu"]):
        return "FRAMEWORK_PYRAMID_ASCENDING"
    elif any(kw in full_text for kw in ["aarrr", "pirate", "phễu aarrr"]):
        return "FRAMEWORK_PIRATE_AARRR"
    elif any(kw in full_text for kw in ["phễu lọc", "lọc đa tầng", "pipeline filtration"]):
        return "PROCESS_PIPELINE_FILTRATION"
    elif any(kw in full_text for kw in ["phễu", "funnel", "chuyển đổi", "tỷ lệ rớt"]):
        return "FRAMEWORK_CONVERSION_FUNNEL"
    elif any(kw in full_text for kw in ["vòng quay", "flywheel", "bánh đà"]):
        return "FRAMEWORK_GROWTH_FLYWHEEL"
    elif any(kw in full_text for kw in ["hệ sinh thái", "hub", "spoke", "vệ tinh"]):
        return "FRAMEWORK_HUB_SPOKE"
    elif any(kw in full_text for kw in ["đồng tâm", "concentric"]):
        return "FRAMEWORK_CONCENTRIC_RINGS"
    elif any(kw in full_text for kw in ["giao thoa 3", "venn 3", "ikigai"]):
        return "FRAMEWORK_VENN_3_SET"
    elif any(kw in full_text for kw in ["giao thoa", "venn", "sweet spot"]):
        return "FRAMEWORK_VENN_2_SET"
    elif any(kw in full_text for kw in ["kim cương", "diamond model"]):
        return "FRAMEWORK_DIAMOND_MODEL"
    elif any(kw in full_text for kw in ["ansoff", "thâm nhập thị trường", "đa dạng hóa"]):
        return "FRAMEWORK_ANSOFF_MATRIX"
    elif any(kw in full_text for kw in ["mckinsey 7s", "7s"]):
        return "FRAMEWORK_MCKINSEY_7S"
    elif any(kw in full_text for kw in ["đồng hồ chiến lược", "bowman"]):
        return "FRAMEWORK_STRATEGY_CLOCK"
    elif any(kw in full_text for kw in ["cmmi", "độ trưởng thành", "maturity"]):
        return "FRAMEWORK_CMMI_STAIRS"
    elif any(kw in full_text for kw in ["vrio", "độ hiếm", "khó sao chép"]):
        return "FRAMEWORK_VRIO_MATRIX"
    elif any(kw in full_text for kw in ["vòng tròn vàng", "golden circle", "simon sinek"]):
        return "FRAMEWORK_GOLDEN_CIRCLE"
    elif any(kw in full_text for kw in ["tảng băng", "iceberg"]):
        return "FRAMEWORK_ICEBERG_MODEL"
    elif any(kw in full_text for kw in ["double diamond", "2 viên kim cương"]):
        return "FRAMEWORK_DOUBLE_DIAMOND"
    elif any(kw in full_text for kw in ["steeple", "môi trường vĩ mô 7"]):
        return "FRAMEWORK_STEEPLE"
    elif any(kw in full_text for kw in ["kano", "phân loại tính năng"]):
        return "FRAMEWORK_KANO_MODEL"
    elif any(kw in full_text for kw in ["lean canvas", "kinh doanh tinh gọn"]):
        return "FRAMEWORK_LEAN_CANVAS"
    elif any(kw in full_text for kw in ["value proposition", "đề xuất giá trị"]):
        return "FRAMEWORK_VALUE_PROPOSITION_CANVAS"
    elif any(kw in full_text for kw in ["cynefin", "khung cynefin"]):
        return "FRAMEWORK_CYNEFIN"
    elif any(kw in full_text for kw in ["bow tie", "nơ bướm", "rào chắn rủi ro"]):
        return "FRAMEWORK_BOW_TIE"
    elif any(kw in full_text for kw in ["errc", "đại dương xanh", "blue ocean"]):
        return "FRAMEWORK_BLUE_OCEAN_ERRC"
    elif any(kw in full_text for kw in ["north star", "bắc đẩu", "nsm"]):
        return "FRAMEWORK_NORTH_STAR_METRIC"
    elif any(kw in full_text for kw in ["grow coaching", "mô hình grow"]):
        return "FRAMEWORK_GROW_COACHING"
    elif any(kw in full_text for kw in ["aarrr", "pirate metrics", "phễu aarrr"]):
        return "FRAMEWORK_PIRATE_AARRR"

    # Process Keywords
    elif any(kw in full_text for kw in ["chu trình 6 bước", "loop 6"]):
        return "PROCESS_CIRCULAR_LOOP_6STEP"
    elif any(kw in full_text for kw in ["xoắn ốc", "spiral"]):
        return "PROCESS_SPIRAL_GROWTH"
    elif any(kw in full_text for kw in ["đồng hồ cát", "hourglass"]):
        return "PROCESS_HOURGLASS_WORKFLOW"
    elif any(kw in full_text for kw in ["3 luồng song song", "parallel streams"]):
        return "PROCESS_PARALLEL_STREAMS"
    elif any(kw in full_text for kw in ["stage gate", "cổng quyết định"]):
        return "PROCESS_STAGED_GATE_PHASES"
    elif any(kw in full_text for kw in ["serpentine", "lộ trình chữ s", "s roadmap"]):
        return "PROCESS_SERPENTINE_ROADMAP"
    elif any(kw in full_text for kw in ["lọc đa tầng", "pipeline filtration"]):
        return "PROCESS_PIPELINE_FILTRATION"
    elif any(kw in full_text for kw in ["pdca liên tục", "cải tiến liên tục pdca"]):
        return "PROCESS_CONTINUOUS_IMPROVEMENT_PDCA"
    elif any(kw in full_text for kw in ["devsecops", "vô cực", "infinity loop"]):
        return "PROCESS_DEVSECOPS_INFINITY_LOOP"
    elif any(kw in full_text for kw in ["đường găng", "pert cpm", "critical path"]):
        return "PROCESS_CRITICAL_PATH_CPM"
    elif any(kw in full_text for kw in ["đường cong", "s-curve", "curved pipeline", "ống dẫn cong"]):
        return "PROCESS_CURVED_PIPELINE"
    elif any(kw in full_text for kw in ["chu trình", "vòng tuần hoàn", "pdca"]):
        return "PROCESS_CIRCULAR_CYCLE"
    elif any(kw in full_text for kw in ["bánh răng", "gears", "ăn khớp"]):
        return "PROCESS_INTERLOCKING_GEARS"
    elif any(kw in full_text for kw in ["xương cá", "ishikawa", "nguyên nhân kết quả"]):
        return "PROCESS_FISHBONE_ISHIKAWA"
    elif any(kw in full_text for kw in ["cây quyết định", "decision tree", "yes/no"]):
        return "PROCESS_DECISION_FLOW"
    elif any(kw in full_text for kw in ["phân làn", "swimlane"]):
        return "PROCESS_SWIMLANE_TRACKS"
    elif any(kw in full_text for kw in ["bậc thang", "stairs"]):
        return "PROCESS_ASCENDING_STAIRS"
    elif any(kw in full_text for kw in ["ruy băng", "flag ribbon"]):
        return "PROCESS_TIMELINE_FLAG_RIBBON"
    elif any(kw in full_text for kw in ["trục dọc", "xương sống", "vertical spine"]):
        return "PROCESS_VERTICAL_SPINE"
    elif any(kw in full_text for kw in ["gantt", "thanh tiến độ"]):
        return "PROCESS_GANTT_ROADMAP"
    elif any(kw in full_text for kw in ["3 chân trời", "three horizons"]):
        return "PROCESS_3_HORIZONS_ROADMAP"
    elif any(kw in full_text for kw in ["scrum", "sprint", "agile"]):
        return "PROCESS_AGILE_SCRUM_CYCLE"
    elif any(kw in full_text for kw in ["cầu nối", "as-is", "to-be", "chuyển đổi hệ thống"]):
        return "PROCESS_BRIDGE_MIGRATION"
    elif any(kw in full_text for kw in ["mảnh ghép", "jigsaw", "puzzle"]):
        return "PROCESS_JIGSAW_PUZZLE"
    elif any(kw in full_text for kw in ["tổ ong", "lục giác", "honeycomb"]):
        return "PROCESS_HONEYCOMB_CHAIN"
    elif any(kw in full_text for kw in ["etl", "pipeline dữ liệu", "etl pipeline", "data pipeline", "thu nạp"]):
        return "PROCESS_ETL_DATA_PIPELINE"
    elif any(kw in full_text for kw in ["chiếc thang", "ladder", "nâng tầm"]):
        return "PROCESS_LEVEL_UP_LADDER"
    elif any(kw in full_text for kw in ["domino", "dây chuyền"]):
        return "PROCESS_DOMINO_CASCADE"
    elif any(kw in full_text for kw in ["tỏa tia", "360 độ", "radial"]):
        return "PROCESS_RADIAL_PROGRESSION"
    elif any(kw in full_text for kw in ["quy trình", "các bước", "bước 1", "chevron"]):
        return "PROCESS_CHEVRON_LINEAR"

    # Architecture Keywords
    elif any(kw in full_text for kw in ["kafka", "event driven", "hướng sự kiện"]):
        return "ARCH_EVENT_DRIVEN_KAFKA"
    elif any(kw in full_text for kw in ["serverless", "không máy chủ", "cloud function"]):
        return "ARCH_SERVERLESS_EVENT_FLOW"
    elif any(kw in full_text for kw in ["zero trust", "không tin cậy", "an ninh 5 lớp"]):
        return "ARCH_ZERO_TRUST_SECURITY"
    elif any(kw in full_text for kw in ["medallion", "lakehouse", "bronze silver gold"]):
        return "ARCH_DATA_LAKEHOUSE_MEDALLION"
    elif any(kw in full_text for kw in ["ci/cd", "tự động hóa build", "pipeline ci cd"]):
        return "ARCH_CI_CD_AUTOMATION"
    elif any(kw in full_text for kw in ["hub spoke enterprise", "transit gateway"]):
        return "ARCH_HUB_SPOKE_ENTERPRISE_NETWORK"
    elif any(kw in full_text for kw in ["multi tenant", "đa người thuê", "saas multi tenant"]):
        return "ARCH_MULTI_TENANT_SAAS"
    elif any(kw in full_text for kw in ["rag", "vector db", "retriever llm"]):
        return "ARCH_RAG_LLM_PIPELINE"
    elif any(kw in full_text for kw in ["edge to cloud", "iot cảm biến"]):
        return "ARCH_EDGE_TO_CLOUD_IOT"
    elif any(kw in full_text for kw in ["modular monolith", "monolith module hóa"]):
        return "ARCH_MODULAR_MONOLITH"
    elif any(kw in full_text for kw in ["phân tầng", "layered", "tầng 1", "tier"]):
        return "ARCH_SYSTEM_LAYERED_STACK"
    elif any(kw in full_text for kw in ["cơ cấu tổ chức", "sơ đồ tổ chức", "org chart"]):
        return "ARCH_ORG_HIERARCHY_TREE"
    elif any(kw in full_text for kw in ["sơ đồ tư duy", "mind map"]):
        return "ARCH_RADIAL_MIND_MAP"
    elif any(kw in full_text for kw in ["microservices", "service mesh"]):
        return "ARCH_MICROSERVICES_MESH"
    elif any(kw in full_text for kw in ["đa tầng bảo mật", "defense in depth", "lá chắn"]):
        return "ARCH_DEFENSE_IN_DEPTH"
    elif any(kw in full_text for kw in ["đám mây lai", "hybrid cloud"]):
        return "ARCH_CLOUD_HYBRID_INFRA"
    elif any(kw in full_text for kw in ["trục xe buýt", "event bus", "bus bar"]):
        return "ARCH_BUS_BAR_MODULAR"
    elif any(kw in full_text for kw in ["ports", "adapters", "kiến trúc lục giác"]):
        return "ARCH_HEXAGONAL_PORTS"
    elif any(kw in full_text for kw in ["mạng lưới giá trị", "hệ sinh thái mạng"]):
        return "ARCH_ECOSYSTEM_NETWORK"
    elif any(kw in full_text for kw in ["tổ chức ma trận", "matrix org"]):
        return "ARCH_MATRIX_ORGANIZATION"
    elif any(kw in full_text for kw in ["api gateway", "cổng điều phối"]):
        return "ARCH_API_GATEWAY_HUB"
    elif any(kw in full_text for kw in ["quản trị dữ liệu", "data mesh", "xuất xứ dữ liệu"]):
        return "ARCH_DATA_GOVERNANCE_MESH"
    elif any(kw in full_text for kw in ["củ hành", "clean architecture", "onion"]):
        return "ARCH_CLEAN_ONION_STACK"
    elif any(kw in full_text for kw in ["k8s", "kubernetes", "container cluster"]):
        return "ARCH_CONTAINER_CLUSTER_K8S"
    elif any(kw in full_text for kw in ["orchestrator", "đa tác tử", "điều phối ai"]):
        return "ARCH_AI_AGENT_ORCHESTRATOR"

    # Keynote Containers Keywords
    elif any(kw in full_text for kw in ["màn hình thiết bị", "mockup", "laptop frame"]):
        return "CONTAINER_DEVICE_MOCKUP_FRAME"
    elif any(kw in full_text for kw in ["marquee banner", "dải banner 4 chỉ số"]):
        return "CONTAINER_METRIC_MARQUEE_BANNER"
    elif any(kw in full_text for kw in ["3 trụ cột kính mờ", "three pillars glass", "three pillars", "ba trụ cột"]):
        return "CONTAINER_THREE_PILLARS_CARDS"
    elif any(kw in full_text for kw in ["nỗi đau giải pháp tác động", "problem solution impact", "vấn đề giải pháp tác động"]):
        return "CONTAINER_PROBLEM_SOLUTION_IMPACT"
    elif any(kw in full_text for kw in ["cụm lục giác", "feature hex cluster"]):
        return "CONTAINER_FEATURE_HEX_CLUSTER"
    elif any(kw in full_text for kw in ["nhận xét khách hàng", "testimonial carousel"]):
        return "CONTAINER_TESTIMONIAL_CAROUSEL_ROW"
    elif any(kw in full_text for kw in ["chia đôi 60 40", "stat split 60 40"]):
        return "CONTAINER_STAT_HERO_SPLIT_60_40"
    elif any(kw in full_text for kw in ["steve jobs", "trích dẫn tối giản", "apple quote"]):
        return "CONTAINER_MINIMALIST_APPLE_QUOTE"
    elif any(kw in full_text for kw in ["trước và sau", "before after", "thực trạng và giải pháp"]):
        return "CONTAINER_BEFORE_AFTER_SPLIT"
    elif any(kw in full_text for kw in ["trích dẫn", "quote"]):
        return "CONTAINER_EXECUTIVE_QUOTE"
    elif any(kw in full_text for kw in ["chỉ số", "kpi", "% yoy", "tăng trưởng"]):
        return "CONTAINER_KPI_STAT_DELTA"
    elif any(kw in full_text for kw in ["vấn đề", "hệ quả", "giải pháp"]):
        return "CONTAINER_PROBLEM_SOL_3STEP"
    elif any(kw in full_text for kw in ["mục tiêu", "bullseye", "hồng tâm"]):
        return "CONTAINER_TARGET_BULLSEYE"
    elif any(kw in full_text for kw in ["cán cân", "so sánh tương quan", "seesaw"]):
        return "CONTAINER_BALANCE_SEESAW"
    elif any(kw in full_text for kw in ["đồng hồ đo", "áp suất", "gauge"]):
        return "CONTAINER_GAUGE_METER_DIAL"
    elif any(kw in full_text for kw in ["kính mờ", "glassmorphic"]):
        return "CONTAINER_GLASSMORPHIC_HERO"
    elif any(kw in full_text for kw in ["tách đôi", "hero split"]):
        return "CONTAINER_HERO_SPLIT_CARDS"
    elif any(kw in full_text for kw in ["vát chéo", "diagonal"]):
        return "CONTAINER_DIAGONAL_SPLIT"
    elif any(kw in full_text for kw in ["huy hiệu", "ribbon", "notification"]):
        return "CONTAINER_NOTIFICATION_TAGS"
    elif any(kw in full_text for kw in ["hành trình khách hàng", "customer journey"]):
        return "CONTAINER_CUSTOMER_JOURNEY"
    elif any(kw in full_text for kw in ["chiều sâu", "isometric"]):
        return "CONTAINER_ISOMETRIC_STACK"
    elif any(kw in full_text for kw in ["tab", "điều hướng tab"]):
        return "CONTAINER_TABBED_OVERVIEW"
    elif any(kw in full_text for kw in ["bảng điều khiển", "dashboard tổng"]):
        return "CONTAINER_EXECUTIVE_DASHBOARD"
    elif any(kw in full_text for kw in ["kêu gọi hành động", "cta", "đăng ký ngay"]):
        return "CONTAINER_CLOSING_CTA_HERO"
    elif any(kw in full_text for kw in ["4 cột trụ", "4 trụ"]):
        return "CONTAINER_PILLAR_4_COLUMNS"
    elif any(kw in full_text for kw in ["3 cột trụ", "3 trụ"]):
        return "CONTAINER_PILLAR_3_COLUMNS"
    elif any(kw in full_text for kw in ["9 ô", "lưới bento"]):
        return "CONTAINER_BENTO_GRID_3X3"

    return "CONTAINER_BENTO_COMPLEX_4"

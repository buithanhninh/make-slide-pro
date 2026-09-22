"""
scripts/macc_council/gate4_spatial_motion/agent11_layout_archetype.py
Agent 11: LayoutArchetypeStrategist (Spatial Layout & Archetype Fit Auditor).
Ensures chosen layout archetypes structurally match the density and semantics of slide atoms.
Hardened with schema-agnostic counting, semantic intent recognition, and auto-remediation.
"""

from __future__ import annotations

import copy
import re
from typing import Any, Dict, List, Optional
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, Severity



try:
    from ...component_library import ARCHETYPES_REGISTRY
except (ImportError, ValueError):
    try:
        from scripts.component_library import ARCHETYPES_REGISTRY
    except ImportError:
        ARCHETYPES_REGISTRY = {}


class LayoutArchetypeStrategist(BaseCouncilAgent):
    """
    Agent 11: Layout Archetype Strategist.
    Audits alignment between the selected layout archetype and the atom/card count and semantic intent.
    Supports 165+ Archetypes across 6 core V8.6.0 presentation engines:
    Tables, Frameworks, Processes, Architectures, Office Charts, and Keynote Containers.
    Prevents spatial collisions, visual vacuums, and mismatched layout structures.
    """

    # Base legacy archetypes rules
    BASE_ATOM_RULES = {
        "title_hero": (0, 0),
        "split_comparison": (2, 2),
        "3_cards": (3, 3),
        "grid_2x2": (4, 4),
        "process_flow_4": (2, 4),
        "process_flow_5": (4, 5),
        "metric_callout_3x": (2, 3),
        "quote_callout": (0, 1),
        "conclusion_cta": (1, 4),
        "table_dense": (4, 20)
    }

    # Dedicated V8.6.0 Archetype Atom Requirements
    V86_ATOM_RULES = {
        # --- Frameworks (Module 2) ---
        "FRAMEWORK_SWOT_ANALYSIS": (4, 4), "SWOT_ANALYSIS": (4, 4), "SWOT": (4, 4),
        "FRAMEWORK_PESTEL_HEX": (6, 6), "PESTEL_HEX": (6, 6), "PESTEL": (6, 6),
        "FRAMEWORK_STEEPLE": (7, 7), "STEEPLE": (7, 7),
        "FRAMEWORK_MCKINSEY_7S": (7, 7), "MCKINSEY_7S": (7, 7), "7S_MODEL": (7, 7),
        "FRAMEWORK_PORTER_5_FORCES": (5, 5), "PORTER_5_FORCES": (5, 5), "FIVE_FORCES": (5, 5),
        "FRAMEWORK_BALANCED_SCORECARD": (4, 4), "BALANCED_SCORECARD": (4, 4), "BSC": (4, 4),
        "FRAMEWORK_MATRIX_2X2": (4, 4), "MATRIX_2X2": (4, 4), "2X2_MATRIX": (4, 4),
        "FRAMEWORK_MATRIX_3X3": (9, 9), "MATRIX_3X3": (9, 9), "GE_MCKINSEY_9BOX": (9, 9),
        "FRAMEWORK_PIRATE_AARRR": (5, 5), "PIRATE_AARRR": (5, 5), "AARRR_FUNNEL": (5, 5),
        "FRAMEWORK_GROW_COACHING": (4, 4), "GROW_COACHING": (4, 4),
        "FRAMEWORK_CYNEFIN": (4, 5), "CYNEFIN": (4, 5),
        "FRAMEWORK_DIAMOND_MODEL": (4, 4), "DIAMOND_MODEL": (4, 4), "PORTER_DIAMOND": (4, 4),
        "FRAMEWORK_DOUBLE_DIAMOND": (4, 4), "DOUBLE_DIAMOND": (4, 4), "DESIGN_THINKING_DIAMOND": (4, 4),
        "FRAMEWORK_ANSOFF_MATRIX": (4, 4), "ANSOFF_MATRIX": (4, 4), "ANSOFF": (4, 4),
        "FRAMEWORK_BLUE_OCEAN_ERRC": (4, 4), "BLUE_OCEAN_ERRC": (4, 4), "ERRC_GRID": (4, 4),
        "FRAMEWORK_GOLDEN_CIRCLE": (3, 3), "GOLDEN_CIRCLE": (3, 3), "SIMON_SINEK_CIRCLE": (3, 3),
        "FRAMEWORK_PYRAMID_ASCENDING": (3, 5), "FRAMEWORK_PYRAMID": (3, 5), "PYRAMID": (3, 5),
        "FRAMEWORK_INVERTED_PYRAMID": (3, 5), "INVERTED_PYRAMID": (3, 5),
        "FRAMEWORK_CONVERSION_FUNNEL": (3, 5), "FRAMEWORK_FUNNEL": (3, 5), "FUNNEL": (3, 5),
        "FRAMEWORK_GROWTH_FLYWHEEL": (3, 6), "FRAMEWORK_FLYWHEEL": (3, 6), "FLYWHEEL": (3, 6),
        "FRAMEWORK_HUB_SPOKE": (3, 8), "HUB_SPOKE": (3, 8), "HUB_AND_SPOKE": (3, 8),
        "FRAMEWORK_CONCENTRIC_RINGS": (3, 5), "CONCENTRIC_RINGS": (3, 5),
        "FRAMEWORK_VENN_2_SET": (2, 3), "FRAMEWORK_VENN": (2, 3), "VENN": (2, 3),
        "FRAMEWORK_VENN_3_SET": (3, 4), "VENN_3_SET": (3, 4),
        "FRAMEWORK_STRATEGY_HOUSE": (3, 6), "STRATEGY_HOUSE": (3, 6), "TEMPLE": (3, 6),
        "FRAMEWORK_STRATEGY_CLOCK": (4, 8), "STRATEGY_CLOCK": (4, 8), "BOWMAN_CLOCK": (4, 8),
        "FRAMEWORK_CMMI_STAIRS": (4, 6), "CMMI_STAIRS": (4, 6), "MATURITY_LADDER": (4, 6),
        "FRAMEWORK_VRIO_MATRIX": (4, 4), "VRIO_MATRIX": (4, 4), "VRIO": (4, 4),
        "FRAMEWORK_ICEBERG_MODEL": (2, 4), "ICEBERG_MODEL": (2, 4), "ICEBERG": (2, 4),
        "FRAMEWORK_VALUE_CHAIN": (3, 6), "VALUE_CHAIN": (3, 6),
        "FRAMEWORK_ROADMAP_GANTT": (3, 6), "ROADMAP_GANTT": (3, 6),
        "FRAMEWORK_SWIMLANE": (2, 5), "SWIMLANE": (2, 5),
        "FRAMEWORK_KANO_MODEL": (3, 5), "KANO_MODEL": (3, 5),
        "FRAMEWORK_LEAN_CANVAS": (4, 9), "LEAN_CANVAS": (4, 9),
        "FRAMEWORK_VALUE_PROPOSITION_CANVAS": (2, 6), "VALUE_PROPOSITION_CANVAS": (2, 6),
        "FRAMEWORK_BOW_TIE": (3, 6), "BOW_TIE": (3, 6),
        "FRAMEWORK_NORTH_STAR_METRIC": (2, 5), "NORTH_STAR_METRIC": (2, 5),

        # --- Processes (Module 3) ---
        "PROCESS_DEVSECOPS_INFINITY_LOOP": (4, 8), "DEVSECOPS_INFINITY_LOOP": (4, 8), "DEVSECOPS_LOOP": (4, 8),
        "PROCESS_CRITICAL_PATH_CPM": (4, 8), "CRITICAL_PATH_CPM": (4, 8), "PERT_CPM": (4, 8),
        "PROCESS_CIRCULAR_LOOP_6STEP": (5, 6), "CIRCULAR_LOOP_6STEP": (5, 6),
        "PROCESS_3_HORIZONS_ROADMAP": (3, 3), "THREE_HORIZONS": (3, 3), "MCKINSEY_3_HORIZONS": (3, 3),
        "PROCESS_AGILE_SCRUM_CYCLE": (3, 6), "AGILE_SCRUM_CYCLE": (3, 6), "SCRUM_SPRINT": (3, 6),
        "PROCESS_CHEVRON_LINEAR": (3, 6), "CHEVRON_LINEAR": (3, 6), "PROCESS_CHEVRON": (3, 6), "CHEVRON_FLOW": (3, 6),
        "PROCESS_CURVED_PIPELINE": (3, 6), "CURVED_PIPELINE": (3, 6), "S_CURVE_PIPELINE": (3, 6),
        "PROCESS_CIRCULAR_CYCLE": (3, 6), "CIRCULAR_CYCLE": (3, 6), "PDCA_CYCLE": (3, 6),
        "PROCESS_INTERLOCKING_GEARS": (3, 5), "INTERLOCKING_GEARS": (3, 5), "GEARS_MECHANISM": (3, 5),
        "PROCESS_FISHBONE_ISHIKAWA": (3, 6), "FISHBONE_ISHIKAWA": (3, 6), "ISHIKAWA_DIAGRAM": (3, 6),
        "PROCESS_DECISION_FLOW": (3, 6), "DECISION_FLOW": (3, 6), "DECISION_TREE": (3, 6),
        "PROCESS_SWIMLANE_TRACKS": (2, 5), "SWIMLANE_TRACKS": (2, 5),
        "PROCESS_ASCENDING_STAIRS": (3, 6), "ASCENDING_STAIRS": (3, 6), "STAIRCASE_PROGRESSION": (3, 6),
        "PROCESS_TIMELINE_FLAG_RIBBON": (3, 6), "TIMELINE_FLAG_RIBBON": (3, 6), "FLAG_RIBBON": (3, 6),
        "PROCESS_VERTICAL_SPINE": (3, 6), "VERTICAL_SPINE": (3, 6), "VERTICAL_TIMELINE": (3, 6),
        "PROCESS_GANTT_ROADMAP": (3, 6), "GANTT_ROADMAP": (3, 6), "PROJECT_GANTT": (3, 6),
        "PROCESS_BRIDGE_MIGRATION": (2, 4), "BRIDGE_MIGRATION": (2, 4), "AS_IS_TO_BE_BRIDGE": (2, 4),
        "PROCESS_JIGSAW_PUZZLE": (3, 6), "JIGSAW_PUZZLE": (3, 6), "PUZZLE_PIECES": (3, 6),
        "PROCESS_HONEYCOMB_CHAIN": (3, 6), "HONEYCOMB_CHAIN": (3, 6), "HEXAGON_FLOW": (3, 6),
        "PROCESS_ETL_DATA_PIPELINE": (3, 6), "ETL_DATA_PIPELINE": (3, 6), "DATA_PIPELINE_FLOW": (3, 6),
        "PROCESS_LEVEL_UP_LADDER": (3, 5), "LEVEL_UP_LADDER": (3, 5), "COMPETENCY_LADDER": (3, 5),
        "PROCESS_DOMINO_CASCADE": (3, 6), "DOMINO_CASCADE": (3, 6), "CHAIN_REACTION": (3, 6),
        "PROCESS_RADIAL_PROGRESSION": (3, 6), "RADIAL_PROGRESSION": (3, 6),
        "PROCESS_SPIRAL_GROWTH": (3, 6), "SPIRAL_GROWTH": (3, 6),
        "PROCESS_HOURGLASS_WORKFLOW": (3, 6), "HOURGLASS_WORKFLOW": (3, 6),
        "PROCESS_PARALLEL_STREAMS": (2, 5), "PARALLEL_STREAMS": (2, 5),
        "PROCESS_STAGED_GATE_PHASES": (3, 6), "STAGED_GATE_PHASES": (3, 6), "STAGE_GATE": (3, 6),
        "PROCESS_SERPENTINE_ROADMAP": (3, 6), "SERPENTINE_ROADMAP": (3, 6), "S_ROADMAP": (3, 6),
        "PROCESS_PIPELINE_FILTRATION": (3, 6), "PIPELINE_FILTRATION": (3, 6),
        "PROCESS_CONTINUOUS_IMPROVEMENT_PDCA": (3, 6), "CONTINUOUS_IMPROVEMENT_PDCA": (3, 6),

        # --- Architectures (Module 4) ---
        "ARCH_DATA_LAKEHOUSE_MEDALLION": (3, 4), "DATA_LAKEHOUSE_MEDALLION": (3, 4), "MEDALLION_LAKEHOUSE": (3, 4),
        "ARCH_RAG_LLM_PIPELINE": (3, 5), "RAG_LLM_PIPELINE": (3, 5), "RAG_PIPELINE": (3, 5),
        "ARCH_DEFENSE_IN_DEPTH": (3, 5), "DEFENSE_IN_DEPTH": (3, 5), "SECURITY_SHIELD_LAYERS": (3, 5),
        "ARCH_SYSTEM_LAYERED_STACK": (3, 5), "SYSTEM_LAYERED_STACK": (3, 5), "LAYERED_ARCHITECTURE": (3, 5),
        "ARCH_ORG_HIERARCHY_TREE": (3, 8), "ORG_HIERARCHY_TREE": (3, 8), "ORGANIZATION_CHART": (3, 8),
        "ARCH_RADIAL_MIND_MAP": (3, 8), "RADIAL_MIND_MAP": (3, 8), "MIND_MAP": (3, 8),
        "ARCH_MICROSERVICES_MESH": (3, 6), "MICROSERVICES_MESH": (3, 6), "SERVICE_MESH": (3, 6),
        "ARCH_CLOUD_HYBRID_INFRA": (3, 5), "CLOUD_HYBRID_INFRA": (3, 5), "HYBRID_CLOUD": (3, 5),
        "ARCH_BUS_BAR_MODULAR": (3, 6), "BUS_BAR_MODULAR": (3, 6), "EVENT_BUS_ARCHITECTURE": (3, 6),
        "ARCH_HEXAGONAL_PORTS": (3, 6), "HEXAGONAL_PORTS": (3, 6), "PORTS_AND_ADAPTERS": (3, 6),
        "ARCH_ECOSYSTEM_NETWORK": (3, 6), "ECOSYSTEM_NETWORK": (3, 6), "VALUE_NETWORK": (3, 6),
        "ARCH_MATRIX_ORGANIZATION": (3, 6), "MATRIX_ORGANIZATION": (3, 6), "MATRIX_ORG": (3, 6),
        "ARCH_API_GATEWAY_HUB": (3, 6), "API_GATEWAY_HUB": (3, 6), "GATEWAY_HUB": (3, 6),
        "ARCH_DATA_GOVERNANCE_MESH": (3, 6), "DATA_GOVERNANCE_MESH": (3, 6), "DATA_MESH": (3, 6),
        "ARCH_CLEAN_ONION_STACK": (3, 5), "CLEAN_ONION_STACK": (3, 5), "ONION_ARCHITECTURE": (3, 5),
        "ARCH_CONTAINER_CLUSTER_K8S": (3, 6), "CONTAINER_CLUSTER_K8S": (3, 6), "K8S_CLUSTER": (3, 6),
        "ARCH_AI_AGENT_ORCHESTRATOR": (3, 6), "AI_AGENT_ORCHESTRATOR": (3, 6), "AGENT_ORCHESTRATION": (3, 6),
        "ARCH_EVENT_DRIVEN_KAFKA": (3, 6), "EVENT_DRIVEN_KAFKA": (3, 6), "KAFKA_STREAMING": (3, 6),
        "ARCH_SERVERLESS_EVENT_FLOW": (3, 6), "SERVERLESS_EVENT_FLOW": (3, 6), "SERVERLESS_ARCHITECTURE": (3, 6),
        "ARCH_ZERO_TRUST_SECURITY": (3, 5), "ZERO_TRUST_SECURITY": (3, 5), "ZERO_TRUST": (3, 5),
        "ARCH_CI_CD_AUTOMATION": (3, 6), "CI_CD_AUTOMATION": (3, 6), "CI_CD_PIPELINE": (3, 6),
        "ARCH_HUB_SPOKE_ENTERPRISE_NETWORK": (3, 6), "HUB_SPOKE_ENTERPRISE_NETWORK": (3, 6), "ENTERPRISE_HUB_SPOKE": (3, 6),
        "ARCH_MULTI_TENANT_SAAS": (3, 5), "MULTI_TENANT_SAAS": (3, 5), "SAAS_MULTI_TENANT": (3, 5),
        "ARCH_EDGE_TO_CLOUD_IOT": (3, 6), "EDGE_TO_CLOUD_IOT": (3, 6), "IOT_EDGE_TO_CLOUD": (3, 6),
        "ARCH_MODULAR_MONOLITH": (3, 5), "MODULAR_MONOLITH": (3, 5),

        # --- Containers & Bento (Module 6) ---
        "CONTAINER_BENTO_COMPLEX": (2, 6), "BENTO_COMPLEX": (2, 6),
        "CONTAINER_BENTO_COMPLEX_4": (4, 4),
        "CONTAINER_BENTO_GRID_3X3": (4, 9), "BENTO_GRID_3X3": (4, 9),
        "CONTAINER_PILLAR_3D": (3, 3), "PILLAR_3D": (3, 3), "THREE_PILLARS": (3, 3),
        "CONTAINER_PILLAR_3_COLUMNS": (3, 3), "CONTAINER_THREE_PILLARS_CARDS": (3, 3),
        "THREE_PILLARS_CARDS": (3, 3),
        "CONTAINER_PILLAR_4_COLUMNS": (4, 4), "PILLAR_4_COLUMNS": (4, 4), "FOUR_PILLARS": (4, 4),
        "CONTAINER_BEFORE_AFTER": (2, 2), "BEFORE_AFTER": (2, 2), "CONTRAST_SPLIT": (2, 2),
        "CONTAINER_BEFORE_AFTER_SPLIT": (2, 2),
        "CONTAINER_STAT_HERO_SPLIT_60_40": (2, 4), "STAT_HERO_SPLIT_60_40": (2, 4), "STAT_SPLIT_60_40": (2, 4),
        "CONTAINER_KPI_STAT_DELTA": (2, 4), "KPI_STAT_DELTA": (2, 4),
        "CONTAINER_EXECUTIVE_QUOTE": (0, 2), "EXECUTIVE_QUOTE": (0, 2), "QUOTE_BANNER": (0, 2),
        "CONTAINER_MINIMALIST_APPLE_QUOTE": (0, 2), "MINIMALIST_APPLE_QUOTE": (0, 2), "APPLE_QUOTE": (0, 2),
        "CONTAINER_PROBLEM_SOL_3STEP": (3, 3), "PROBLEM_SOL_3STEP": (3, 3), "PROBLEM_SOLUTION_STEP": (3, 3),
        "CONTAINER_PROBLEM_SOLUTION_IMPACT": (3, 3), "PROBLEM_SOLUTION_IMPACT": (3, 3), "PROBLEM_SOL_IMPACT": (3, 3),
        "CONTAINER_TARGET_BULLSEYE": (3, 5), "TARGET_BULLSEYE": (3, 5), "BULLSEYE": (3, 5),
        "CONTAINER_BALANCE_SEESAW": (2, 2), "BALANCE_SEESAW": (2, 2), "SEESAW": (2, 2),
        "CONTAINER_GAUGE_METER_DIAL": (1, 3), "GAUGE_METER_DIAL": (1, 3), "SPEEDOMETER": (1, 3),
        "CONTAINER_GLASSMORPHIC_HERO": (1, 3), "GLASSMORPHIC_HERO": (1, 3),
        "CONTAINER_HERO_SPLIT_CARDS": (2, 4), "HERO_SPLIT_CARDS": (2, 4),
        "CONTAINER_DIAGONAL_SPLIT": (2, 4), "DIAGONAL_SPLIT": (2, 4),
        "CONTAINER_NOTIFICATION_TAGS": (2, 5), "NOTIFICATION_TAGS": (2, 5),
        "CONTAINER_CUSTOMER_JOURNEY": (3, 6), "CUSTOMER_JOURNEY": (3, 6),
        "CONTAINER_ISOMETRIC_STACK": (3, 5), "ISOMETRIC_STACK": (3, 5),
        "CONTAINER_TABBED_OVERVIEW": (3, 5), "TABBED_OVERVIEW": (3, 5),
        "CONTAINER_EXECUTIVE_DASHBOARD": (3, 6), "EXECUTIVE_DASHBOARD": (3, 6),
        "CONTAINER_CLOSING_CTA_HERO": (1, 4), "CLOSING_CTA_HERO": (1, 4), "CLOSING_CTA": (1, 4),
        "CONTAINER_DEVICE_MOCKUP_FRAME": (1, 3), "DEVICE_MOCKUP_FRAME": (1, 3), "MOCKUP_FRAME": (1, 3),
        "CONTAINER_METRIC_MARQUEE_BANNER": (3, 6), "METRIC_MARQUEE_BANNER": (3, 6), "MARQUEE_BANNER": (3, 6),
        "CONTAINER_FEATURE_HEX_CLUSTER": (3, 6), "FEATURE_HEX_CLUSTER": (3, 6), "HEX_CLUSTER": (3, 6),
        "CONTAINER_TESTIMONIAL_CAROUSEL_ROW": (2, 4), "TESTIMONIAL_CAROUSEL_ROW": (2, 4), "TESTIMONIALS_ROW": (2, 4),
    }

    # Combined Atom Rules dictionary
    ARCHETYPE_ATOM_RULES = {**BASE_ATOM_RULES, **V86_ATOM_RULES}

    VJ_TO_ARCHETYPE = {
        "HERO_TITLE": "title_hero",
        "BENTO": "CONTAINER_BENTO_COMPLEX",
        "BENTO_GRID": "CONTAINER_BENTO_GRID_3X3",
        "EDITORIAL_HERO": "split_comparison",
        "COMPARISON": "split_comparison",
        "VERSUS": "split_comparison",
        "TWO_PILLARS": "split_comparison",
        "THREE_PILLARS": "CONTAINER_PILLAR_3D",
        "FOUR_PILLARS": "CONTAINER_PILLAR_4_COLUMNS",
        "CARDS": "3_cards",
        "PROCESS": "process_flow_4",
        "ROADMAP": "PROCESS_SERPENTINE_ROADMAP",
        "TIMELINE": "PROCESS_TIMELINE_FLAG_RIBBON",
        "DATA_TABLE": "table_dense",
        "TABLE": "table_dense",
        "METRIC": "CONTAINER_KPI_STAT_DELTA",
        "METRIC_HERO": "CONTAINER_KPI_STAT_DELTA",
        "CHART_AND_INSIGHTS": "3_cards",
        "FORMULA_CARD": "split_comparison",
    }

    ARCHETYPE_TO_VJ = {
        "title_hero": "HERO_TITLE",
        "split_comparison": "COMPARISON",
        "3_cards": "CARDS",
        "grid_2x2": "CARDS",
        "process_flow_4": "PROCESS",
        "process_flow_5": "PROCESS",
        "metric_callout_3x": "METRIC",
        "quote_callout": "EDITORIAL_HERO",
        "conclusion_cta": "EDITORIAL_HERO",
        "table_dense": "DATA_TABLE"
    }

    PROCESS_KEYWORDS = [
        "quy trình", "tiến trình", "lộ trình", "giai đoạn", "bước",
        "phase", "step", "process", "timeline", "workflow", "nối tiếp",
        "vận hành", "pipeline", "vòng lặp", "chu trình"
    ]

    COMPARISON_KEYWORDS = [
        "so sánh", "đối chiếu", "trước và sau", "before and after",
        "before vs after", "versus", "vs", "ưu điểm và nhược điểm", "pros and cons",
        "tương phản", "mặt đối lập", "khác biệt", "phân biệt"
    ]

    METRIC_KEYWORDS = [
        "chỉ số", "doanh thu", "lợi nhuận", "kết quả tài chính", "tăng trưởng", "kpi", "metrics",
        "thống kê", "tỷ lệ", "tỷ trọng", "delta", "đo lường"
    ]

    FRAMEWORK_KEYWORDS = [
        "mô hình", "khung", "framework", "chiến lược", "ma trận", "swot", "pestel",
        "7s", "porter", "cột trụ", "nguyên lý", "yếu tố"
    ]

    def __init__(self):
        super().__init__(name="LayoutArchetypeStrategist", gate="Gate 4: Spatial Geometry, Typography & Motion")

    def _get_slides(self, target: Any) -> List[Dict[str, Any]]:
        if isinstance(target, list):
            return target
        if isinstance(target, dict):
            return target.get("slides", [target])
        return []

    def _get_item_count(self, s: Dict[str, Any]) -> int:
        for k in ["atoms", "cards", "content_items", "boxes", "items"]:
            items = s.get(k)
            if isinstance(items, list) and len(items) > 0:
                return len(items)
        return 0

    def _get_archetype_bounds(self, arch_name: str) -> Optional[Tuple[int, int]]:
        """Resolves atom bounds for any legacy or V8.6.0 archetype."""
        if arch_name in self.ARCHETYPE_ATOM_RULES:
            return self.ARCHETYPE_ATOM_RULES[arch_name]
        arch_upper = arch_name.upper()
        if arch_upper in self.ARCHETYPE_ATOM_RULES:
            return self.ARCHETYPE_ATOM_RULES[arch_upper]
        
        # Module-based heuristic bounds from ARCHETYPES_REGISTRY
        module = ARCHETYPES_REGISTRY.get(arch_upper)
        if module == "tables" or arch_upper.startswith("TABLE_"):
            return (2, 20)
        elif module == "charts" or arch_upper.startswith("CHART_"):
            return (0, 6)
        elif module == "frameworks" or arch_upper.startswith("FRAMEWORK_"):
            return (3, 8)
        elif module == "processes" or arch_upper.startswith("PROCESS_"):
            return (3, 8)
        elif module == "architectures" or arch_upper.startswith("ARCH_"):
            return (3, 8)
        elif module == "containers" or arch_upper.startswith("CONTAINER_"):
            return (2, 6)
        return None

    def _recommend_archetype(self, count: int, text: str) -> str:
        lower_text = text.lower()
        is_process = any(k in lower_text for k in self.PROCESS_KEYWORDS)
        is_comparison = any(k in lower_text for k in self.COMPARISON_KEYWORDS)
        is_metric = any(k in lower_text for k in self.METRIC_KEYWORDS)
        is_framework = any(k in lower_text for k in self.FRAMEWORK_KEYWORDS)

        if count <= 1:
            return "quote_callout"
        elif count == 2:
            if is_comparison:
                return "split_comparison"
            if is_process:
                return "process_flow_4"
            return "split_comparison"
        elif count == 3:
            if is_process:
                return "process_flow_4"
            if is_metric:
                return "metric_callout_3x"
            if is_framework:
                return "FRAMEWORK_GOLDEN_CIRCLE"
            return "3_cards"
        elif count == 4:
            if is_process:
                return "process_flow_4"
            if is_comparison:
                return "FRAMEWORK_BLUE_OCEAN_ERRC"
            if is_framework:
                return "FRAMEWORK_MATRIX_2X2"
            return "grid_2x2"
        elif count == 5:
            if is_framework:
                return "FRAMEWORK_PORTER_5_FORCES"
            return "process_flow_5"
        elif count == 6:
            if is_framework:
                return "FRAMEWORK_PESTEL_HEX"
            if is_process:
                return "PROCESS_CIRCULAR_LOOP_6STEP"
            return "CONTAINER_BENTO_GRID_3X3"
        elif count == 7:
            return "FRAMEWORK_STEEPLE"
        elif count == 8:
            if is_process:
                return "PROCESS_DEVSECOPS_INFINITY_LOOP"
            return "CONTAINER_BENTO_GRID_3X3"
        return "table_dense"

    def audit(self, target: Any, context: Optional[Dict[str, Any]] = None) -> List[AgentFinding]:
        findings: List[AgentFinding] = []
        slides = self._get_slides(target)

        for s in slides:
            slide_id = s.get("slide_id", "unknown_slide")
            role = s.get("role", "CONTENT").upper()
            if role == "COVER":
                continue
            if s.get("illustration") or s.get("visual_job") in {"EDITORIAL_HERO", "ILLUSTRATION_SPLIT"} or s.get("chart_file") or s.get("visual_job") == "CHART_AND_INSIGHTS":
                continue

            visual_job = s.get("visual_job", "").upper()
            raw_arch = s.get("archetype")
            
            # Resolve archetype: check raw_arch, then check if visual_job is in registry, else check VJ_TO_ARCHETYPE
            if raw_arch:
                archetype = raw_arch
            elif visual_job in ARCHETYPES_REGISTRY or visual_job in self.ARCHETYPE_ATOM_RULES:
                archetype = visual_job
            else:
                archetype = self.VJ_TO_ARCHETYPE.get(visual_job, "3_cards")

            item_count = self._get_item_count(s)
            slide_text = self.extract_slide_text(s)

            # 1. Check atom/card count fit
            bounds = self._get_archetype_bounds(archetype)
            if bounds:
                min_atoms, max_atoms = bounds
                # Flexible layouts exemptions
                if visual_job in {"EDITORIAL_HERO", "BENTO", "BENTO_GRID"} and 1 <= item_count <= 3:
                    pass
                elif archetype.upper().startswith("CHART_") or visual_job == "CHART_AND_INSIGHTS":
                    pass
                elif archetype.upper().startswith("TABLE_") or visual_job == "DATA_TABLE" or s.get("table_data"):
                    pass
                elif item_count < min_atoms or item_count > max_atoms:
                    rec_arch = self._recommend_archetype(item_count, slide_text)
                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=slide_id,
                            severity=Severity.P1,
                            issue=f"Bố cục archetype '{archetype}' không tương thích với số lượng atom ({item_count} atoms)",
                            rationale=f"Layout '{archetype}' được thiết kế tối ưu cho {min_atoms}-{max_atoms} thành phần. Với {item_count} atoms sẽ tạo khoảng trống thị giác hoặc gây đè chữ.",
                            suggestion=f"Chuyển đổi sang archetype phù hợp hơn: '{rec_arch}'.",
                            evidence=f"archetype='{archetype}', count={item_count}",
                            original_value=archetype,
                            suggested_value=rec_arch
                        )
                    )
                    continue

            # 2. Check semantic mismatch
            lower_text = slide_text.lower()
            is_process = any(k in lower_text for k in self.PROCESS_KEYWORDS)
            is_comparison = any(k in lower_text for k in self.COMPARISON_KEYWORDS)

            comparison_archetypes = {
                "split_comparison", "COMPARISON", "VERSUS", "CONTAINER_BEFORE_AFTER",
                "BEFORE_AFTER", "CONTRAST_SPLIT", "CONTAINER_BEFORE_AFTER_SPLIT"
            }

            if is_process and not is_comparison and archetype in {"split_comparison", "COMPARISON", "VERSUS"}:
                rec_arch = self._recommend_archetype(item_count, slide_text)
                findings.append(
                    AgentFinding(
                        agent=self.name,
                        gate=self.gate,
                        slide_id=slide_id,
                        severity=Severity.P1,
                        issue=f"Archetype '{archetype}' không phù hợp với ngữ nghĩa quy trình/tiến trình tuần tự",
                        rationale="Nội dung diễn giải quy trình/bước tuần tự cần hiển thị theo mạch dòng chảy ngang (Process Flow) thay vì chia đôi so sánh.",
                        suggestion=f"Chuyển đổi sang archetype tiến trình: '{rec_arch}'.",
                        evidence=f"Keywords in text, archetype='{archetype}'",
                        original_value=archetype,
                        suggested_value=rec_arch
                    )
                )
            elif is_comparison and item_count == 2 and archetype not in comparison_archetypes:
                findings.append(
                    AgentFinding(
                        agent=self.name,
                        gate=self.gate,
                        slide_id=slide_id,
                        severity=Severity.P1,
                        issue=f"Nội dung mang ý nghĩa so sánh đối chiếu nhưng dùng archetype '{archetype}'",
                        rationale="Với 2 đối tượng so sánh (trước/sau, phương án A/B), 'split_comparison' tạo đối trọng thị giác trực quan rõ ràng nhất.",
                        suggestion="Chuyển đổi sang archetype 'split_comparison'.",
                        evidence=f"Comparison intent with 2 items in '{archetype}'",
                        original_value=archetype,
                        suggested_value="split_comparison"
                    )
                )

        return findings

    def auto_remediate(self, target: Any, findings: List[AgentFinding], context: Optional[Dict[str, Any]] = None) -> Any:
        remediated = copy.deepcopy(target)
        slides = self._get_slides(remediated)

        for finding in findings:
            if finding.agent == self.name and finding.suggested_value:
                for s in slides:
                    if s.get("slide_id") == finding.slide_id:
                        s["archetype"] = finding.suggested_value
                        if finding.suggested_value in self.ARCHETYPE_TO_VJ:
                            s["visual_job"] = self.ARCHETYPE_TO_VJ[finding.suggested_value]

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            return remediated
        return slides

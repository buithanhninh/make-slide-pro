"""
scripts/macc_council/__init__.py
MACC-QA V8.0: 16-Agent Omniscient Council Framework.
Exports base models, all 16 specialized agents across 5 forensic gates, and the master MultiRoundCouncilOrchestrator.
"""

from .models import (
    Severity,
    AgentFinding,
    GateReport,
    CouncilAuditReport
)
from .base_agent import BaseCouncilAgent

from .gate1_source_privacy import SourceFidelityFactChecker, CompliancePrivacyGuardian
from .gate2_macro_narrative import NarrativeArcDirector, CrossSlideConsistencyAuditor
from .gate3_micro_pedagogy import (
    DomainPedagogyScholar,
    MathematicalOMMLValidator,
    NaturalLanguagePurist,
    AssertionCognitiveArbiter,
    AdversarialContentCritic,
    MasterPedagogicalRewriter
)
from .gate4_spatial_motion import (
    LayoutArchetypeStrategist,
    DataChartCartographer,
    TypographyWidowOrphanSentinel,
    VisualErgonomicsAuditor,
    MotionChoreographer
)
from .gate5_supreme_arbitration import SupremeConsensusJudge
from .orchestrator import MultiRoundCouncilOrchestrator

__all__ = [
    "Severity",
    "AgentFinding",
    "GateReport",
    "CouncilAuditReport",
    "BaseCouncilAgent",
    # Gate 1
    "SourceFidelityFactChecker",
    "CompliancePrivacyGuardian",
    # Gate 2
    "NarrativeArcDirector",
    "CrossSlideConsistencyAuditor",
    # Gate 3
    "DomainPedagogyScholar",
    "MathematicalOMMLValidator",
    "NaturalLanguagePurist",
    "AssertionCognitiveArbiter",
    "AdversarialContentCritic",
    "MasterPedagogicalRewriter",
    # Gate 4
    "LayoutArchetypeStrategist",
    "DataChartCartographer",
    "TypographyWidowOrphanSentinel",
    "VisualErgonomicsAuditor",
    "MotionChoreographer",
    # Gate 5
    "SupremeConsensusJudge",
    # Orchestrator
    "MultiRoundCouncilOrchestrator"
]

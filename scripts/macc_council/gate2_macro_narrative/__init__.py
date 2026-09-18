"""
scripts/macc_council/gate2_macro_narrative/__init__.py
Gate 2: Macro-Narrative Arc & Consistency
Exports Agent 3 (NarrativeArcDirector) and Agent 4 (CrossSlideConsistencyAuditor).
"""

from .agent03_narrative_arc import NarrativeArcDirector
from .agent04_cross_slide_consistency import CrossSlideConsistencyAuditor

__all__ = [
    "NarrativeArcDirector",
    "CrossSlideConsistencyAuditor"
]

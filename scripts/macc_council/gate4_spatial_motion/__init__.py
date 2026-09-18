"""
scripts/macc_council/gate4_spatial_motion/__init__.py
Gate 4: Spatial Geometry, Typography & Motion
Exports Agents 11 through 15.
"""

from .agent11_layout_archetype import LayoutArchetypeStrategist
from .agent12_data_chart import DataChartCartographer
from .agent13_typography_sentinel import TypographyWidowOrphanSentinel
from .agent14_visual_ergonomics import VisualErgonomicsAuditor
from .agent15_motion_choreographer import MotionChoreographer

__all__ = [
    "LayoutArchetypeStrategist",
    "DataChartCartographer",
    "TypographyWidowOrphanSentinel",
    "VisualErgonomicsAuditor",
    "MotionChoreographer"
]

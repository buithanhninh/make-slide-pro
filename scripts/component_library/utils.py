# -*- coding: utf-8 -*-
"""
Common utility functions for Make Slide Pro Vector Engines:
- Color conversion (hex_to_bgr)
- Deterministic Safe Grouping for PowerPoint COM (safe_group)
- Vector Connectors & Directional Flow Arrows (add_vector_connector)
"""
from typing import List, Any, Optional
import time

msoConnectorStraight = 1
msoConnectorElbow = 2
msoConnectorCurve = 3
msoArrowheadNone = 1
msoArrowheadTriangle = 2
msoArrowheadLengthMedium = 2
msoArrowheadWidthMedium = 2
msoLineSolid = 1
msoLineDash = 4
msoLineRoundDot = 3
msoTrue = -1
msoFalse = 0

_unique_counter = 0


def hex_to_bgr(hex_color: str) -> int:
    """Converts a hex color code (e.g. #0284C7) to PowerPoint BGR integer."""
    hex_clean = hex_color.lstrip('#')
    if len(hex_clean) != 6:
        return 0
    r = int(hex_clean[0:2], 16)
    g = int(hex_clean[2:4], 16)
    b = int(hex_clean[4:6], 16)
    return (b << 16) | (g << 8) | r


def safe_group(slide: Any, shapes: List[Any], name: Optional[str] = None) -> Any:
    """
    Safely groups a list of PowerPoint Shape objects into a single Shape group.
    Ensures all sub-shapes have globally unique Names to prevent COM Range selection collisions.
    If only 1 shape is provided, returns it directly.
    If grouping fails, returns the list of shapes or first shape gracefully.
    """
    global _unique_counter
    valid_shapes = [s for s in shapes if s is not None]
    if not valid_shapes:
        return None
    if len(valid_shapes) == 1:
        if name:
            try:
                valid_shapes[0].Name = name
            except Exception:
                pass
        return valid_shapes[0]

    names = []
    for s in valid_shapes:
        _unique_counter += 1
        s_id = getattr(s, 'Id', _unique_counter)
        unique_name = f'AtomicShape_{_unique_counter}_{s_id}_{int(time.time()*1000)%1000000}'
        try:
            s.Name = unique_name
            names.append(unique_name)
        except Exception:
            pass

    if len(names) < 2:
        return valid_shapes[0]

    try:
        grp = slide.Shapes.Range(names).Group()
        if name:
            grp.Name = name
        return grp
    except Exception:
        return valid_shapes[0]


def add_vector_connector(
    slide: Any,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    color: str = '#0284C7',
    weight: float = 2.0,
    dashed: bool = False,
    arrowhead: bool = True,
    connector_type: int = msoConnectorStraight
) -> Any:
    """Adds a native vector connector line/arrow between two coordinates."""
    try:
        conn = slide.Shapes.AddConnector(connector_type, x1, y1, x2, y2)
        conn.Line.ForeColor.RGB = hex_to_bgr(color)
        conn.Line.Weight = weight
        if dashed:
            conn.Line.DashStyle = msoLineDash
        else:
            conn.Line.DashStyle = msoLineSolid

        if arrowhead:
            conn.Line.EndArrowheadStyle = msoArrowheadTriangle
            conn.Line.EndArrowheadLength = msoArrowheadLengthMedium
            conn.Line.EndArrowheadWidth = msoArrowheadWidthMedium
        else:
            conn.Line.EndArrowheadStyle = msoArrowheadNone

        return conn
    except Exception:
        return None

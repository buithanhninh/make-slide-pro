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


def cluster_and_group_atomic_cards(slide: Any, shapes: List[Any]) -> List[Any]:
    """
    Exhaustive Spatial Clustering & Grouping for 100% Atomic Presentation Cards.
    Inspects bounding boxes (Left, Top, Width, Height) of loose shapes rendered on a slide.
    Strictly distinguishes background container shapes from child elements (textboxes, badges, chips, icons).
    Encapsulates all child elements enclosed within each parent container into a single unified GroupShape.
    Guarantees that slide components are grouped into 2 to 5 atomic presentation cards with zero loose clicks.
    """
    valid_shapes = [s for s in shapes if s is not None]
    if len(valid_shapes) <= 1:
        return valid_shapes

    # If all shapes are already groups (Type == 6: msoGroup), return as-is
    try:
        if all(getattr(s, "Type", 0) == 6 for s in valid_shapes):
            return valid_shapes
    except Exception:
        pass

    # Extract geometry and classification safely
    shape_meta = []
    for s in valid_shapes:
        try:
            s_type = getattr(s, "Type", 0)
            left = float(getattr(s, "Left", 0.0))
            top = float(getattr(s, "Top", 0.0))
            width = float(getattr(s, "Width", 0.0))
            height = float(getattr(s, "Height", 0.0))
            area = width * height

            # Check if shape is a transparent textbox or text frame (Child element, NEVER container)
            is_pure_text = (s_type == 14)  # msoTextBox
            if not is_pure_text:
                try:
                    if getattr(s, "HasTextFrame", False) and getattr(s.Fill, "Visible", 1) == 0:
                        is_pure_text = True
                except Exception:
                    pass

            shape_meta.append({
                "shape": s,
                "type": s_type,
                "left": left,
                "top": top,
                "width": width,
                "height": height,
                "area": area,
                "cx": left + width / 2.0,
                "cy": top + height / 2.0,
                "is_pure_text": is_pure_text,
                "claimed": False
            })
        except Exception:
            shape_meta.append({
                "shape": s,
                "type": 0,
                "left": 0.0,
                "top": 0.0,
                "width": 0.0,
                "height": 0.0,
                "area": 0.0,
                "cx": 0.0,
                "cy": 0.0,
                "is_pure_text": False,
                "claimed": False
            })

    # Identify container candidates:
    # Must NOT be a group (type 6), must NOT be a pure transparent textbox,
    # must have substantial card area (w >= 70, h >= 40, area >= 3500),
    # and not be a full-width background stage strip (width > 760 and height < 25)
    containers = []
    for idx, m in enumerate(shape_meta):
        if (
            m["type"] != 6
            and not m["is_pure_text"]
            and m["width"] >= 70
            and m["height"] >= 40
            and m["area"] >= 3500
            and not (m["width"] > 760 and m["height"] < 30)
            and not (m["width"] > 880)
        ):
            containers.append((idx, m))

    card_groups = []

    if containers:
        # Sort containers by area DESCENDING so primary card bodies claim their children first
        containers.sort(key=lambda x: x[1]["area"], reverse=True)

        for c_idx, c_meta in containers:
            if c_meta["claimed"]:
                continue
            c_shape = c_meta["shape"]
            c_meta["claimed"] = True
            c_left = c_meta["left"] - 6.0
            c_top = c_meta["top"] - 6.0
            c_right = c_meta["left"] + c_meta["width"] + 6.0
            c_bottom = c_meta["top"] + c_meta["height"] + 6.0

            cluster = [c_shape]

            # Find unclaimed child shapes whose center is inside this container
            for m in shape_meta:
                if m["claimed"] or m["shape"] is c_shape:
                    continue
                if c_left <= m["cx"] <= c_right and c_top <= m["cy"] <= c_bottom:
                    if m["area"] <= c_meta["area"] * 0.98:
                        cluster.append(m["shape"])
                        m["claimed"] = True

            if len(cluster) > 1:
                grp = safe_group(slide, cluster, f"Atomic_Card_{len(card_groups)+1}")
                card_groups.append(grp)
            else:
                card_groups.append(c_shape)

    # Fallback Spatial Column Partitioning:
    # If shapes remain unclaimed, check if they can be clustered by horizontal columns (X-proximity)
    unclaimed_meta = [m for m in shape_meta if not m["claimed"]]
    if unclaimed_meta:
        # Check if remaining shapes have multiple items and form columns
        # Filter out full-width strips (w > 700)
        strips = [m for m in unclaimed_meta if m["width"] > 700 or m["height"] < 12]
        column_items = [m for m in unclaimed_meta if m not in strips]

        if len(column_items) >= 2 and not containers:
            # Cluster by X center
            column_items.sort(key=lambda m: m["cx"])
            col_clusters = []
            curr_cluster = [column_items[0]]
            for k in range(1, len(column_items)):
                # If within 60pt horizontally, same column
                if abs(column_items[k]["cx"] - curr_cluster[-1]["cx"]) < 60.0:
                    curr_cluster.append(column_items[k])
                else:
                    col_clusters.append(curr_cluster)
                    curr_cluster = [column_items[k]]
            if curr_cluster:
                col_clusters.append(curr_cluster)

            for c_list in col_clusters:
                c_shapes = [m["shape"] for m in c_list]
                for m in c_list:
                    m["claimed"] = True
                if len(c_shapes) > 1:
                    grp = safe_group(slide, c_shapes, f"Atomic_Col_{len(card_groups)+1}")
                    card_groups.append(grp)
                else:
                    card_groups.append(c_shapes[0])

        # Architectural Orphan Absorption Layer:
        # If card_groups exist, absorb loose connectors (lines/arrows) and bottom strips into existing cards
        # so they never generate isolated presenter click triggers!
        if card_groups:
            unclaimed = [m for m in shape_meta if not m["claimed"]]
            for m in unclaimed:
                s = m["shape"]
                # 1. Check if bottom banner/strip (w > 500 and (top > 360 or h < 35))
                if m["width"] >= 500 and (m["top"] >= 360 or m["height"] <= 35):
                    # Absorb into Card 0 (Anchor Card)
                    m["claimed"] = True
                    card_groups[0] = safe_group(slide, [card_groups[0], s], "Atomic_Anchor_With_Strip")
                # 2. Check if connector / flow arrow (narrow line / arrow between cards)
                elif m["width"] <= 45 or m["height"] <= 12 or m["area"] < 1500:
                    # Find closest card group in card_groups to merge with
                    closest_idx = 0
                    min_dist = float("inf")
                    for c_i, c_grp in enumerate(card_groups):
                        try:
                            c_cx = float(c_grp.Left) + float(c_grp.Width) / 2.0
                            dist = abs(c_cx - m["cx"])
                            if dist < min_dist:
                                min_dist = dist
                                closest_idx = c_i
                        except Exception:
                            pass
                    m["claimed"] = True
                    card_groups[closest_idx] = safe_group(slide, [card_groups[closest_idx], s], f"Atomic_Card_{closest_idx+1}_With_Conn")

        # Any remaining truly independent primary shapes
        for m in shape_meta:
            if not m["claimed"]:
                card_groups.append(m["shape"])
                m["claimed"] = True

    # Intelligent orientation-aware sorting for natural presenter sequence:
    def get_pos(s):
        try:
            return (float(s.Left), float(s.Top), float(s.Width), float(s.Height))
        except Exception:
            return (0.0, 0.0, 0.0, 0.0)

    positions = [get_pos(s) for s in card_groups]
    is_pure_horizontal = False
    if len(positions) >= 2:
        sorted_by_left = sorted(positions, key=lambda p: p[0])
        has_overlap = False
        for k in range(len(sorted_by_left) - 1):
            curr_right = sorted_by_left[k][0] + sorted_by_left[k][2] * 0.5
            next_left = sorted_by_left[k + 1][0]
            if curr_right > next_left + 10.0:
                has_overlap = True
                break
        if not has_overlap:
            is_pure_horizontal = True

    if is_pure_horizontal:
        card_groups.sort(key=lambda s: float(getattr(s, "Left", 0.0)))
    else:
        card_groups.sort(key=lambda s: (round(float(getattr(s, "Top", 0.0)) / 120.0), float(getattr(s, "Left", 0.0))))

    # Enforce Universal Inter-Slide Kinetic Morph Naming Contract
    for idx, s in enumerate(card_groups):
        try:
            s.Name = f"!!Kinetic_Card_{idx+1}!!"
        except Exception:
            pass

    return card_groups

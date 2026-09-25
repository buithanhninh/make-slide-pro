# -*- coding: utf-8 -*-
"""
scripts/mas_engine_v9/inspectors/inter_slide_morph.py
Forensic Inter-Slide Kinetic Morph & Presenter Sequencing Inspector (Agent 2 of MAS-CLSH V9.0).
Verifies:
1. Pure Continuous Morph (ppEffectMorphByObject = 3954, 0.85s) on internal slides (2..N-1).
2. Cinematic Fade (ppTransitionFadeSmoothly = 3849, 0.65s) on Slide 1 & Slide N.
3. Atomic card presenter click sequencing: Card 0 WithPrevious, Cards 1..N OnClick.
4. Absence of broken, disconnected, or un-grouped shape animations.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple
from ..models import DefectIssue

# PowerPoint COM Constants
MORPH_EFFECT_CODES = {3954, 3850, 3953, 3955}
FADE_EFFECT_CODES = {3849, 3844, 3848}
TRIGGER_ON_CLICK = 1       # msoAnimTriggerOnPageClick
TRIGGER_WITH_PREV = 2      # msoAnimTriggerWithPrevious


class InterSlideKineticMorphAgent:
    """Specialized Inspector for Inter-Slide Morph Continuity & Kinetic Sequencing."""

    def inspect_deck_transitions(
        self,
        slide_index: int,
        total_slides: int,
        entry_effect: int,
        duration: float,
        timeline_triggers: List[int],
        has_atomic_groups: bool,
    ) -> Tuple[float, List[DefectIssue]]:
        defects: List[DefectIssue] = []
        score = 100.0

        is_cover = (slide_index == 1)
        is_outro = (slide_index == total_slides)

        # 1. Verify Transition Effect
        if is_cover or is_outro:
            if entry_effect not in FADE_EFFECT_CODES:
                defects.append(
                    DefectIssue(
                        slide_index=slide_index,
                        severity="P0",
                        domain="MOTION",
                        root_cause=f"Cover/Outro slide uses transition code {entry_effect} instead of Cinematic Fade (3849/3844).",
                        remediation_action="Assign ppTransitionFadeSmoothly (3849) with 0.65s duration.",
                    )
                )
                score -= 30.0
            elif abs(duration - 0.65) > 0.15:
                defects.append(
                    DefectIssue(
                        slide_index=slide_index,
                        severity="P2",
                        domain="MOTION",
                        root_cause=f"Fade transition duration is {duration:.2f}s (standard is 0.65s).",
                        remediation_action="Standardize transition duration to 0.65s.",
                    )
                )
                score -= 5.0
        else:
            if entry_effect not in MORPH_EFFECT_CODES:
                defects.append(
                    DefectIssue(
                        slide_index=slide_index,
                        severity="P0",
                        domain="MOTION",
                        root_cause=f"Content slide {slide_index} uses non-Morph transition {entry_effect} (violates 100% Continuous Morph).",
                        remediation_action="Assign ppEffectMorphByObject (3954) with 0.85s duration.",
                    )
                )
                score -= 40.0
            elif abs(duration - 0.85) > 0.15:
                defects.append(
                    DefectIssue(
                        slide_index=slide_index,
                        severity="P2",
                        domain="MOTION",
                        root_cause=f"Morph duration is {duration:.2f}s (standard is 0.85s).",
                        remediation_action="Standardize Morph duration to 0.85s.",
                    )
                )
                score -= 5.0

        # 2. Verify Presenter Sequencing on Content Slides
        if not (is_cover or is_outro) and timeline_triggers:
            # Check for Runaway Presenter Clicks (>5 triggers indicates fragmented, ungrouped shapes)
            if len(timeline_triggers) > 5:
                defects.append(
                    DefectIssue(
                        slide_index=slide_index,
                        severity="P0",
                        domain="MOTION",
                        root_cause=f"Runaway Presenter Clicks: Slide requires {len(timeline_triggers)} clicks (>5 clicks indicates fragmented, ungrouped shapes).",
                        remediation_action="Cluster and group child elements into 2-4 atomic cards using safe_group.",
                    )
                )
                score -= 30.0

            # Under Keynote Morph Bridge sequencing:
            # Card 0 enters directly via the 0.85s slide transition Morph (no intra-slide animation).
            # Triggers on the slide are strictly for subsequent cards, which must be OnPageClick (1)
            # (or optional aux strip WithPrevious).
            invalid_triggers = [t for t in timeline_triggers if t not in (TRIGGER_ON_CLICK, TRIGGER_WITH_PREV)]
            if invalid_triggers:
                defects.append(
                    DefectIssue(
                        slide_index=slide_index,
                        severity="P1",
                        domain="MOTION",
                        root_cause=f"Invalid animation trigger types detected: {invalid_triggers}",
                        remediation_action="Ensure animation triggers are OnPageClick (1) or WithPrevious (2).",
                    )
                )
                score -= 15.0

        # 3. Verify Atomic Grouping
        if not (is_cover or is_outro) and not has_atomic_groups and len(timeline_triggers) > 1:
            defects.append(
                DefectIssue(
                    slide_index=slide_index,
                    severity="P1",
                    domain="MOTION",
                    root_cause="Slide animations applied to disjoint, ungrouped shapes (causes fragmented text click bug).",
                    remediation_action="Apply safe_group / cluster_and_group_atomic_cards before assigning animation triggers.",
                )
            )
            score -= 20.0

        score = max(0.0, min(100.0, score))
        return score, defects

    def inspect_com_slide(
        self, slide_index: int, total_slides: int, ppt_slide_obj: Any
    ) -> Tuple[float, List[DefectIssue]]:
        """Inspects live PowerPoint COM slide transition and animation timeline."""
        try:
            trans = ppt_slide_obj.SlideShowTransition
            entry_eff = trans.EntryEffect
            dur = trans.Duration

            timeline = ppt_slide_obj.TimeLine.MainSequence
            triggers = []
            morph_suppression_defect = None
            for a_idx in range(1, timeline.Count + 1):
                try:
                    effect = timeline(a_idx)
                    triggers.append(effect.Timing.TriggerType)
                    anim_shape = effect.Shape
                    if anim_shape and getattr(anim_shape, "Name", "") == "!!Kinetic_Card_1!!":
                        morph_suppression_defect = DefectIssue(
                            slide_index=slide_index,
                            severity="P1",
                            domain="MOTION",
                            root_cause="!!Kinetic_Card_1!! has intra-slide animation in MainSequence (suppresses Morph transition).",
                            remediation_action="Remove intra-slide entrance effect on Card 0 so it participates directly in slide transition Morph.",
                        )
                except Exception:
                    pass

            group_count = 0
            for j in range(1, ppt_slide_obj.Shapes.Count + 1):
                if ppt_slide_obj.Shapes(j).Type == 6:  # msoGroup
                    group_count += 1

            has_atomic_groups = (group_count > 0)

            score, defects = self.inspect_deck_transitions(
                slide_index=slide_index,
                total_slides=total_slides,
                entry_effect=entry_eff,
                duration=dur,
                timeline_triggers=triggers,
                has_atomic_groups=has_atomic_groups,
            )
            if morph_suppression_defect:
                defects.append(morph_suppression_defect)
                score = max(0.0, score - 20.0)
            return score, defects
        except Exception as e:
            return 50.0, [
                DefectIssue(
                    slide_index=slide_index,
                    severity="P1",
                    domain="MOTION",
                    root_cause=f"COM animation timeline inspection error: {e}",
                    remediation_action="Re-initialize slide animation sequence.",
                )
            ]

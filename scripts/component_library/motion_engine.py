# -*- coding: utf-8 -*-
"""
scripts/component_library/motion_engine.py
=========================================
Apple Keynote-Grade Kinetic Motion & Transition Engine (V8.6.0).
Choreographs slide transitions and intra-slide micro-animations with:
- Magic Morph by Object / Word
- Cinematic Ease-In-Out Smooth Fades
- Directional Kinetic Pushes and Smooth Reveals
- Staggered Waterfall Card Reveals (Delta t = 0.10s - 0.15s, SmoothStart/End)
- 100% Native PowerPoint COM, fully compliant with KineticPacingAuditor.
"""

from typing import List, Dict, Any, Optional

# COM Constants
ppTransitionNone = 0
ppTransitionFadeSmoothly = 3849
ppEffectMorphByObject = 3954
ppEffectMorphByWord = 3955
ppEffectMorphByChar = 3956
ppEffectPushLeft = 3867
ppEffectPushRight = 3868
ppEffectPushUp = 3869
ppEffectPushDown = 3870
ppEffectWipeLeft = 3875
ppEffectWipeRight = 3876
ppEffectZoomIn = 3881
ppEffectPan = 3894
ppEffectReveal = 3850

msoAnimTriggerOnPageClick = 1
msoAnimTriggerWithPrevious = 2
msoAnimTriggerAfterPrevious = 3
msoAnimEffectAppear = 1
msoAnimEffectFly = 2
msoAnimEffectFade = 10
msoAnimEffectZoom = 23
msoAnimEffectRiseUp = 63
msoAnimateLevelNone = 0
msoTrue = -1
msoFalse = 0


class AppleSlideTransitionOrchestrator:
    """
    Orchestrates slide-to-slide transitions with Apple Keynote kinetic elegance.
    Restores 100% pure spatial continuous Morph across all content slides.
    """

    @staticmethod
    def apply_transition(
        slide: Any,
        slide_idx: int,
        total_slides: int,
        spec: Dict[str, Any],
        prev_spec: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Configures the optimal entry transition on a slide."""
        trans = slide.SlideShowTransition
        role = spec.get("role", "CONTENT").upper()

        if slide_idx == 1 or role == "COVER":
            effect = ppTransitionFadeSmoothly
            duration = 0.65
            transition_name = "CINEMATIC_SMOOTH_FADE"
        elif slide_idx == total_slides or role in {"CLOSING", "OUTRO", "SUMMARY"}:
            effect = ppTransitionFadeSmoothly
            duration = 0.75
            transition_name = "CINEMATIC_SMOOTH_FADE"
        elif role in {"SECTION_HEADER", "CHAPTER_DIVIDER"}:
            effect = ppTransitionFadeSmoothly
            duration = 0.60
            transition_name = "CINEMATIC_SMOOTH_FADE"
        else:
            # 100% PURE CONTINUOUS MORPH ON ALL CONTENT SLIDES (Word & Shape Interpolation)
            effect = ppEffectMorphByWord
            duration = 0.85
            transition_name = "APPLE_MORPH_WORD"

        # Apply to COM
        try:
            trans.EntryEffect = effect
            trans.Duration = duration
            trans.AdvanceOnClick = msoTrue
            trans.AdvanceOnTime = msoFalse
        except Exception:
            try:
                trans.EntryEffect = ppTransitionFadeSmoothly
                trans.Duration = 0.60
                trans.AdvanceOnClick = msoTrue
                trans.AdvanceOnTime = msoFalse
                transition_name = "FALLBACK_SMOOTH_FADE"
            except Exception:
                pass

        return {
            "slide_idx": slide_idx,
            "transition_name": transition_name,
            "effect_code": effect,
            "duration": duration,
            "advance_on_click": True
        }


class AppleChoreographedEntranceAnimator:
    """
    Choreographs intra-slide shapes with presenter click sequencing
    or optional staggered waterfall reveals.
    """

    @staticmethod
    def animate_slide_components(
        slide: Any,
        rendered_shapes: Optional[List[Any]] = None,
        header_shapes: Optional[List[Any]] = None,
        motion_mode: str = "presenter_click"
    ) -> int:
        """
        Adds micro-animations to slide components.
        In 'presenter_click' (default):
        - Header stays static (for continuous Morph stability)
        - Card 0 (Hero / Anchor Card) enters via the Slide Transition Morph directly (NO intra-slide animation)
        - Subsequent cards (idx >= 1) enter on click (msoAnimTriggerOnPageClick)
        In 'kinetic_cascade':
        - Staggered cascade with msoAnimTriggerWithPrevious
        """
        if not hasattr(slide, "TimeLine") or not hasattr(slide.TimeLine, "MainSequence"):
            return 0

        seq = slide.TimeLine.MainSequence
        effect_count = 0
        is_click_mode = (motion_mode.lower() == "presenter_click")

        # Header and Kicker Rails ALWAYS stay static across all slides
        # This provides the permanent visual anchor for 100% Zero-Flicker Keynote Morph.
        # Phase 2: Rendered Component Shapes / Cards (100% Atomic Packaging)
        if rendered_shapes:
            try:
                from .utils import cluster_and_group_atomic_cards
                atomic_cards = cluster_and_group_atomic_cards(slide, rendered_shapes)
            except Exception:
                atomic_cards = [s for s in rendered_shapes if s is not None]

            for idx, s in enumerate(atomic_cards):
                if s is None:
                    continue

                # Enforce Canonical Inter-Slide Kinetic Morph Naming Contract
                try:
                    s.Name = f"!!Kinetic_Card_{idx+1}!!"
                except Exception:
                    pass

                if is_click_mode:
                    # KINETIC MORPH PRESENTER CONTRACT:
                    # Card 0 (Hero / Anchor Card) enters through the slide transition (Morph 0.85s) directly!
                    # Adding an intra-slide entrance effect to Card 0 causes PowerPoint to hide it
                    # during the transition and cancel Morph!
                    # Therefore, Card 0 has NO entrance animation in MainSequence.
                    if idx == 0:
                        continue

                    is_aux_strip = False
                    try:
                        if float(s.Width) > 600 and float(s.Height) < 35:
                            is_aux_strip = True
                    except Exception:
                        pass

                    if is_aux_strip:
                        trigger = msoAnimTriggerWithPrevious
                        delay = 0.10
                    else:
                        trigger = msoAnimTriggerOnPageClick
                        delay = 0.0

                    try:
                        eff = seq.AddEffect(Shape=s, effectId=msoAnimEffectFade, Level=msoAnimateLevelNone, trigger=trigger)
                        eff.Timing.Duration = 0.35
                        if delay > 0 and trigger == msoAnimTriggerWithPrevious:
                            eff.Timing.TriggerDelayTime = delay
                        eff.Timing.SmoothStart = msoTrue
                        eff.Timing.SmoothEnd = msoTrue
                        effect_count += 1
                    except Exception:
                        pass
                else:
                    # KINETIC CASCADE: Staggered waterfall entrance (0.12s, 0.32s, 0.52s...)
                    current_delay = 0.12 + (idx * 0.20)
                    try:
                        eff = seq.AddEffect(Shape=s, effectId=msoAnimEffectFade, Level=msoAnimateLevelNone, trigger=msoAnimTriggerWithPrevious)
                        eff.Timing.Duration = 0.45
                        eff.Timing.TriggerDelayTime = current_delay
                        eff.Timing.SmoothStart = msoTrue
                        eff.Timing.SmoothEnd = msoTrue
                        effect_count += 1
                    except Exception:
                        pass

        return effect_count

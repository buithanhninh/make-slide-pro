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
    """Orchestrates slide-to-slide transitions with Apple Keynote kinetic elegance."""

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
        vjob = spec.get("visual_job", "").upper()

        prev_role = (prev_spec.get("role", "") if prev_spec else "").upper()
        prev_vjob = (prev_spec.get("visual_job", "") if prev_spec else "").upper()

        effect = ppEffectMorphByObject
        duration = 0.85
        transition_name = "APPLE_MORPH_OBJECT"

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
        elif "ROADMAP" in vjob or "TIMELINE" in vjob or "JOURNEY" in vjob or "PROCESS" in vjob:
            effect = ppEffectPushLeft
            duration = 0.65
            transition_name = "DIRECTIONAL_PUSH_LEFT"
        elif "ARCH_" in vjob or "MESH" in vjob or "STACK" in vjob:
            if "ARCH_" in prev_vjob:
                effect = ppEffectMorphByObject
                duration = 0.85
                transition_name = "APPLE_MORPH_OBJECT"
            else:
                effect = ppEffectPushUp
                duration = 0.60
                transition_name = "DIRECTIONAL_PUSH_UP"
        elif "CHART" in vjob or "TABLE" in vjob or "SCORECARD" in vjob:
            effect = ppEffectReveal
            duration = 0.55
            transition_name = "SMOOTH_REVEAL"
        elif prev_spec and (spec.get("assertion_title", "")[:10] == prev_spec.get("assertion_title", "")[:10]):
            effect = ppEffectMorphByWord
            duration = 0.85
            transition_name = "APPLE_MORPH_WORD"
        else:
            effect = ppEffectMorphByObject
            duration = 0.85
            transition_name = "APPLE_MORPH_OBJECT"

        # Apply to COM
        try:
            trans.EntryEffect = effect
            trans.Duration = duration
            trans.AdvanceOnClick = msoTrue
            trans.AdvanceOnTime = msoFalse
        except Exception:
            # Fallback to smooth fade
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
    """Choreographs intra-slide shapes with staggered waterfall reveals and ease-in-out timing."""

    @staticmethod
    def animate_slide_components(
        slide: Any,
        rendered_shapes: Optional[List[Any]] = None,
        header_shapes: Optional[List[Any]] = None
    ) -> int:
        """Adds staggered micro-animations to slide components."""
        if not hasattr(slide, "TimeLine") or not hasattr(slide.TimeLine, "MainSequence"):
            return 0

        seq = slide.TimeLine.MainSequence
        effect_count = 0

        # Phase 1: Header & Kicker (if provided)
        if header_shapes:
            for s in header_shapes:
                if s is not None:
                    try:
                        eff = seq.AddEffect(Shape=s, effectId=msoAnimEffectFade, Level=msoAnimateLevelNone, trigger=msoAnimTriggerWithPrevious)
                        eff.Timing.Duration = 0.40
                        eff.Timing.TriggerDelayTime = 0.05
                        try:
                            eff.Timing.SmoothStart = msoTrue
                            eff.Timing.SmoothEnd = msoTrue
                        except Exception:
                            pass
                        effect_count += 1
                    except Exception:
                        pass

        # Phase 2: Rendered Component Shapes
        if rendered_shapes:
            delay = 0.20
            stagger_step = 0.10
            for idx, s in enumerate(rendered_shapes):
                if s is None:
                    continue
                name = getattr(s, "Name", "")
                
                # Determine animation type based on shape role
                is_badge = "Delta" in name or "Badge" in name or "Pill" in name or "Flag" in name or "Tag" in name
                is_background = "Bg" in name or "Card_Bg" in name or "Container" in name
                
                anim_effect = msoAnimEffectZoom if is_badge else msoAnimEffectFade
                duration = 0.35 if is_badge else 0.45
                current_delay = min(delay + (idx * stagger_step), 1.10)

                try:
                    eff = seq.AddEffect(Shape=s, effectId=anim_effect, Level=msoAnimateLevelNone, trigger=msoAnimTriggerWithPrevious)
                    eff.Timing.Duration = duration
                    eff.Timing.TriggerDelayTime = current_delay
                    try:
                        eff.Timing.SmoothStart = msoTrue
                        eff.Timing.SmoothEnd = msoTrue
                    except Exception:
                        pass
                    effect_count += 1
                except Exception:
                    pass

        return effect_count

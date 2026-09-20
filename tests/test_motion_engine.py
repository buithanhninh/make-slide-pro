"""
tests/test_motion_engine.py
Automated verification suite for Make Slide Pro V8.6.0 Apple Keynote Motion Engine.
Verifies AppleSlideTransitionOrchestrator and AppleChoreographedEntranceAnimator.
"""

import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from component_library.motion_engine import (
    AppleSlideTransitionOrchestrator,
    AppleChoreographedEntranceAnimator,
    ppTransitionFadeSmoothly,
    ppEffectMorphByObject,
    ppEffectMorphByWord,
    ppEffectPushLeft,
    ppEffectPushUp,
    ppEffectReveal,
    msoAnimEffectFade,
    msoAnimEffectZoom,
    msoAnimTriggerWithPrevious,
    msoAnimTriggerOnPageClick,
    msoTrue,
    msoFalse,
)


class MockSlideShowTransition:
    def __init__(self):
        self.EntryEffect = 0
        self.Duration = 0.0
        self.AdvanceOnClick = False
        self.AdvanceOnTime = True


class MockShape:
    def __init__(self, name: str):
        self.Name = name


class MockTiming:
    def __init__(self):
        self.Duration = 0.0
        self.TriggerDelayTime = 0.0
        self.SmoothStart = False
        self.SmoothEnd = False


class MockEffect:
    def __init__(self, shape: MockShape, effect_id: int, trigger: int):
        self.Shape = shape
        self.effectId = effect_id
        self.trigger = trigger
        self.Timing = MockTiming()
        self.Timing.TriggerType = trigger


class MockMainSequence:
    def __init__(self):
        self.effects = []

    @property
    def Count(self):
        return len(self.effects)

    def AddEffect(self, Shape, effectId, Level, trigger):
        eff = MockEffect(Shape, effectId, trigger)
        self.effects.append(eff)
        return eff

    def __call__(self, idx):
        return self.effects[idx - 1]


class MockTimeLine:
    def __init__(self):
        self.MainSequence = MockMainSequence()


class MockSlide:
    def __init__(self):
        self.SlideShowTransition = MockSlideShowTransition()
        self.TimeLine = MockTimeLine()


def test_transition_cover_slide():
    """Verify cover slide uses Cinematic Smooth Fade with 0.65s duration."""
    slide = MockSlide()
    res = AppleSlideTransitionOrchestrator.apply_transition(slide, 1, 10, {"role": "COVER"})
    assert res["transition_name"] == "CINEMATIC_SMOOTH_FADE"
    assert res["effect_code"] == ppTransitionFadeSmoothly
    assert res["duration"] == 0.65
    assert slide.SlideShowTransition.AdvanceOnClick == msoTrue
    assert slide.SlideShowTransition.AdvanceOnTime == msoFalse


def test_transition_closing_slide():
    """Verify closing slide uses Cinematic Smooth Fade with 0.75s duration."""
    slide = MockSlide()
    res = AppleSlideTransitionOrchestrator.apply_transition(slide, 10, 10, {"role": "CLOSING"})
    assert res["transition_name"] == "CINEMATIC_SMOOTH_FADE"
    assert res["effect_code"] == ppTransitionFadeSmoothly
    assert res["duration"] == 0.75
    assert slide.SlideShowTransition.AdvanceOnClick == msoTrue


def test_transition_roadmap_process():
    """Verify roadmap/process slides use 100% pure Apple Morph Object (3954, 0.85s) for spatial continuity."""
    slide = MockSlide()
    res = AppleSlideTransitionOrchestrator.apply_transition(
        slide, 3, 10, {"role": "CONTENT", "visual_job": "PROCESS_DEVSECOPS_INFINITY_LOOP"}
    )
    assert res["transition_name"] == "APPLE_MORPH_OBJECT"
    assert res["effect_code"] == ppEffectMorphByObject
    assert res["duration"] == 0.85


def test_transition_architecture():
    """Verify architecture slides use 100% pure Apple Morph Object (3954, 0.85s)."""
    slide = MockSlide()
    res = AppleSlideTransitionOrchestrator.apply_transition(
        slide, 4, 10, {"role": "CONTENT", "visual_job": "ARCH_DATA_LAKEHOUSE_MEDALLION"}
    )
    assert res["transition_name"] == "APPLE_MORPH_OBJECT"
    assert res["effect_code"] == ppEffectMorphByObject
    assert res["duration"] == 0.85


def test_transition_charts_and_tables():
    """Verify chart and table slides use 100% pure Apple Morph Object (3954, 0.85s)."""
    slide = MockSlide()
    res = AppleSlideTransitionOrchestrator.apply_transition(
        slide, 5, 10, {"role": "CONTENT", "visual_job": "CHART_PARETO_ANALYSIS"}
    )
    assert res["transition_name"] == "APPLE_MORPH_OBJECT"
    assert res["effect_code"] == ppEffectMorphByObject
    assert res["duration"] == 0.85


def test_transition_morph_word_matching_title():
    """Verify consecutive slides default to pure Apple Morph Object (3954, 0.85s) for seamless continuous shape flow."""
    slide = MockSlide()
    prev = {"assertion_title": "Tăng Trưởng Doanh Số Quý 3 Toàn Diện"}
    curr = {"assertion_title": "Tăng Trưởng Doanh Số Quý 4 Dự Báo", "role": "CONTENT", "visual_job": "CONTAINER_KPI_STAT_DELTA"}
    res = AppleSlideTransitionOrchestrator.apply_transition(slide, 6, 10, curr, prev)
    assert res["transition_name"] == "APPLE_MORPH_OBJECT"
    assert res["effect_code"] == ppEffectMorphByObject
    assert res["duration"] == 0.85


def test_transition_default_morph_object():
    """Verify standard content slides default to Apple Morph Object."""
    slide = MockSlide()
    curr = {"assertion_title": "Tổng Quan Chiến Lược Vận Hành", "role": "CONTENT", "visual_job": "CONTAINER_THREE_PILLARS_CARDS"}
    prev = {"assertion_title": "Lời Mở Đầu Hoàn Toàn Khác", "role": "CONTENT", "visual_job": "BENTO"}
    res = AppleSlideTransitionOrchestrator.apply_transition(slide, 2, 10, curr, prev)
    assert res["transition_name"] == "APPLE_MORPH_OBJECT"
    assert res["effect_code"] == ppEffectMorphByObject
    assert res["duration"] == 0.85


def test_choreographed_entrance_animator_timing_and_curves():
    """Verify entrance animator applies proper triggers, durations, and smooth easing."""
    slide = MockSlide()
    title = MockShape("!!Anchor_Assertion_Title!!")
    kicker = MockShape("!!Anchor_Kicker!!")
    card1 = MockShape("Card_Bg_1")
    badge1 = MockShape("Badge_Icon_1")
    card2 = MockShape("Card_Bg_2")

    # Mode 1: presenter_click (Default)
    count = AppleChoreographedEntranceAnimator.animate_slide_components(
        slide,
        rendered_shapes=[card1, badge1, card2],
        header_shapes=[title, kicker],
        motion_mode="presenter_click"
    )

    # Headers remain static to avoid Morph blinking, content cards enter on click
    assert count == 3
    seq = slide.TimeLine.MainSequence
    assert seq.Count == 3

    # Check cards have on page click trigger and smooth easing
    for i in range(1, 4):
        c = seq(i)
        assert c.effectId == msoAnimEffectFade
        assert c.Timing.Duration == 0.40
        assert c.Timing.TriggerType == msoAnimTriggerOnPageClick
        assert c.Timing.SmoothStart == msoTrue
        assert c.Timing.SmoothEnd == msoTrue

    # Mode 2: kinetic_cascade
    slide_cascade = MockSlide()
    count_cascade = AppleChoreographedEntranceAnimator.animate_slide_components(
        slide_cascade,
        rendered_shapes=[card1, badge1, card2],
        header_shapes=[title, kicker],
        motion_mode="kinetic_cascade"
    )
    assert count_cascade == 5
    seq_c = slide_cascade.TimeLine.MainSequence
    assert seq_c.Count == 5

    # Invariant: all durations must strictly be between 0.15s and 1.5s for QA compliance
    for i in range(1, seq_c.Count + 1):
        eff = seq_c(i)
        assert 0.15 <= eff.Timing.Duration <= 1.5

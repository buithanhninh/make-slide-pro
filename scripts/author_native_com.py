"""
author_native_com.py
World-Class Native Microsoft PowerPoint COM Authoring Engine for Make Slide Pro V6.2.
Builds executive presentations directly using PowerPoint COM (Office 16.0+)
with Bento Grids, Editorial AI illustrations, Lucide vector icons, 
300 DPI demographic charts, and choreographed atomic group motion sequences.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

try:
    import win32com.client
    import pythoncom
except ImportError:
    win32com = None

try:
    from component_library import (
        MasterComponentDispatcher,
        detect_optimal_archetype,
        AppleSlideTransitionOrchestrator,
        AppleChoreographedEntranceAnimator,
    )
except ImportError:
    MasterComponentDispatcher = None
    detect_optimal_archetype = None
    AppleSlideTransitionOrchestrator = None
    AppleChoreographedEntranceAnimator = None

# PowerPoint Constants
ppLayoutBlank = 12
msoShapeRectangle = 1
msoShapeOval = 9
msoShapeRoundedRectangle = 5
msoTextOrientationHorizontal = 1
ppAlignLeft = 1
ppAlignCenter = 2
ppAlignRight = 3
msoTrue = -1
msoFalse = 0
msoAnimTriggerOnPageClick = 1
msoAnimTriggerWithPrevious = 2
msoAnimEffectFade = 10
msoAnimEffectFly = 2
msoAnimDirectionBottom = 1
msoAnimateLevelNone = 0
ppTransitionFadeSmoothly = 3849
ppEffectMorphByObject = 3954
ppEffectMorphByWord = 3955
ppEffectMorphByChar = 3956

# Modern Refined Design Tokens (Points: 960 x 540 for 16:9 widescreen)
CANVAS_WIDTH = 960.0
CANVAS_HEIGHT = 540.0
MARGIN_LEFT = 48.0
MARGIN_RIGHT = 48.0
MARGIN_TOP = 36.0
MARGIN_BOTTOM = 32.0
USABLE_WIDTH = CANVAS_WIDTH - MARGIN_LEFT - MARGIN_RIGHT

DARK_TOKENS = {
    "colors": {
        "base": "#060B14",       # Dark Luxury Obsidian Canvas
        "surface": "#0B132B",    # Midnight Slate card surface
        "ink": "#FFFFFF",        # Pure white high-contrast title
        "text_heading": "#FFFFFF",
        "muted": "#CBD5E1",      # Slate 300 readable body text
        "text_muted": "#94A3B8", # Slate 400 caption / kicker
        "line": "#CBD5E1",       # Readable subtitle text
        "brand": "#0284C7",      # Slate Cyan / Primary Brand Accent
        "accent": "#10B981",     # Emerald Teal Accent
        "navy": "#060B14",       # Deep Obsidian
        "card_navy": "#0B132B",  # Executive dark card
        "white": "#FFFFFF",
        "card_border": "#1E293B",
        "highlight": "#38BDF8",
        "badge_bg": "#082F49",   # Soft Cyan Glass Tint
        "accent_bg": "#064E3B",  # Soft Emerald Tint
    },
    "fonts": {
        "primary": "Segoe UI",
        "numeric": "Bahnschrift",
    },
    "sizes": {
        "title": 28,
        "kicker": 13.5,
        "card_title": 19.0,
        "body": 16.5,
        "small": 15.0,
        "metric": 52.0,
        "footer": 11.0,
    }
}

LIGHT_TOKENS = {
    "colors": {
        "base": "#F8FAFC",       # Clean Light Canvas (Slate 50)
        "surface": "#FFFFFF",    # Pure Crisp White Card Surface
        "ink": "#0F172A",        # Slate 900 high-contrast title
        "text_heading": "#0F172A",
        "muted": "#334155",      # Slate 700 readable body text
        "text_muted": "#64748B", # Slate 500 caption / kicker
        "line": "#475569",       # Slate 600 readable subtitle text
        "brand": "#0284C7",      # Deep Sky / Sapphire Accent
        "accent": "#059669",     # Forest Emerald Accent
        "navy": "#F8FAFC",       # Light canvas
        "card_navy": "#FFFFFF",  # Pure white card
        "white": "#0F172A",      # Title ink on light
        "card_border": "#CBD5E1",# Slate 300 crisp border
        "highlight": "#0284C7",
        "badge_bg": "#E0F2FE",   # Soft Light Sky Tint
        "accent_bg": "#D1FAE5",  # Soft Light Emerald Tint
    },
    "fonts": {
        "primary": "Segoe UI",
        "numeric": "Bahnschrift",
    },
    "sizes": {
        "title": 28,
        "kicker": 13.5,
        "card_title": 19.0,
        "body": 16.5,
        "small": 15.0,
        "metric": 52.0,
        "footer": 11.0,
    }
}

TOKENS = DARK_TOKENS

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ICONS_DIR = PROJECT_ROOT / "assets" / "icons"
CHARTS_DIR = PROJECT_ROOT / "assets" / "charts"
ILLUSTRATIONS_DIR = PROJECT_ROOT / "assets" / "illustrations"


def hex_to_bgr(hex_color: str) -> int:
    h = hex_color.lstrip('#')
    if len(h) == 3:
        h = ''.join(c * 2 for c in h)
    r = int(h[0:2], 16)
    g = int(h[2:4], 16)
    b = int(h[4:6], 16)
    return r + (g * 256) + (b * 65536)


try:
    from scripts.headless_deck_author import HeadlessDeckAuthor
except ImportError:
    try:
        from headless_deck_author import HeadlessDeckAuthor
    except ImportError:
        HeadlessDeckAuthor = None

class NativeDeckAuthor:
    def __init__(self, visible: bool = False, theme: str = "DARK", motion_mode: str = "presenter_click"):
        if win32com is None:
            if HeadlessDeckAuthor is not None:
                self._fallback = HeadlessDeckAuthor(visible=visible, theme=theme, motion_mode=motion_mode)
                self.theme = theme
                return
            raise RuntimeError("win32com is not available. Please install pywin32.")
        self._fallback = None
        self.set_theme(theme)
        self.motion_mode = motion_mode.lower()
        self.motion_trigger = msoAnimTriggerOnPageClick if self.motion_mode == "presenter_click" else msoAnimTriggerWithPrevious
        self.seen_images = set()
        pythoncom.CoInitialize()
        self.app = win32com.client.DispatchEx("PowerPoint.Application")
        if visible:
            self.app.Visible = msoTrue
        self.presentation = None

    def set_theme(self, theme: str):
        self.theme = theme.upper()
        self.tokens = LIGHT_TOKENS if self.theme == "LIGHT" else DARK_TOKENS
        global TOKENS
        TOKENS = self.tokens
        if MasterComponentDispatcher is not None:
            self.dispatcher = MasterComponentDispatcher(theme=self.theme, tokens=self.tokens)
        else:
            self.dispatcher = None

    def close(self):
        if getattr(self, "_fallback", None) is not None:
            return self._fallback.close()
        if self.presentation:
            try:
                self.presentation.Close()
            except Exception:
                pass
            self.presentation = None
        if self.app:
            try:
                self.app.Quit()
            except Exception:
                pass
            self.app = None
        pythoncom.CoUninitialize()

    def create_deck(self, blueprints_path: Path, output_pptx: Path, theme: Optional[str] = None) -> Path:
        if getattr(self, "_fallback", None) is not None:
            return self._fallback.create_deck(blueprints_path, output_pptx, theme)
        if theme:
            self.set_theme(theme)

        with open(blueprints_path, "r", encoding="utf-8") as f:
            blueprints = json.load(f)

        output_pptx.parent.mkdir(parents=True, exist_ok=True)
        if output_pptx.exists():
            try:
                output_pptx.unlink()
            except Exception:
                pass

        lesson_idx = blueprints.get("lesson_index", 1)
        deck_title = blueprints.get("deck_title", "").lower()
        lesson_slug = blueprints.get("lesson_slug", "").lower()
        slides_spec = blueprints.get("slides", [])
        total_slides = len(slides_spec)

        import re
        clean_stem = re.sub(r"_(Dark|Light)$", "", output_pptx.stem, flags=re.IGNORECASE)
        clean_stem = re.sub(r" - (Dark|Light)$", "", clean_stem, flags=re.IGNORECASE)
        self.doc_slug = blueprints.get("doc_slug") or "_".join(re.sub(r"[^\w\-_]", "_", clean_stem).split())
        self.seen_images = set()

        # KMCA V9.3: 100% Native Vector Shapes & Kinetic Morph Continuity Engine

        self.presentation = self.app.Presentations.Add(WithWindow=msoTrue)
        self.presentation.PageSetup.SlideWidth = CANVAS_WIDTH
        self.presentation.PageSetup.SlideHeight = CANVAS_HEIGHT

        for s_idx, spec in enumerate(slides_spec, start=1):
            slide = self.presentation.Slides.Add(s_idx, ppLayoutBlank)
            slide.FollowMasterBackground = msoFalse
            slide.Background.Fill.Solid()
            slide.Background.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["base"])

            # Setup Slide Transition (Kinetic Continuity & Morph with Apple Motion Engine)
            role = spec.get("role", "CONTENT").upper()
            prev_spec = slides_spec[s_idx - 2] if s_idx > 1 else None
            if AppleSlideTransitionOrchestrator is not None:
                AppleSlideTransitionOrchestrator.apply_transition(
                    slide, s_idx, total_slides, spec, prev_spec
                )
            trans = slide.SlideShowTransition
            is_fade = (
                s_idx == 1 
                or s_idx == total_slides 
                or role in ("COVER", "OUTRO", "CONCLUSION", "CLOSING") 
                or spec.get("transition") == "fade"
            )
            if is_fade:
                trans.EntryEffect = ppTransitionFadeSmoothly
                trans.Duration = 0.65
            else:
                trans.EntryEffect = ppEffectMorphByWord
                trans.Duration = 0.85
            trans.AdvanceOnClick = msoTrue
            trans.AdvanceOnTime = msoFalse

            if role == "COVER":
                self._render_cover_slide(slide, spec, lesson_idx, s_idx == total_slides)
            else:
                self._render_content_slide(slide, spec, s_idx, total_slides, lesson_idx)

        if output_pptx.exists():
            try:
                output_pptx.unlink()
            except Exception:
                pass
        self.presentation.SaveAs(str(output_pptx.resolve()))
        print(f"Deck saved successfully at: {output_pptx.resolve()}")
        return output_pptx

    def _resolve_asset_dir(self, base_dir: Path) -> Path:
        doc_slug = getattr(self, "doc_slug", "")
        if not doc_slug:
            return base_dir
        p = base_dir / doc_slug
        if p.exists():
            return p
        import unicodedata
        nfkd = unicodedata.normalize('NFKD', doc_slug)
        ascii_slug = "".join([c for c in nfkd if not unicodedata.combining(c)]).replace('đ', 'd').replace('Đ', 'D')
        p_ascii = base_dir / ascii_slug
        if p_ascii.exists():
            return p_ascii
        clean_target = "".join(c.lower() for c in ascii_slug if c.isalnum())
        if base_dir.exists():
            for d in base_dir.iterdir():
                if d.is_dir():
                    d_clean = "".join(c.lower() for c in unicodedata.normalize('NFKD', d.name) if not unicodedata.combining(c) and c.isalnum())
                    if clean_target and (clean_target in d_clean or d_clean in clean_target):
                        return d
        return p

    def _resolve_image_file(self, ill_name: Optional[str], lesson_idx: int = 1) -> Optional[Path]:
        if not ill_name:
            return None
        p = Path(ill_name)
        if p.is_absolute() and p.exists():
            return p
        doc_ill_dir = self._resolve_asset_dir(ILLUSTRATIONS_DIR)
        doc_media_dir = self._resolve_asset_dir(PROJECT_ROOT / "assets" / "extracted_media")
        if doc_ill_dir.exists() and (doc_ill_dir / ill_name).exists():
            return doc_ill_dir / ill_name
        if doc_media_dir.exists() and (doc_media_dir / ill_name).exists():
            return doc_media_dir / ill_name
        if (ILLUSTRATIONS_DIR / ill_name).exists():
            return ILLUSTRATIONS_DIR / ill_name
        return None

    def _insert_icon(self, slide: Any, icon_name: str, left: float, top: float, size: float = 24.0):
        clean_name = icon_name.lower().strip()
        svg_file = ICONS_DIR / f"{clean_name}.svg"
        if not svg_file.exists():
            FALLBACKS = {
                "activity": "activity.svg",
                "calc": "calculator.svg",
                "math": "calculator.svg",
                "trend": "trending-up.svg",
                "up": "trending-up.svg",
                "down": "trending-down.svg",
                "user": "users.svg",
                "people": "users.svg",
                "target": "target.svg",
                "goal": "target.svg",
                "shield": "shield.svg",
                "security": "shield.svg",
                "book": "book-open.svg",
                "edu": "book-open.svg",
                "map": "map-pin.svg",
                "chart": "bar-chart-2.svg",
                "table": "layers.svg",
                "formula": "calculator.svg",
            }
            for k, f in FALLBACKS.items():
                if k in clean_name:
                    cand = ICONS_DIR / f
                    if cand.exists():
                        svg_file = cand
                        break
        if not svg_file.exists():
            svg_file = ICONS_DIR / "target.svg"

        if svg_file.exists():
            try:
                pic = slide.Shapes.AddPicture(str(svg_file.resolve()), False, True, left, top, size, size)
                return pic
            except Exception:
                pass
        return None

    def _create_icon_badge(self, slide: Any, icon_name: str, center_x: float, center_y: float,
                           badge_diameter: float = 32.0, icon_size: float = 20.0,
                           bg_color: Optional[str] = None) -> List[Any]:
        """Creates a circular background badge and a perfectly centered icon inside it (100% concentric)."""
        shapes = []
        c_left = center_x - (badge_diameter / 2.0)
        c_top = center_y - (badge_diameter / 2.0)
        circle = slide.Shapes.AddShape(msoShapeOval, c_left, c_top, badge_diameter, badge_diameter)
        circle.Fill.Solid()
        fill_hex = bg_color if bg_color else TOKENS["colors"]["badge_bg"]
        circle.Fill.ForeColor.RGB = hex_to_bgr(fill_hex)
        circle.Line.Visible = msoFalse
        shapes.append(circle)

        i_left = center_x - (icon_size / 2.0)
        i_top = center_y - (icon_size / 2.0)
        icon = self._insert_icon(slide, icon_name, i_left, i_top, icon_size)
        if icon:
            shapes.append(icon)
        return shapes

    def _group_and_animate(self, slide: Any, shapes: List[Any], duration: float = 0.45, 
                           trigger: Optional[int] = None, effect: int = msoAnimEffectFly,
                           delay: float = 0.0, direction: int = msoAnimDirectionBottom,
                           group_name: Optional[str] = None, is_hero: bool = False) -> Any:
        valid_shapes = [s for s in shapes if s is not None]
        if not valid_shapes:
            return None
        if len(valid_shapes) == 1:
            grp = valid_shapes[0]
        else:
            names = [s.Name for s in valid_shapes]
            grp = slide.Shapes.Range(names).Group()

        if group_name:
            try:
                grp.Name = group_name
            except Exception:
                pass

        # CRITICAL KINETIC MORPH PRESENTER CONTRACT:
        # In presenter_click mode, Card 0 (Hero / Anchor Card) enters directly via the 0.85s
        # slide transition Morph. Adding an intra-slide entrance effect suppresses Morph.
        # Therefore, Card 0 has NO entrance animation in MainSequence.
        if (is_hero or (group_name and ("Hero" in group_name or group_name == "!!Kinetic_Card_1!!"))) and self.motion_mode == "presenter_click":
            try:
                grp.Name = "!!Kinetic_Card_1!!"
            except Exception:
                pass
            return grp

        eff_trigger = self.motion_trigger if trigger is None else trigger
        anim = slide.TimeLine.MainSequence.AddEffect(grp, effect, msoAnimateLevelNone, eff_trigger)
        anim.Timing.Duration = duration
        if delay > 0 and eff_trigger == msoAnimTriggerWithPrevious:
            try:
                anim.Timing.TriggerDelayTime = delay
            except Exception:
                pass
        if effect == msoAnimEffectFly:
            try:
                anim.EffectParameters.Direction = direction
            except Exception:
                pass
        anim.Timing.SmoothStart = msoTrue
        anim.Timing.SmoothEnd = msoTrue
        return grp

    def _render_cover_slide(self, slide: Any, spec: Dict[str, Any], lesson_idx: int, is_summary: bool = False):
        title_text = spec.get("assertion_title", spec.get("deck_title", "BÀI GIẢNG CHUYÊN ĐỀ"))
        subtitle_text = spec.get("primary_claim", "")
        section_text = spec.get("section", "CHUYÊN ĐỀ ĐÀO TẠO").upper()

        slide.FollowMasterBackground = msoFalse
        slide.Background.Fill.Solid()
        slide.Background.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["navy"])

        doc_slug = getattr(self, "doc_slug", "")
        ill_name = spec.get("illustration") or spec.get("image") or spec.get("image_path")
        ill_file = self._resolve_image_file(ill_name, lesson_idx)
        if not ill_file and lesson_idx in [1, 2, 3, 4, 5, 6] and ("bai_" in doc_slug.lower() or "bài" in doc_slug.lower()):
            cand = ILLUSTRATIONS_DIR / f"illustration_bai_{lesson_idx}.jpg"
            if cand.exists():
                ill_file = cand
        if not ill_file:
            doc_ill_dir = self._resolve_asset_dir(ILLUSTRATIONS_DIR)
            if (doc_ill_dir / "cover_hero.png").exists():
                ill_file = doc_ill_dir / "cover_hero.png"
            elif (doc_ill_dir / "cover_hero.jpg").exists():
                ill_file = doc_ill_dir / "cover_hero.jpg"

        has_illustration = (ill_file is not None and ill_file.exists()) and not is_summary
        if has_illustration:
            self.seen_images.add(str(ill_file.resolve()).lower())

        if has_illustration:
            left_w = USABLE_WIDTH * 0.48
            right_left = MARGIN_LEFT + left_w + 24.0
            right_w = USABLE_WIDTH - left_w - 24.0
            img_h = round(right_w / (1376.0 / 768.0), 1)
            img_top = 105.0

            # Accent Bar
            bar = slide.Shapes.AddShape(msoShapeRectangle, MARGIN_LEFT, MARGIN_TOP + 30, 48, 5)
            bar.Fill.Solid()
            bar.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["brand"])
            bar.Line.Visible = msoFalse

            # Section Kicker
            sec_box = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, MARGIN_LEFT, MARGIN_TOP + 46, left_w, 24)
            sec_box.Name = "!!Anchor_Kicker_Rail!!"
            st = sec_box.TextFrame.TextRange
            st.Text = f"CHƯƠNG TRÌNH ĐÀO TẠO DÂN SỐ HỌC  •  {section_text}"
            st.Font.Name = TOKENS["fonts"]["primary"]
            st.Font.Size = TOKENS["sizes"]["kicker"]
            st.Font.Bold = msoTrue
            st.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["accent"])

            # Title
            title_font_size = 28 if len(title_text) > 50 else (30 if len(title_text) > 35 else 34)
            title_box = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, MARGIN_LEFT, MARGIN_TOP + 78, left_w, 120)
            tt = title_box.TextFrame.TextRange
            tt.Text = title_text
            tt.Font.Name = TOKENS["fonts"]["primary"]
            tt.Font.Size = title_font_size
            tt.Font.Bold = msoTrue
            tt.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["white"])
            title_box.TextFrame.WordWrap = msoTrue
            title_box.TextFrame.MarginLeft = 0
            title_box.TextFrame.MarginTop = 0
            title_box.TextFrame.MarginRight = 0

            # Subtitle
            if subtitle_text:
                est_lines = max(1, len(title_text) // 22 + 1)
                est_title_h = est_lines * (title_font_size * 1.25)
                sub_top = max(MARGIN_TOP + 215, MARGIN_TOP + 78 + est_title_h + 16)
                sub_box = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, MARGIN_LEFT, sub_top, left_w, 100)
                sub_t = sub_box.TextFrame.TextRange
                sub_t.Text = subtitle_text
                sub_t.Font.Name = TOKENS["fonts"]["primary"]
                sub_t.Font.Size = 15
                sub_t.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["line"])
                sub_box.TextFrame.WordWrap = msoTrue
                sub_box.TextFrame.MarginLeft = 0
                sub_box.TextFrame.MarginTop = 0

            # Right Editorial Illustration: Exact 16:9 native aspect ratio, direct rounded corners & brand border (0px mismatch)
            pic = slide.Shapes.AddPicture(str(ill_file.resolve()), False, True, right_left, img_top, right_w, img_h)
            pic.Name = "!!Stage_Hero_Container!!"
            try:
                pic.AutoShapeType = msoShapeRoundedRectangle
                pic.Line.Visible = msoTrue
                pic.Line.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["brand"])
                pic.Line.Weight = 1.5
            except Exception:
                pass

            self._group_and_animate(slide, [pic], duration=0.6, trigger=msoAnimTriggerWithPrevious, effect=msoAnimEffectFade, group_name="!!Stage_Hero_Container!!")

        else:
            # Full Dark Cover Layout
            dec1 = slide.Shapes.AddShape(msoShapeOval, CANVAS_WIDTH - MARGIN_RIGHT - 240, 24, 240, 240)
            dec1.Name = "Deco_Accent_1"
            dec1.Fill.Solid()
            dec1.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["badge_bg"])
            dec1.Line.Visible = msoFalse

            dec2 = slide.Shapes.AddShape(msoShapeRectangle, CANVAS_WIDTH - MARGIN_RIGHT - 180, CANVAS_HEIGHT - MARGIN_BOTTOM - 180, 180, 180)
            dec2.Name = "Deco_Accent_2"
            dec2.Fill.Solid()
            dec2.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["accent_bg"])
            dec2.Line.Visible = msoFalse

            bar = slide.Shapes.AddShape(msoShapeRectangle, MARGIN_LEFT, MARGIN_TOP + 40, 48, 5)
            bar.Fill.Solid()
            bar.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["brand"])
            bar.Line.Visible = msoFalse

            sec_box = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, MARGIN_LEFT, MARGIN_TOP + 56, USABLE_WIDTH, 24)
            sec_box.Name = "!!Anchor_Kicker_Rail!!"
            st = sec_box.TextFrame.TextRange
            st.Text = f"CHƯƠNG TRÌNH ĐÀO TẠO DÂN SỐ HỌC  •  {section_text}"
            st.Font.Name = TOKENS["fonts"]["primary"]
            st.Font.Size = TOKENS["sizes"]["kicker"]
            st.Font.Bold = msoTrue
            st.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["accent"])

            title_box = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, MARGIN_LEFT, MARGIN_TOP + 90, USABLE_WIDTH * 0.90, 120)
            tt = title_box.TextFrame.TextRange
            tt.Text = title_text
            tt.Font.Name = TOKENS["fonts"]["primary"]
            tt.Font.Size = 36
            tt.Font.Bold = msoTrue
            tt.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["white"])
            title_box.TextFrame.WordWrap = msoTrue

            if subtitle_text:
                sub_box = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, MARGIN_LEFT, MARGIN_TOP + 230, USABLE_WIDTH * 0.85, 100)
                sub_t = sub_box.TextFrame.TextRange
                sub_t.Text = subtitle_text
                sub_t.Font.Name = TOKENS["fonts"]["primary"]
                sub_t.Font.Size = 18
                sub_t.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["line"])
                sub_box.TextFrame.WordWrap = msoTrue

    def _render_content_slide(self, slide: Any, spec: Dict[str, Any], slide_num: int, total_slides: int, lesson_idx: int):
        section_text = spec.get("section", "CHUYÊN ĐỀ").upper()
        title_text = spec.get("assertion_title", spec.get("title", ""))
        footer_source = spec.get("source_footer", "Nguồn: Tài liệu chuẩn hóa bài giảng")
        visual_job = spec.get("visual_job", "CARDS").upper()
        atoms = spec.get("atoms", spec.get("source_atoms", []))
        chart_type = spec.get("chart_type")

        # Header Rail (Visual Anchors for Zero-Flicker Morph)
        kicker_box = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, MARGIN_LEFT, MARGIN_TOP, USABLE_WIDTH - 80, 20)
        kicker_box.Name = "!!Anchor_Kicker_Rail!!"
        kt = kicker_box.TextFrame.TextRange
        kt.Text = f"{section_text}  •  TRỌNG TÂM"
        kt.Font.Name = TOKENS["fonts"]["primary"]
        kt.Font.Size = TOKENS["sizes"]["kicker"]
        kt.Font.Bold = msoTrue
        kt.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["brand"])

        num_box = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, CANVAS_WIDTH - MARGIN_RIGHT - 60, MARGIN_TOP, 60, 20)
        num_box.Name = "!!Anchor_Slide_Tracker!!"
        nt = num_box.TextFrame.TextRange
        nt.Text = f"{slide_num:02d} / {total_slides:02d}"
        nt.Font.Name = TOKENS["fonts"]["numeric"]
        nt.Font.Size = TOKENS["sizes"]["kicker"]
        nt.Font.Bold = msoTrue
        nt.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["muted"])
        num_box.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignRight

        title_len = len(title_text)
        is_long_title = (title_len > 42 or len(title_text.split()) > 7)
        title_font_size = 24 if is_long_title else 28
        title_box_height = 58.0 if is_long_title else 38.0

        title_box = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, MARGIN_LEFT, MARGIN_TOP + 20, USABLE_WIDTH, title_box_height)
        title_box.Name = "!!Anchor_Assertion_Title!!"
        tt = title_box.TextFrame.TextRange
        tt.Text = title_text
        tt.Font.Name = TOKENS["fonts"]["primary"]
        tt.Font.Size = title_font_size
        tt.Font.Bold = msoTrue
        tt.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["ink"])
        title_box.TextFrame.WordWrap = msoTrue
        title_box.TextFrame.MarginTop = 0
        title_box.TextFrame.MarginBottom = 0

        content_top = MARGIN_TOP + 20 + title_box_height + 18.0
        content_height = CANVAS_HEIGHT - content_top - MARGIN_BOTTOM - 20.0

        # Dispatch
        has_table_data = bool(spec.get("table_data") and spec["table_data"].get("headers"))
        has_chart = bool(spec.get("chart_file") or chart_type or visual_job == "CHART_AND_INSIGHTS")

        # Strict Image Resolution & Per-Deck Deduplication Gate (for non-chart slides)
        if not has_chart:
            ill_name = spec.get("illustration") or spec.get("image") or spec.get("image_path")
            ill_file = self._resolve_image_file(ill_name, lesson_idx) if ill_name else None
            if ill_file:
                norm_p = str(ill_file.resolve()).lower()
                if norm_p in self.seen_images:
                    # Deduplication: Already used earlier in this deck!
                    ill_file = None
                    spec.pop("illustration", None)
                    spec.pop("image_path", None)
                    spec.pop("image", None)
                else:
                    self.seen_images.add(norm_p)
            has_illustration = (ill_file is not None and ill_file.exists())
        else:
            has_illustration = False
            ill_file = None

        if not has_chart and not has_illustration and visual_job in {"EDITORIAL_HERO", "ILLUSTRATION_SPLIT"}:
            cnt = len(atoms)
            if cnt == 2:
                visual_job = "CONTAINER_HERO_SPLIT_CARDS"
            elif cnt == 3:
                visual_job = "CONTAINER_THREE_PILLARS_CARDS"
            elif cnt == 4:
                visual_job = "CONTAINER_PILLAR_4_COLUMNS"
            elif cnt >= 5:
                visual_job = "CONTAINER_BENTO_COMPLEX"
            else:
                visual_job = "CONTAINER_THREE_PILLARS_CARDS"

        rendered_shapes = None

        if has_chart:
            self._render_chart_and_insights_layout(slide, spec, atoms, content_top, content_height)
        elif has_illustration:
            self._render_editorial_hero_layout(slide, spec, atoms, content_top, content_height, lesson_idx, pre_resolved_file=ill_file)
        elif hasattr(self, "dispatcher") and self.dispatcher:
            resolved_archetype = None
            if self.dispatcher.can_handle(visual_job):
                resolved_archetype = visual_job
            elif has_table_data:
                resolved_archetype = detect_optimal_archetype(spec) if detect_optimal_archetype else "TABLE_METRIC_MATRIX"
            elif spec.get("chart_data"):
                resolved_archetype = detect_optimal_archetype(spec) if detect_optimal_archetype else "CHART_COLUMN_CLUSTERED"

            if resolved_archetype and self.dispatcher.can_handle(resolved_archetype):
                rendered_shapes = self.dispatcher.render(slide, spec, resolved_archetype, MARGIN_LEFT, content_top, USABLE_WIDTH, content_height)

        if rendered_shapes is not None and len(rendered_shapes) > 0:
            # Successfully rendered by Master Component Library
            try:
                from scripts.component_library.utils import cluster_and_group_atomic_cards
                active_shapes = cluster_and_group_atomic_cards(slide, rendered_shapes)
            except Exception:
                active_shapes = rendered_shapes

            # Apple Keynote-Grade Choreographed Micro-Animations (Atomic Presenter Sequencing)
            if AppleChoreographedEntranceAnimator is not None:
                AppleChoreographedEntranceAnimator.animate_slide_components(
                    slide,
                    rendered_shapes=active_shapes,
                    header_shapes=[title_box, kicker_box],
                    motion_mode=self.motion_mode
                )
        elif not has_illustration and not has_chart:
            if has_table_data or visual_job in {"DATA_TABLE", "TABLE_MATRIX", "TABLE", "TABLE_MULTI_ROW_DYNAMIC"}:
                self._render_data_table_layout(slide, spec, atoms, content_top, content_height)
            elif visual_job in {"FORMULA_CARD", "FORMULA_HERO", "FORMULA", "MATH_FORMULA"}:
                self._render_formula_hero_layout(slide, spec, atoms, content_top, content_height)
            elif "BENTO" in visual_job:
                self._render_bento_grid_layout(slide, spec, atoms, content_top, content_height)
            elif "PROCESS" in visual_job or visual_job in {"PROCESS_STEPS_HORIZONTAL", "PROCESS_DEVSECOPS_PIPELINE", "ROADMAP", "TIMELINE", "STEPS"}:
                self._render_process_layout(slide, atoms, content_top, content_height)
            elif visual_job in {"COMPARISON", "VERSUS", "TWO_PILLARS"}:
                self._render_comparison_layout(slide, atoms, content_top, content_height)
            elif visual_job in {"METRIC", "METRIC_HERO"}:
                self._render_metric_layout(slide, spec, atoms, content_top, content_height)
            else:
                self._render_cards_layout(slide, atoms, content_top, content_height)

        # Footer (Visual Anchor)
        if footer_source:
            footer_box = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, MARGIN_LEFT, CANVAS_HEIGHT - MARGIN_BOTTOM - 14, USABLE_WIDTH, 18)
            footer_box.Name = "!!Anchor_Source_Footer!!"
            ft = footer_box.TextFrame.TextRange
            ft.Text = footer_source
            ft.Font.Name = TOKENS["fonts"]["primary"]
            ft.Font.Size = TOKENS["sizes"]["footer"]
            ft.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["muted"])

    def _render_bento_grid_layout(self, slide: Any, spec: Dict[str, Any], atoms: List[Any], top: float, height: float):
        hero_atom = atoms[0] if atoms else {"title": "Trọng Tâm Bài Học", "text": spec.get("primary_claim", ""), "icon": "target"}
        sub_atoms = atoms[1:3] if len(atoms) > 1 else [{"title": "Ý Nghĩa", "text": "Phân tích sâu sắc các tác động then chốt.", "icon": "activity"}]

        hero_w = USABLE_WIDTH * 0.55
        right_left = MARGIN_LEFT + hero_w + 18.0
        right_w = USABLE_WIDTH - hero_w - 18.0

        # === 1. Left Hero Card Group ===
        hero_shapes = []
        h_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, MARGIN_LEFT, top, hero_w, height)
        h_card.Fill.Solid()
        h_card.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["surface"])
        h_card.Line.Visible = msoTrue
        h_card.Line.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["brand"])
        h_card.Line.Weight = 2.0
        hero_shapes.append(h_card)

        # Hero Pill Badge
        h_pill = slide.Shapes.AddShape(msoShapeRoundedRectangle, MARGIN_LEFT + 20, top + 18, 120, 22)
        h_pill.Fill.Solid()
        h_pill.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["badge_bg"])
        h_pill.Line.Visible = msoFalse
        pt = h_pill.TextFrame.TextRange
        pt.Text = "TRỌNG TÂM CỐT LÕI"
        pt.Font.Name = TOKENS["fonts"]["primary"]
        pt.Font.Size = 13.5
        pt.Font.Bold = msoTrue
        pt.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["brand"])
        h_pill.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
        hero_shapes.append(h_pill)

        # Hero Icon Badge (100% concentric)
        hero_icon_name = hero_atom.get("icon", "target") if isinstance(hero_atom, dict) else "target"
        hero_shapes.extend(self._create_icon_badge(slide, hero_icon_name, MARGIN_LEFT + 39, top + 67, 38, 26))

        # Hero Text
        h_title = hero_atom.get("title", "Luận Điểm Trọng Yếu") if isinstance(hero_atom, dict) else "Trọng Tâm"
        h_body = hero_atom.get("text", str(hero_atom)) if isinstance(hero_atom, dict) else str(hero_atom)

        tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, MARGIN_LEFT + 20, top + 94, hero_w - 40, height - 108)
        tf = tb.TextFrame
        tf.WordWrap = msoTrue
        tf.MarginLeft = 0

        p1 = tf.TextRange.Paragraphs(1)
        p1.Text = h_title + "\n"
        p1.Font.Name = TOKENS["fonts"]["primary"]
        p1.Font.Size = 20
        p1.Font.Bold = msoTrue
        p1.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["ink"])
        p1.ParagraphFormat.SpaceAfter = 10

        p2 = tf.TextRange.Paragraphs(2)
        p2.Text = h_body
        p2.Font.Name = TOKENS["fonts"]["primary"]
        p2.Font.Size = 16.5
        p2.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["muted"])
        p2.ParagraphFormat.LineRuleWithin = msoTrue
        p2.ParagraphFormat.SpaceWithin = 1.3
        hero_shapes.append(tb)

        # Package Hero Group for Continuous Seamless Morph
        names = [s.Name for s in hero_shapes if s is not None]
        hero_grp = None
        if len(names) > 1:
            hero_grp = slide.Shapes.Range(names).Group()
            hero_grp.Name = "!!Kinetic_Card_1!!"
        elif len(names) == 1:
            hero_grp = hero_shapes[0]
            hero_grp.Name = "!!Kinetic_Card_1!!"
        if hero_grp is not None:
            self._group_and_animate(slide, [hero_grp], duration=0.45, group_name="!!Kinetic_Card_1!!", is_hero=True)

        # === 2. Right Stacked Cards ===
        count = len(sub_atoms)
        card_h = (height - (14.0 * (count - 1))) / count

        for i, atom in enumerate(sub_atoms):
            sub_shapes = []
            c_top = top + i * (card_h + 14.0)

            rcard = slide.Shapes.AddShape(msoShapeRoundedRectangle, right_left, c_top, right_w, card_h)
            rcard.Fill.Solid()
            rcard.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["surface"])
            rcard.Line.Visible = msoTrue
            rcard.Line.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["card_border"])
            sub_shapes.append(rcard)

            # Pill Tag
            pill = slide.Shapes.AddShape(msoShapeRoundedRectangle, right_left + 16, c_top + 14, 85, 20)
            pill.Fill.Solid()
            pill.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["badge_bg"])
            pill.Line.Visible = msoFalse
            pt = pill.TextFrame.TextRange
            is_obj = "mục tiêu" in spec.get("section", "").lower() or "mục tiêu" in spec.get("assertion_title", "").lower()
            pill_lbl = "MỤC TIÊU" if is_obj else "TRỌNG ĐIỂM"
            pt.Text = f"{pill_lbl} 0{i+1}"
            pt.Font.Name = TOKENS["fonts"]["primary"]
            pt.Font.Size = 13.0
            pt.Font.Bold = msoTrue
            pt.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["brand"])
            pill.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
            sub_shapes.append(pill)

            # Badge Circle & Icon (100% concentric)
            s_icon_name = atom.get("icon", "activity") if isinstance(atom, dict) else "activity"
            sub_shapes.extend(self._create_icon_badge(slide, s_icon_name, right_left + 32, c_top + 56, 32, 22))

            stitle = atom.get("title", f"Yếu Tố {i+1}") if isinstance(atom, dict) else f"Yếu Tố {i+1}"
            sbody = atom.get("text", str(atom)) if isinstance(atom, dict) else str(atom)

            stb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, right_left + 58, c_top + 34, right_w - 70, card_h - 42)
            stf = stb.TextFrame
            stf.WordWrap = msoTrue
            stf.MarginTop = 0

            sp1 = stf.TextRange.Paragraphs(1)
            sp1.Text = stitle + "\n"
            sp1.Font.Name = TOKENS["fonts"]["primary"]
            sp1.Font.Size = 18.5
            sp1.Font.Bold = msoTrue
            sp1.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["ink"])
            sp1.ParagraphFormat.SpaceAfter = 4

            sp2 = stf.TextRange.Paragraphs(2)
            sp2.Text = sbody
            sp2.Font.Name = TOKENS["fonts"]["primary"]
            sp2.Font.Size = 16.0
            sp2.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["muted"])
            sub_shapes.append(stb)

            # Animate Sub Card as Staggered Kinetic Cascade
            self._group_and_animate(slide, sub_shapes, duration=0.45, delay=0.12 * (i + 1), group_name=f"!!Kinetic_Card_{i+2}!!")

    def _render_editorial_hero_layout(self, slide: Any, spec: Dict[str, Any], atoms: List[Any], top: float, height: float, lesson_idx: int, pre_resolved_file: Optional[Path] = None):
        card_w = USABLE_WIDTH * 0.49
        right_left = MARGIN_LEFT + card_w + 18.0
        right_w = USABLE_WIDTH - card_w - 18.0

        ill_file = pre_resolved_file
        if ill_file is None:
            ill_name = spec.get("illustration") or spec.get("image") or spec.get("image_path")
            ill_file = self._resolve_image_file(ill_name, lesson_idx)

        # === 1. Left Image Container & Takeaway Card Group ===
        left_shapes = []
        if ill_file is not None and ill_file.exists():
            # Exact 16:9 native aspect ratio (1376x768 = 1.792), direct rounded corners and border (0px mismatch)
            img_h = round(card_w / (1376.0 / 768.0), 1)
            pic = slide.Shapes.AddPicture(str(ill_file.resolve()), False, True, MARGIN_LEFT, top, card_w, img_h)
            try:
                pic.AutoShapeType = msoShapeRoundedRectangle
                pic.Line.Visible = msoTrue
                pic.Line.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["card_border"])
                pic.Line.Weight = 1.0
            except Exception:
                pass
            left_shapes.append(pic)

            # Sleek Takeaway Highlight Card below illustration
            callout_top = top + img_h + 12.0
            callout_h = height - img_h - 12.0
            callout_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, MARGIN_LEFT, callout_top, card_w, callout_h)
            callout_card.Fill.Solid()
            callout_card.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["surface"])
            callout_card.Line.Visible = msoTrue
            callout_card.Line.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["brand"])
            callout_card.Line.Weight = 1.5
            left_shapes.append(callout_card)

            # Pill Tag for Callout
            pill = slide.Shapes.AddShape(msoShapeRoundedRectangle, MARGIN_LEFT + 14, callout_top + 10, 160, 24)
            pill.Fill.Solid()
            pill.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["badge_bg"])
            pill.Line.Visible = msoFalse
            pt = pill.TextFrame.TextRange
            pt.Text = "THÔNG ĐIỆP CỐT LÕI"
            pt.Font.Name = TOKENS["fonts"]["primary"]
            pt.Font.Size = 13.5
            pt.Font.Bold = msoTrue
            pt.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["brand"])
            pill.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
            left_shapes.append(pill)

            # Dedicated Claim Textbox (High-Contrast 16.5pt Body)
            callout_tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, MARGIN_LEFT + 14, callout_top + 40, card_w - 28, callout_h - 48)
            ctf = callout_tb.TextFrame
            ctf.WordWrap = msoTrue
            ctf.MarginLeft = 0
            ctf.MarginTop = 0
            ct = ctf.TextRange
            ct.Text = spec.get("primary_claim", "Nền tảng định lượng và lý luận cốt lõi của bài học.")
            ct.Font.Name = TOKENS["fonts"]["primary"]
            ct.Font.Size = 16.5
            ct.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["ink"])
            ct.ParagraphFormat.LineRuleWithin = msoTrue
            ct.ParagraphFormat.SpaceWithin = 1.25
            left_shapes.append(callout_tb)
        else:
            fallback_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, MARGIN_LEFT, top, card_w, height)
            fallback_card.Fill.Solid()
            fallback_card.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["surface"])
            fallback_card.Line.Visible = msoTrue
            fallback_card.Line.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["card_border"])
            left_shapes.append(fallback_card)

        # Package Left Image Container for Continuous Seamless Morph
        names = [s.Name for s in left_shapes if s is not None]
        hero_grp = None
        if len(names) > 1:
            hero_grp = slide.Shapes.Range(names).Group()
            hero_grp.Name = "!!Kinetic_Card_1!!"
        elif len(names) == 1:
            hero_grp = left_shapes[0]
            hero_grp.Name = "!!Kinetic_Card_1!!"
        if hero_grp is not None:
            self._group_and_animate(slide, [hero_grp], duration=0.45, group_name="!!Kinetic_Card_1!!", is_hero=True)

        # === 2. Right Column Insight Cards ===
        # Resilience Fallback: If atoms is empty, auto-recover from matrix_data, cards, or synthesize from primary_claim
        effective_atoms = list(atoms) if atoms else []
        if not effective_atoms:
            m_quads = spec.get("matrix_data", {}).get("quadrants", [])
            if m_quads:
                for q in m_quads:
                    effective_atoms.append({
                        "title": q.get("title", ""),
                        "text": q.get("desc", ""),
                        "icon": "shield"
                    })
            elif spec.get("cards"):
                effective_atoms = list(spec.get("cards"))
            else:
                claim = spec.get("primary_claim", "Nội dung phân tích bối cảnh và định hướng trọng tâm.")
                effective_atoms = [
                    {"title": "Định Hướng Can Thiệp", "text": claim, "icon": "trending-up"},
                    {"title": "Mục Tiêu Chuẩn Hóa", "text": "Bảo đảm đồng bộ các quy chuẩn chuyên môn và chỉ số đầu ra.", "icon": "award"},
                    {"title": "Giải Pháp Bền Vững", "text": "Kết nối chặt chẽ giữa tuyến chuyên sâu và mạng lưới cơ sở.", "icon": "shield"}
                ]

        count = max(1, min(len(effective_atoms), 2))
        card_h = (height - (16.0 * (count - 1))) / count

        for i, atom in enumerate(effective_atoms[:count]):
            card_shapes = []
            c_top = top + i * (card_h + 12.0)

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, right_left, c_top, right_w, card_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["surface"])
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["brand"] if i == 0 else TOKENS["colors"]["card_border"])
            card.Line.Weight = 1.5 if i == 0 else 1.0
            card_shapes.append(card)

            # 100% Concentric Icon Badge
            icon_name = atom.get("icon", "activity") if isinstance(atom, dict) else "activity"
            card_shapes.extend(self._create_icon_badge(slide, icon_name, right_left + 29, c_top + 29, 30, 20))

            title_t = atom.get("title", f"Phân Tích {i+1}") if isinstance(atom, dict) else f"Phân Tích {i+1}"
            body_t = atom.get("text", str(atom)) if isinstance(atom, dict) else str(atom)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, right_left + 52, c_top + 10, right_w - 62, card_h - 18)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            tf.MarginTop = 0

            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = title_t + "\n"
            p1.Font.Name = TOKENS["fonts"]["primary"]
            p1.Font.Size = 18.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["ink"])
            p1.ParagraphFormat.SpaceAfter = 4

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = body_t
            p2.Font.Name = TOKENS["fonts"]["primary"]
            p2.Font.Size = 16.0
            p2.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["muted"])
            card_shapes.append(tb)

            # Animate each insight card sequentially with staggered kinetic cascade
            self._group_and_animate(slide, card_shapes, duration=0.45, delay=0.12 * (i + 1), group_name=f"!!Kinetic_Card_{i+2}!!")

    def _render_chart_and_insights_layout(self, slide: Any, spec: Dict[str, Any], atoms: List[Any], top: float, height: float):
        theme_suffix = "_light.png" if self.theme == "LIGHT" else "_dark.png"
        doc_slug = getattr(self, "doc_slug", "")
        doc_media_dir = self._resolve_asset_dir(PROJECT_ROOT / "assets" / "extracted_media")
        chart_file_spec = spec.get("chart_file") or spec.get("image_path") or spec.get("image")
        chart_file = None
        if chart_file_spec and Path(chart_file_spec).is_absolute() and Path(chart_file_spec).exists():
            chart_file = Path(chart_file_spec)
        elif chart_file_spec and doc_media_dir.exists() and (doc_media_dir / chart_file_spec).exists():
            chart_file = doc_media_dir / chart_file_spec
        elif doc_media_dir.exists():
            # Match Biểu X in section or title
            sec_t = spec.get("section", "") + " " + spec.get("assertion_title", "")
            m = re.search(r"biểu\s*([0-9]+)", sec_t, re.IGNORECASE)
            if m:
                b_num = int(m.group(1))
                for ext in [".png", ".jpg", ".emf"]:
                    cand = doc_media_dir / f"image{b_num}{ext}"
                    if cand.exists():
                        chart_file = cand
                        break
        elif chart_file_spec and (CHARTS_DIR / chart_file_spec).exists():
            chart_file = CHARTS_DIR / chart_file_spec
        elif ("bai_" in doc_slug.lower() or "bài" in doc_slug.lower()):
            # Only for legacy Course 1
            chart_type = spec.get("chart_type", "POPULATION_PYRAMID")
            themed_chart_file = CHARTS_DIR / f"chart_{chart_type.lower()}{theme_suffix}"
            if themed_chart_file.exists():
                chart_file = themed_chart_file
            else:
                chart_file = CHARTS_DIR / f"chart_{chart_type.lower()}.png"
        else:
            chart_file = None

        chart_w = USABLE_WIDTH * 0.52
        insights_w = USABLE_WIDTH * 0.45
        gutter = USABLE_WIDTH * 0.03

        # === 1. Left Container: Native Themed Chart with Perfect Aspect Ratio ===
        chart_shapes = []
        if chart_file is not None and chart_file.exists():
            # Exact aspect ratio preservation (1408x1078 = 1.30612), direct rounded corners and border
            ideal_h = round(chart_w / (1408.0 / 1078.0), 1)
            chart_h = min(height, ideal_h)
            chart_top = top + (height - chart_h) / 2.0
            chart_pic = slide.Shapes.AddPicture(str(chart_file.resolve()), False, True, MARGIN_LEFT, chart_top, chart_w, chart_h)
            try:
                chart_pic.AutoShapeType = msoShapeRoundedRectangle
                chart_pic.Line.Visible = msoTrue
                chart_pic.Line.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["card_border"])
                chart_pic.Line.Weight = 1.0
            except Exception:
                pass
            chart_shapes.append(chart_pic)
        else:
            chart_bg = slide.Shapes.AddShape(msoShapeRoundedRectangle, MARGIN_LEFT, top, chart_w, height)
            chart_bg.Fill.Solid()
            chart_bg.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["surface"])
            chart_bg.Line.Visible = msoTrue
            chart_bg.Line.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["brand"])
            chart_bg.Line.Weight = 1.5
            chart_shapes.append(chart_bg)

            # Icon badge and metric assertion
            chart_shapes.extend(self._create_icon_badge(slide, "bar-chart-2", MARGIN_LEFT + 32, top + 36, 42, 24))
            tb_stat = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, MARGIN_LEFT + 24, top + 70, chart_w - 48, height - 90)
            tf_stat = tb_stat.TextFrame
            tf_stat.WordWrap = msoTrue
            p_s1 = tf_stat.TextRange.Paragraphs(1)
            p_s1.Text = "CHỈ SỐ THỰC CHỨNG & ĐỊNH LƯỢNG\n"
            p_s1.Font.Name = TOKENS["fonts"]["primary"]
            p_s1.Font.Size = 14.5
            p_s1.Font.Bold = msoTrue
            p_s1.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["brand"])
            p_s2 = tf_stat.TextRange.Paragraphs(2)
            p_s2.Text = spec.get("primary_claim", "Phân tích số liệu và xu hướng phát triển thực tế.")
            p_s2.Font.Name = TOKENS["fonts"]["primary"]
            p_s2.Font.Size = 17.5
            p_s2.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["white"])
            chart_shapes.append(tb_stat)

        # Package Chart Container for Continuous Seamless Morph
        names = [s.Name for s in chart_shapes if s is not None]
        chart_hero_grp = None
        if len(names) > 1:
            chart_hero_grp = slide.Shapes.Range(names).Group()
            chart_hero_grp.Name = "!!Kinetic_Card_1!!"
        elif len(names) == 1:
            chart_hero_grp = chart_shapes[0]
            chart_hero_grp.Name = "!!Kinetic_Card_1!!"
        if chart_hero_grp is not None:
            self._group_and_animate(slide, [chart_hero_grp], duration=0.45, group_name="!!Kinetic_Card_1!!", is_hero=True)

        # === 2. Right Column: Insights Cards ===
        right_left = MARGIN_LEFT + chart_w + gutter
        count = max(1, min(len(atoms), 2))
        card_h = (height - (16.0 * (count - 1))) / count

        for i, atom in enumerate(atoms[:count]):
            card_shapes = []
            c_top = top + i * (card_h + 16.0)

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, right_left, c_top, insights_w, card_h)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["surface"])
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["brand"] if i == 0 else TOKENS["colors"]["card_border"])
            card.Line.Weight = 1.5 if i == 0 else 1.0
            card_shapes.append(card)

            # 100% Concentric Icon Badge
            icon_name = atom.get("icon", "activity") if isinstance(atom, dict) else "activity"
            card_shapes.extend(self._create_icon_badge(slide, icon_name, right_left + 29, c_top + 29, 30, 20))

            title_t = atom.get("title", f"Phân Tích {i+1}") if isinstance(atom, dict) else f"Phân Tích {i+1}"
            body_t = atom.get("text", str(atom)) if isinstance(atom, dict) else str(atom)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, right_left + 52, c_top + 10, insights_w - 62, card_h - 18)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            tf.MarginTop = 0

            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = title_t + "\n"
            p1.Font.Name = TOKENS["fonts"]["primary"]
            p1.Font.Size = 18.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["ink"])
            p1.ParagraphFormat.SpaceAfter = 4

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = body_t
            p2.Font.Name = TOKENS["fonts"]["primary"]
            p2.Font.Size = 16.0
            p2.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["muted"])
            card_shapes.append(tb)

            # Animate each insight card sequentially with staggered kinetic cascade
            self._group_and_animate(slide, card_shapes, duration=0.45, delay=0.12 * (i + 1), group_name=f"!!Kinetic_Card_{i+2}!!")

    def _render_cards_layout(self, slide: Any, atoms: List[Any], top: float, height: float):
        count = max(1, min(len(atoms), 3))
        gutter = 16.0
        card_w = (USABLE_WIDTH - (gutter * (count - 1))) / count

        for i, atom in enumerate(atoms[:count]):
            card_shapes = []
            left = MARGIN_LEFT + i * (card_w + gutter)

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, card_w, height)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["surface"])
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["card_border"])
            card.Line.Weight = 1.0
            card_shapes.append(card)

            top_line = slide.Shapes.AddShape(msoShapeRectangle, left + 16, top + 16, 36, 3)
            top_line.Fill.Solid()
            top_line.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["brand"])
            top_line.Line.Visible = msoFalse
            card_shapes.append(top_line)

            # 100% Concentric Icon Badge
            icon_name = atom.get("icon", "activity") if isinstance(atom, dict) else "activity"
            card_shapes.extend(self._create_icon_badge(slide, icon_name, left + 32, top + 42, 32, 22))

            title_text = atom.get("title", f"Yếu Tố {i+1}") if isinstance(atom, dict) else f"Luận Điểm {i+1}"
            body_text = atom.get("text", str(atom)) if isinstance(atom, dict) else str(atom)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 16, top + 68, card_w - 32, height - 76)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            tf.MarginTop = 0
            tf.MarginLeft = 0

            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = title_text + "\n"
            p1.Font.Name = TOKENS["fonts"]["primary"]
            p1.Font.Size = 18
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["ink"])
            p1.ParagraphFormat.SpaceAfter = 8

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = body_text
            p2.Font.Name = TOKENS["fonts"]["primary"]
            p2.Font.Size = TOKENS["sizes"]["body"]
            p2.Font.Bold = msoFalse
            p2.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["muted"])
            p2.ParagraphFormat.LineRuleWithin = msoTrue
            p2.ParagraphFormat.SpaceWithin = 1.25
            card_shapes.append(tb)

            if i == 0:
                self._group_and_animate(slide, card_shapes, duration=0.45, group_name="!!Kinetic_Card_1!!", is_hero=True)
            else:
                self._group_and_animate(slide, card_shapes, duration=0.45, delay=0.14 * i, group_name=f"!!Kinetic_Card_{i+1}!!")

    def _render_process_layout(self, slide: Any, atoms: List[Any], top: float, height: float):
        count = max(1, min(len(atoms), 4))
        gutter = 14.0
        step_w = (USABLE_WIDTH - (gutter * (count - 1))) / count

        for i, atom in enumerate(atoms[:count]):
            step_shapes = []
            left = MARGIN_LEFT + i * (step_w + gutter)

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, step_w, height)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["surface"])
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["card_border"])
            step_shapes.append(card)

            badge = slide.Shapes.AddShape(msoShapeRectangle, left + 16, top + 16, 32, 24)
            badge.Fill.Solid()
            badge.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["brand"])
            badge.Line.Visible = msoFalse
            bt = badge.TextFrame.TextRange
            bt.Text = f"{i+1:02d}"
            bt.Font.Name = TOKENS["fonts"]["numeric"]
            bt.Font.Size = 14.0
            bt.Font.Bold = msoTrue
            bt.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["white"])
            badge.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
            step_shapes.append(badge)

            icon_name = atom.get("icon", "activity") if isinstance(atom, dict) else "activity"
            icon = self._insert_icon(slide, icon_name, left + step_w - 38, top + 16, 22)
            if icon:
                step_shapes.append(icon)

            title_text = atom.get("title", f"Bước {i+1}") if isinstance(atom, dict) else f"Giai Đoạn {i+1}"
            body_text = atom.get("text", str(atom)) if isinstance(atom, dict) else str(atom)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 16, top + 52, step_w - 32, height - 64)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue
            tf.MarginLeft = 0

            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = title_text + "\n"
            p1.Font.Name = TOKENS["fonts"]["primary"]
            p1.Font.Size = 18.5
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["ink"])
            p1.ParagraphFormat.SpaceAfter = 6

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = body_text
            p2.Font.Name = TOKENS["fonts"]["primary"]
            p2.Font.Size = 16.0
            p2.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["muted"])
            step_shapes.append(tb)

            if i == 0:
                self._group_and_animate(slide, step_shapes, duration=0.45, group_name="!!Kinetic_Card_1!!", is_hero=True)
            else:
                self._group_and_animate(slide, step_shapes, duration=0.45, delay=0.12 * i, group_name=f"!!Kinetic_Card_{i+1}!!")

    def _render_comparison_layout(self, slide: Any, atoms: List[Any], top: float, height: float):
        card_w = (USABLE_WIDTH - 24.0) / 2.0
        for i, atom in enumerate(atoms[:2]):
            pillar_shapes = []
            left = MARGIN_LEFT + i * (card_w + 24.0)

            card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, top, card_w, height)
            card.Fill.Solid()
            card.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["surface"])
            card.Line.Visible = msoTrue
            card.Line.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["brand"] if i == 1 else TOKENS["colors"]["card_border"])
            card.Line.Weight = 2.0 if i == 1 else 1.0
            pillar_shapes.append(card)

            pill = slide.Shapes.AddShape(msoShapeRoundedRectangle, left + 20, top + 18, 110, 22)
            pill.Fill.Solid()
            pill.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["accent_bg"] if i == 1 else TOKENS["colors"]["badge_bg"])
            pill.Line.Visible = msoFalse
            pt = pill.TextFrame.TextRange
            pt.Text = "TIÊU CHÍ SO SÁNH" if i == 0 else "ĐẶC TRƯNG CỐT LÕI"
            pt.Font.Name = TOKENS["fonts"]["primary"]
            pt.Font.Size = 13.0
            pt.Font.Bold = msoTrue
            pt.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["accent"] if i == 1 else TOKENS["colors"]["brand"])
            pill.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
            pillar_shapes.append(pill)

            # 100% Concentric Icon Badge
            icon_name = atom.get("icon", "scale" if i == 0 else "users") if isinstance(atom, dict) else "scale"
            pillar_shapes.extend(self._create_icon_badge(slide, icon_name, left + 38, top + 64, 36, 24))

            title_text = atom.get("title", "Phương Án A" if i == 0 else "Phương Án B") if isinstance(atom, dict) else f"Khía Cạnh {i+1}"
            body_text = atom.get("text", str(atom)) if isinstance(atom, dict) else str(atom)

            tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 20, top + 90, card_w - 40, height - 100)
            tf = tb.TextFrame
            tf.WordWrap = msoTrue

            p1 = tf.TextRange.Paragraphs(1)
            p1.Text = title_text + "\n"
            p1.Font.Name = TOKENS["fonts"]["primary"]
            p1.Font.Size = 20
            p1.Font.Bold = msoTrue
            p1.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["highlight"] if i == 1 else TOKENS["colors"]["ink"])
            p1.ParagraphFormat.SpaceAfter = 12

            p2 = tf.TextRange.Paragraphs(2)
            p2.Text = body_text
            p2.Font.Name = TOKENS["fonts"]["primary"]
            p2.Font.Size = TOKENS["sizes"]["body"]
            p2.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["muted"])
            p2.ParagraphFormat.LineRuleWithin = msoTrue
            p2.ParagraphFormat.SpaceWithin = 1.3
            pillar_shapes.append(tb)

            if i == 0:
                self._group_and_animate(slide, pillar_shapes, duration=0.45, group_name="!!Kinetic_Card_1!!", is_hero=True)
            else:
                self._group_and_animate(slide, pillar_shapes, duration=0.5, delay=0.18, group_name="!!Kinetic_Card_2!!")

    def _render_metric_layout(self, slide: Any, spec: Dict[str, Any], atoms: List[Any], top: float, height: float):
        left_w = USABLE_WIDTH * 0.42
        right_w = USABLE_WIDTH * 0.54
        gutter = USABLE_WIDTH * 0.04

        metric_val = spec.get("metric_value", "85%")
        metric_lbl = spec.get("metric_label", "Tỷ Lệ Tác Động")
        metric_ctx = spec.get("metric_context", "Đo lường trên toàn bộ tập dữ liệu nghiên cứu")

        # Hero Metric Group
        hero_shapes = []
        hero = slide.Shapes.AddShape(msoShapeRoundedRectangle, MARGIN_LEFT, top, left_w, height)
        hero.Fill.Solid()
        hero.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["surface"])
        hero.Line.Visible = msoTrue
        hero.Line.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["brand"])
        hero.Line.Weight = 2.0
        hero_shapes.append(hero)

        tb_num = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, MARGIN_LEFT + 24, top + 30, left_w - 48, 80)
        tfn = tb_num.TextFrame.TextRange
        tfn.Text = metric_val
        tfn.Font.Name = TOKENS["fonts"]["numeric"]
        tfn.Font.Size = TOKENS["sizes"]["metric"]
        tfn.Font.Bold = msoTrue
        tfn.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["brand"])
        hero_shapes.append(tb_num)

        tb_ctx = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, MARGIN_LEFT + 24, top + 115, left_w - 48, height - 130)
        tfc = tb_ctx.TextFrame
        tfc.WordWrap = msoTrue

        p1 = tfc.TextRange.Paragraphs(1)
        p1.Text = metric_lbl + "\n"
        p1.Font.Name = TOKENS["fonts"]["primary"]
        p1.Font.Size = 18
        p1.Font.Bold = msoTrue
        p1.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["ink"])
        p1.ParagraphFormat.SpaceAfter = 8

        p2 = tfc.TextRange.Paragraphs(2)
        p2.Text = metric_ctx
        p2.Font.Name = TOKENS["fonts"]["primary"]
        p2.Font.Size = 16.5
        p2.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["muted"])
        hero_shapes.append(tb_ctx)

        # Package Hero Metric for Continuous Seamless Morph
        names = [s.Name for s in hero_shapes if s is not None]
        hero_grp = None
        if len(names) > 1:
            hero_grp = slide.Shapes.Range(names).Group()
            hero_grp.Name = "!!Kinetic_Card_1!!"
        elif len(names) == 1:
            hero_grp = hero_shapes[0]
            hero_grp.Name = "!!Kinetic_Card_1!!"
        if hero_grp is not None:
            self._group_and_animate(slide, [hero_grp], duration=0.45, group_name="!!Kinetic_Card_1!!", is_hero=True)

        # Right Stacked List Cards
        right_left = MARGIN_LEFT + left_w + gutter
        count = max(1, min(len(atoms), 3))
        card_h = (height - (12.0 * (count - 1))) / count

        for i, atom in enumerate(atoms[:count]):
            rcard_shapes = []
            c_top = top + i * (card_h + 12.0)

            rcard = slide.Shapes.AddShape(msoShapeRoundedRectangle, right_left, c_top, right_w, card_h)
            rcard.Fill.Solid()
            rcard.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["surface"])
            rcard.Line.Visible = msoTrue
            rcard.Line.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["card_border"])
            rcard_shapes.append(rcard)

            # 100% Concentric Icon Badge
            icon_name = atom.get("icon", "activity") if isinstance(atom, dict) else "activity"
            rcard_shapes.extend(self._create_icon_badge(slide, icon_name, right_left + 32, c_top + 32, 32, 22))

            title_t = atom.get("title", f"Luận Cứ {i+1}") if isinstance(atom, dict) else f"Luận Cứ {i+1}"
            body_t = atom.get("text", str(atom)) if isinstance(atom, dict) else str(atom)

            stb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, right_left + 58, c_top + 12, right_w - 70, card_h - 24)
            stf = stb.TextFrame
            stf.WordWrap = msoTrue

            sp1 = stf.TextRange.Paragraphs(1)
            sp1.Text = title_t + "\n"
            sp1.Font.Name = TOKENS["fonts"]["primary"]
            sp1.Font.Size = 18.5
            sp1.Font.Bold = msoTrue
            sp1.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["ink"])
            sp1.ParagraphFormat.SpaceAfter = 4

            sp2 = stf.TextRange.Paragraphs(2)
            sp2.Text = body_t
            sp2.Font.Name = TOKENS["fonts"]["primary"]
            sp2.Font.Size = 16.0
            sp2.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["muted"])
            self._group_and_animate(slide, rcard_shapes, duration=0.45, delay=0.12 * (i + 1), group_name=f"!!Kinetic_Card_{i+2}!!")

    def _render_formula_hero_layout(self, slide: Any, spec: Dict[str, Any], atoms: List[Any], top: float, height: float):
        formula_expr = spec.get("formula", "")
        if not formula_expr:
            for a in atoms:
                txt = a.get("text", "") if isinstance(a, dict) else str(a)
                if "=" in txt:
                    formula_expr = txt.split(".")[0].strip()
                    break
            if not formula_expr:
                formula_expr = spec.get("primary_claim", "Công thức định lượng nhân khẩu học")

        hero_h = 88.0
        hero_shapes = []
        f_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, MARGIN_LEFT, top, USABLE_WIDTH, hero_h)
        f_card.Fill.Solid()
        f_card.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["surface"])
        f_card.Line.Visible = msoTrue
        f_card.Line.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["brand"])
        f_card.Line.Weight = 2.0
        hero_shapes.append(f_card)

        pill = slide.Shapes.AddShape(msoShapeRoundedRectangle, MARGIN_LEFT + 20, top + 10, 190, 20)
        pill.Fill.Solid()
        pill.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["badge_bg"])
        pill.Line.Visible = msoFalse
        pt = pill.TextFrame.TextRange
        pt.Text = "CÔNG THỨC ĐỊNH LƯỢNG CHUẨN"
        pt.Font.Name = TOKENS["fonts"]["primary"]
        pt.Font.Size = 13.5
        pt.Font.Bold = msoTrue
        pt.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["brand"])
        pill.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
        hero_shapes.append(pill)

        formula_len = len(formula_expr)
        f_font_size = 17 if formula_len > 55 else (20 if formula_len > 38 else 23)
        tb_eq = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, MARGIN_LEFT + 20, top + 32, USABLE_WIDTH - 40, 48)
        tb_eq.TextFrame.WordWrap = msoTrue
        teq = tb_eq.TextFrame.TextRange
        teq.Text = formula_expr
        teq.Font.Name = "Segoe UI"
        teq.Font.Size = f_font_size
        teq.Font.Bold = msoTrue
        teq.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["accent"] if self.theme == "DARK" else TOKENS["colors"]["brand"])
        tb_eq.TextFrame.TextRange.ParagraphFormat.Alignment = ppAlignCenter
        hero_shapes.append(tb_eq)

        names = [s.Name for s in hero_shapes if s is not None]
        if len(names) > 1:
            grp = slide.Shapes.Range(names).Group()
            grp.Name = "!!Kinetic_Card_1!!"
        elif len(names) == 1:
            hero_shapes[0].Name = "!!Kinetic_Card_1!!"

        param_top = top + hero_h + 14.0
        param_height = height - hero_h - 14.0
        count = len(atoms)

        if count <= 3:
            card_w = (USABLE_WIDTH - (16.0 * (count - 1))) / count
            for i, atom in enumerate(atoms):
                c_shapes = []
                left = MARGIN_LEFT + i * (card_w + 16.0)
                p_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, param_top, card_w, param_height)
                p_card.Fill.Solid()
                p_card.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["surface"])
                p_card.Line.Visible = msoTrue
                p_card.Line.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["card_border"])
                p_card.Line.Weight = 1.0
                c_shapes.append(p_card)

                # 100% Concentric Icon Badge
                icon_name = atom.get("icon", "calculator") if isinstance(atom, dict) else "calculator"
                c_shapes.extend(self._create_icon_badge(slide, icon_name, left + 32, param_top + 32, 32, 22))

                p_title = atom.get("title", f"Tham Số {i+1}") if isinstance(atom, dict) else f"Tham Số {i+1}"
                p_body = atom.get("text", str(atom)) if isinstance(atom, dict) else str(atom)

                tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 16, param_top + 56, card_w - 32, param_height - 64)
                tf = tb.TextFrame
                tf.WordWrap = msoTrue
                tf.MarginLeft = 0
                tf.MarginTop = 0

                p1 = tf.TextRange.Paragraphs(1)
                p1.Text = p_title + "\n"
                p1.Font.Name = TOKENS["fonts"]["primary"]
                p1.Font.Size = 18.5
                p1.Font.Bold = msoTrue
                p1.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["ink"])
                p1.ParagraphFormat.SpaceAfter = 6

                p2 = tf.TextRange.Paragraphs(2)
                p2.Text = p_body
                p2.Font.Name = TOKENS["fonts"]["primary"]
                p2.Font.Size = 16.0
                p2.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["muted"])
                p2.ParagraphFormat.LineRuleWithin = msoTrue
                p2.ParagraphFormat.SpaceWithin = 1.25
                c_shapes.append(tb)

                self._group_and_animate(slide, c_shapes, duration=0.45, delay=0.12 * (i + 1), group_name=f"!!Kinetic_Card_{i+2}!!")

        else:
            card_w = (USABLE_WIDTH - 16.0) / 2
            card_h = (param_height - 12.0) / 2
            for i, atom in enumerate(atoms[:4]):
                c_shapes = []
                r = i // 2
                c = i % 2
                left = MARGIN_LEFT + c * (card_w + 16.0)
                c_top = param_top + r * (card_h + 12.0)

                p_card = slide.Shapes.AddShape(msoShapeRoundedRectangle, left, c_top, card_w, card_h)
                p_card.Fill.Solid()
                p_card.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["surface"])
                p_card.Line.Visible = msoTrue
                p_card.Line.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["card_border"])
                p_card.Line.Weight = 1.0
                c_shapes.append(p_card)

                # 100% Concentric Icon Badge
                icon_name = atom.get("icon", "calculator") if isinstance(atom, dict) else "calculator"
                c_shapes.extend(self._create_icon_badge(slide, icon_name, left + 28, c_top + 28, 28, 20))

                p_title = atom.get("title", f"Tham Số {i+1}") if isinstance(atom, dict) else f"Tham Số {i+1}"
                p_body = atom.get("text", str(atom)) if isinstance(atom, dict) else str(atom)

                tb = slide.Shapes.AddTextbox(msoTextOrientationHorizontal, left + 50, c_top + 8, card_w - 60, card_h - 16)
                tf = tb.TextFrame
                tf.WordWrap = msoTrue
                tf.MarginLeft = 0
                tf.MarginTop = 0

                p1 = tf.TextRange.Paragraphs(1)
                p1.Text = p_title + "\n"
                p1.Font.Name = TOKENS["fonts"]["primary"]
                p1.Font.Size = 18.0
                p1.Font.Bold = msoTrue
                p1.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["ink"])
                p1.ParagraphFormat.SpaceAfter = 4

                p2 = tf.TextRange.Paragraphs(2)
                p2.Text = p_body
                p2.Font.Name = TOKENS["fonts"]["primary"]
                p2.Font.Size = 16.0
                p2.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["muted"])
                p2.ParagraphFormat.LineRuleWithin = msoTrue
                p2.ParagraphFormat.SpaceWithin = 1.2
                c_shapes.append(tb)

                self._group_and_animate(slide, c_shapes, duration=0.45, delay=0.12 * (i + 1), group_name=f"!!Kinetic_Card_{i+2}!!")

    def _render_data_table_layout(self, slide: Any, spec: Dict[str, Any], atoms: List[Any], top: float, height: float):
        table_data = spec.get("table_data", {})
        if not table_data or "headers" not in table_data:
            headers = ["Chỉ Tiêu / Yếu Tố", "Nội Dung Phân Tích & Minh Chứng Thực Tiễn"]
            rows = []
            for a in atoms:
                t = a.get("title", "") if isinstance(a, dict) else str(a)
                b = a.get("text", "") if isinstance(a, dict) else ""
                rows.append([t, b])
            table_data = {"headers": headers, "rows": rows, "col_widths": [0.32, 0.68]}

        headers = table_data.get("headers", [])
        rows = table_data.get("rows", [])
        num_rows = len(rows) + 1
        num_cols = len(headers)

        col_weights = table_data.get("col_widths", [1.0 / num_cols] * num_cols)
        total_w = sum(col_weights)
        norm_weights = [w / total_w for w in col_weights]

        table_shape = slide.Shapes.AddTable(num_rows, num_cols, MARGIN_LEFT, top, USABLE_WIDTH, height)
        table_shape.Name = "!!Kinetic_Card_1!!"
        tbl = table_shape.Table

        for c_idx, w_pct in enumerate(norm_weights, start=1):
            tbl.Columns(c_idx).Width = USABLE_WIDTH * w_pct

        for c_idx, h_text in enumerate(headers, start=1):
            cell = tbl.Cell(1, c_idx)
            cell.Shape.Fill.Solid()
            cell.Shape.Fill.ForeColor.RGB = hex_to_bgr(TOKENS["colors"]["brand"])
            try:
                cell.Shape.TextFrame.VerticalAnchor = 3  # msoAnchorMiddle
                cell.Shape.TextFrame.MarginTop = 6
                cell.Shape.TextFrame.MarginBottom = 6
            except Exception:
                pass
            tr = cell.Shape.TextFrame.TextRange
            tr.Text = str(h_text).upper()
            tr.Font.Name = TOKENS["fonts"]["primary"]
            tr.Font.Size = 14.5
            tr.Font.Bold = msoTrue
            tr.Font.Color.RGB = hex_to_bgr("#FFFFFF")
            tr.ParagraphFormat.Alignment = ppAlignCenter if c_idx > 1 else ppAlignLeft

        for r_idx, row_items in enumerate(rows, start=2):
            is_odd = (r_idx % 2 == 1)
            row_bg = TOKENS["colors"]["surface"] if is_odd else (TOKENS["colors"]["card_navy"] if self.theme == "DARK" else "#F1F5F9")
            for c_idx, val in enumerate(row_items, start=1):
                cell = tbl.Cell(r_idx, c_idx)
                cell.Shape.Fill.Solid()
                cell.Shape.Fill.ForeColor.RGB = hex_to_bgr(row_bg)
                try:
                    cell.Shape.TextFrame.VerticalAnchor = 3  # msoAnchorMiddle
                    cell.Shape.TextFrame.MarginTop = 6
                    cell.Shape.TextFrame.MarginBottom = 6
                except Exception:
                    pass
                tr = cell.Shape.TextFrame.TextRange
                tr.Text = str(val)
                tr.Font.Name = TOKENS["fonts"]["primary"]
                tr.Font.Size = 14.0
                tr.Font.Bold = msoTrue if c_idx == 1 else msoFalse
                tr.Font.Color.RGB = hex_to_bgr(TOKENS["colors"]["ink"])
                tr.ParagraphFormat.Alignment = ppAlignCenter if (c_idx > 1 and len(str(val)) <= 18) else ppAlignLeft



def main():
    parser = argparse.ArgumentParser(description="Author Native PowerPoint Presentation Deck")
    parser.add_argument("--blueprints", required=True, type=Path, help="Path to slide-blueprints.json")
    parser.add_argument("--output", required=True, type=Path, help="Output path for .pptx file")
    parser.add_argument("--theme", default="DARK", choices=["DARK", "LIGHT"], help="Presentation theme")
    parser.add_argument("--motion-mode", default="presenter_click", choices=["presenter_click", "kinetic_cascade"],
                        help="Motion choreography mode (default: presenter_click)")
    parser.add_argument("--visible", action="store_true", help="Launch PowerPoint with visible UI")
    args = parser.parse_args()

    author = NativeDeckAuthor(visible=args.visible, theme=args.theme, motion_mode=args.motion_mode)
    try:
        t0 = time.time()
        out_path = author.create_deck(args.blueprints, args.output)
        elapsed = time.time() - t0
        print(f"Presentation authored successfully in {elapsed:.2f}s: {out_path}")
    finally:
        author.close()


if __name__ == "__main__":
    main()

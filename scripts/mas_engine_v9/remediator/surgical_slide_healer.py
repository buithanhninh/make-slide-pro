# -*- coding: utf-8 -*-
"""
scripts/mas_engine_v9/remediator/surgical_slide_healer.py
Surgical In-Place Slide Remediator (Agent 6 of MAS-CLSH V9.0).
Executes pinpoint slide re-generation and in-place COM hot-swapping:
1. Compiles patched blueprint for the single defective slide.
2. Renders a temporary single-slide deck via Native PowerPoint COM.
3. Swaps the healed slide directly into the target deck at exact index k.
4. Preserves all other 49+ slides untouched in sub-second time.
"""

from __future__ import annotations
import json
import os
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
import win32com.client

from ..models import RemediationDirective

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from scripts.author_native_com import NativeDeckAuthor
except ImportError:
    NativeDeckAuthor = None


class SurgicalSlideRemediator:
    """Surgically re-generates and replaces a defective slide in-place."""

    def __init__(self, theme: str = "DARK", motion_mode: str = "presenter_click"):
        self.theme = theme.upper()
        self.motion_mode = motion_mode

    def heal_slide_in_place(
        self,
        presentation_path: Path,
        slide_index: int,
        directive: RemediationDirective,
    ) -> bool:
        """Hot-swaps slide at slide_index with the patched blueprint version."""
        if not directive.updated_blueprint:
            print(f"[SurgicalHealer] No updated blueprint provided for Slide {slide_index}.")
            return False

        if not presentation_path.exists():
            print(f"[SurgicalHealer] File not found: {presentation_path}")
            return False

        temp_dir = Path(tempfile.mkdtemp(prefix="slide_heal_"))
        temp_bp_path = temp_dir / "healed_slide_bp.json"
        temp_pptx_path = temp_dir / "healed_slide.pptx"

        # Build 1-slide blueprint envelope
        single_slide_bp = {
            "schema_version": "9.0.0",
            "version": "9.0.0",
            "deck_title": "HEALED_SLIDE_PATCH",
            "total_slides": 1,
            "theme": self.theme,
            "slides": [directive.updated_blueprint],
        }

        with open(temp_bp_path, "w", encoding="utf-8") as f:
            json.dump(single_slide_bp, f, ensure_ascii=False, indent=2)

        # 1. Render single healed slide
        if NativeDeckAuthor is None:
            print("[SurgicalHealer] NativeDeckAuthor unavailable.")
            return False

        print(f"[*] [SurgicalHealer] Rendering healed replacement for Slide {slide_index}...")
        author = NativeDeckAuthor(visible=False, theme=self.theme, motion_mode=self.motion_mode)
        try:
            author.create_deck(temp_bp_path, temp_pptx_path)
        except Exception as e:
            print(f"[SurgicalHealer] Error rendering replacement slide: {e}")
            return False
        finally:
            try:
                author.close()
            except Exception:
                pass

        # 2. Hot-swap in PowerPoint COM
        ppt_app = win32com.client.DispatchEx("PowerPoint.Application")
        deck = None
        try:
            deck = ppt_app.Presentations.Open(
                str(presentation_path.resolve()), ReadOnly=False, Untitled=False, WithWindow=False
            )
            total_slides = deck.Slides.Count

            if 1 <= slide_index <= total_slides:
                # Insert the healed slide immediately AFTER the target slide
                deck.Slides.InsertFromFile(str(temp_pptx_path.resolve()), slide_index, 1, 1)
                # Delete the old defective slide (which is now at slide_index)
                deck.Slides(slide_index).Delete()
                deck.Save()
                print(f"✔ [SurgicalHealer] Successfully hot-swapped Slide {slide_index} in {presentation_path.name}.")
                return True
            else:
                print(f"[SurgicalHealer] Slide index {slide_index} out of bounds (1..{total_slides}).")
                return False
        except Exception as e:
            print(f"[SurgicalHealer] COM hot-swap failed: {e}")
            return False
        finally:
            if deck is not None:
                try:
                    deck.Close()
                except Exception:
                    pass
            try:
                ppt_app.Quit()
            except Exception:
                pass
            # Clean up temp files
            try:
                if temp_pptx_path.exists():
                    temp_pptx_path.unlink()
                if temp_bp_path.exists():
                    temp_bp_path.unlink()
                temp_dir.rmdir()
            except Exception:
                pass

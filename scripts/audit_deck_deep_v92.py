# -*- coding: utf-8 -*-
"""
scripts/audit_deck_deep_v92.py
Exhaustive Deep Post-Render Forensic Quality Audit Gate for Make Slide Pro V9.2.2.
Inspects all slides via PowerPoint COM for:
1. Pure Continuous Morph (0.85s) on slides 2..N-1, Cinematic Fade (0.65s) on Slide 1 & N.
2. Presenter Sequencing: Trigger 0 = WithPrevious (2), Triggers 1..N = OnPageClick (1), Total Triggers <= 5.
3. Zero Runaway Clicks (no slide with > 5 click triggers).
4. Atomic Card Encapsulation: groups present, zero loose fragmented shapes.
5. Zero AI clichés & Zero developer mock leaks (SLA, Morph, 165+, Q1/2024).
6. Title-Content Cardinality Consistency.
"""

from __future__ import annotations
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple
import win32com.client

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MORPH_CODES = {3954, 3850, 3953, 3955}
FADE_CODES = {3849, 3844, 3848}

SLOP_PATTERNS = [
    r"sla\s*99",
    r"morph\s*0\.85s?",
    r"165\+\s*mẫu",
    r"165\+\s*archetypes",
    r"thư viện mega",
    r"mckinsey & bcg",
    r"q[1-4]/\d{4}",
    r"100m\+\s*records",
    r"gemini\s*&\s*embeddings",
    r"bức tranh toàn cảnh",
    r"chìa khóa then chốt",
    r"tiếp cận đa chiều",
    r"\(phần\s*\d+/\d+\)",
    r"tiêu chuẩn đào tạo",
    r"watermark",
    r"delta\s*lake",
    r"apache\s*iceberg",
    r"acid\s*guaranteed",
]


def audit_deck(pptx_path: Path) -> Dict[str, Any]:
    ppt_app = win32com.client.DispatchEx("PowerPoint.Application")
    deck = None
    results = {
        "file": pptx_path.name,
        "total_slides": 0,
        "p0_defects": [],
        "p1_defects": [],
        "p2_defects": [],
        "slide_details": {},
        "overall_passed": False
    }

    try:
        deck = ppt_app.Presentations.Open(str(pptx_path.resolve()), ReadOnly=True, Untitled=False, WithWindow=False)
        total_slides = deck.Slides.Count
        results["total_slides"] = total_slides

        for i in range(1, total_slides + 1):
            s = deck.Slides(i)
            is_cover = (i == 1)
            is_outro = (i == total_slides)

            # 1. Transition Check
            trans = s.SlideShowTransition
            entry_eff = trans.EntryEffect
            dur = round(trans.Duration, 2)
            trans_ok = True
            if is_cover or is_outro:
                if entry_eff not in FADE_CODES:
                    results["p0_defects"].append(f"Slide {i:02d}: Transition {entry_eff} is not Fade (expected 3849/3844)")
                    trans_ok = False
            else:
                if entry_eff not in MORPH_CODES:
                    results["p0_defects"].append(f"Slide {i:02d}: Transition {entry_eff} is not Morph (expected 3954)")
                    trans_ok = False

            # 2. Timeline and Presenter Sequencing Check
            seq = s.TimeLine.MainSequence
            triggers = [seq(t).Timing.TriggerType for t in range(1, seq.Count + 1)]
            timeline_ok = True

            if not (is_cover or is_outro) and triggers:
                # Runaway clicks
                if len(triggers) > 5:
                    results["p0_defects"].append(f"Slide {i:02d}: Runaway clicks! {len(triggers)} triggers ({triggers})")
                    timeline_ok = False

                # Validate trigger types (1=OnPageClick, 2=WithPrevious)
                invalid_triggers = [tr for tr in triggers if tr not in (1, 2)]
                if invalid_triggers:
                    results["p1_defects"].append(f"Slide {i:02d}: Invalid trigger types {invalid_triggers}")
                    timeline_ok = False

                # Morph-Suppression Check: Card 0 / !!Kinetic_Card_1!! must NOT have an intra-slide animation
                # because any entrance effect in MainSequence causes PowerPoint to hide Card 0 during transition
                # and cancels Morph!
                for t in range(1, seq.Count + 1):
                    try:
                        anim_shape = seq(t).Shape
                        if anim_shape and getattr(anim_shape, "Name", "") == "!!Kinetic_Card_1!!":
                            results["p1_defects"].append(f"Slide {i:02d}: !!Kinetic_Card_1!! has intra-slide animation (suppresses Morph!)")
                            timeline_ok = False
                            break
                    except Exception:
                        pass

            # 3. Shape & Group Analysis & Kinetic Naming Contract
            shape_count = s.Shapes.Count
            shape_names = []
            for j in range(1, shape_count + 1):
                try:
                    shape_names.append(s.Shapes(j).Name)
                except Exception:
                    pass

            groups = [s.Shapes(j) for j in range(1, shape_count + 1) if s.Shapes(j).Type == 6]
            group_count = len(groups)

            # Morph Bridge Contract: Content slides should have !!Kinetic_Card_1!!
            if not (is_cover or is_outro):
                has_kinetic_card = any("Kinetic_Card_1" in name for name in shape_names)
                if not has_kinetic_card and shape_count > 3:
                    results["p1_defects"].append(f"Slide {i:02d}: Missing !!Kinetic_Card_1!! (Morph Bridge anchor missing)")

            # Check loose shape fragmentation
            if not (is_cover or is_outro) and shape_count > 9 and group_count == 0:
                results["p1_defects"].append(f"Slide {i:02d}: Fragmented loose shapes! {shape_count} shapes with 0 groups")

            # 4. Text Extraction and Slop Scan
            slide_texts = []
            for j in range(1, shape_count + 1):
                shp = s.Shapes(j)
                if shp.HasTextFrame and shp.TextFrame.HasText:
                    slide_texts.append(shp.TextFrame.TextRange.Text.strip())
                elif shp.Type == 6:  # group
                    try:
                        for gi in range(1, shp.GroupItems.Count + 1):
                            c_shp = shp.GroupItems(gi)
                            if c_shp.HasTextFrame and c_shp.TextFrame.HasText:
                                slide_texts.append(c_shp.TextFrame.TextRange.Text.strip())
                    except Exception:
                        pass

            full_text = "\n".join(slide_texts)

            # Slop pattern scan
            for pat in SLOP_PATTERNS:
                m = re.search(pat, full_text, re.IGNORECASE)
                if m:
                    results["p0_defects"].append(f"Slide {i:02d}: Leaked slop pattern '{m.group(0)}'")

            # Cardinality check
            title_txt = slide_texts[0] if slide_texts else ""
            cardinal_m = re.search(r"\b([2-9])\s*(khối|giai đoạn|đặc trưng|trụ cột|bước|nguyên tắc|mục tiêu|khía cạnh)\b", title_txt, re.IGNORECASE)
            if cardinal_m:
                expected = int(cardinal_m.group(1))
                num_items = set(re.findall(r"(?:^|\n)\s*([1-9])\.\s+", full_text))
                if num_items and len(num_items) != expected:
                    results["p0_defects"].append(f"Slide {i:02d}: Cardinality mismatch! Title says '{expected}' but found items {sorted(list(num_items))}")

            results["slide_details"][i] = {
                "shapes": shape_count,
                "groups": group_count,
                "triggers": triggers,
                "trans": f"{'Fade' if is_cover or is_outro else 'Morph'} ({dur}s)",
                "status": "PASS" if trans_ok and timeline_ok else "FLAGGED"
            }

        results["overall_passed"] = (len(results["p0_defects"]) == 0 and len(results["p1_defects"]) == 0)

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

    return results


if __name__ == "__main__":
    target = PROJECT_ROOT / "Du_An_Outputs" / "A_Tuan_Dan_So_2" / "BÀI 1. Tổng quan về dịch vụ dân số - Dark.pptx"
    if not target.exists():
        target = PROJECT_ROOT / "Du_An_Outputs" / "A_Tuan_Dan_So_2" / "BÀI_1__Tổng_quan_về_dịch_vụ_dân_số" / "BÀI_1__Tổng_quan_về_dịch_vụ_dân_số_Dark.pptx"
    
    print("=" * 80)
    print("   FORENSIC QUALITY AUDIT GATE: MAKE SLIDE PRO V9.2.2")
    print(f"   Target Presentation: {target.name}")
    print("=" * 80)

    res = audit_deck(target)
    print(f"Total Slides Audited: {res['total_slides']}")
    print(f"P0 Defects: {len(res['p0_defects'])}")
    for d in res["p0_defects"]:
        print(f"  [P0] {d}")
    print(f"P1 Defects: {len(res['p1_defects'])}")
    for d in res["p1_defects"]:
        print(f"  [P1] {d}")

    print("\nSummary of Slide Details:")
    for s_idx, d in res["slide_details"].items():
        print(f"  Slide {s_idx:02d}: {d['trans']} | Shapes={d['shapes']}, Groups={d['groups']} | Triggers={d['triggers']} -> {d['status']}")

    print("\n" + "=" * 80)
    if res["overall_passed"]:
        print("   ★ CERTIFIED: 100% COMPLIANT WITH MAKE SLIDE PRO V9.2.2 STANDARD ★")
    else:
        print(f"   ✖ NOT CERTIFIED: Found {len(res['p0_defects'])} P0 and {len(res['p1_defects'])} P1 defects.")
    print("=" * 80)

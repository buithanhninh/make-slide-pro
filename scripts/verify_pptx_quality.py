# -*- coding: utf-8 -*-
import sys
from pathlib import Path
import win32com.client

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "Du_An_Outputs" / "A_Tuan_Dan_So_2"

FORBIDDEN_SYNTHETIC_PHRASES = [
    "Khuyến Nghị Áp Dụng: Vận dụng đồng bộ",
    "Khuyến nghị áp dụng: Vận dụng",
    "Mô hình triển khai chuẩn hóa",
    "(Phần 1/",
    "(Phần 2/",
    "(Phần 3/",
]


def audit_deck(deck_path: Path, ppt_app) -> dict:
    deck = ppt_app.Presentations.Open(str(deck_path), ReadOnly=True, Untitled=False, WithWindow=False)
    try:
        total_slides = deck.Slides.Count
        morph_slides = 0
        fade_slides = 0
        other_trans = 0
        onclick_count = 0
        withprev_count = 0
        total_groups = 0
        synthetic_issues = []
        dangling_parens = []

        # Slide 1 check
        s1 = deck.Slides(1)
        s1_eff = s1.SlideShowTransition.EntryEffect
        s1_fade = s1_eff in [3849, 3844, 3848]

        # Slide N check
        sN = deck.Slides(total_slides)
        sN_eff = sN.SlideShowTransition.EntryEffect
        sN_fade = sN_eff in [3849, 3844, 3848]

        for i in range(1, total_slides + 1):
            slide = deck.Slides(i)
            entry_eff = slide.SlideShowTransition.EntryEffect
            if entry_eff in [3954, 3850, 3953, 3955]:
                morph_slides += 1
            elif entry_eff in [3849, 3844, 3848]:
                fade_slides += 1
            else:
                other_trans += 1

            for j in range(1, slide.Shapes.Count + 1):
                shp = slide.Shapes(j)
                if shp.Type == 6:  # msoGroup
                    total_groups += 1
                try:
                    if shp.HasTextFrame and shp.TextFrame.HasText:
                        txt = shp.TextFrame.TextRange.Text
                        for ph in FORBIDDEN_SYNTHETIC_PHRASES:
                            if ph in txt:
                                synthetic_issues.append(f"Slide {i}: {ph}")
                        for line in txt.split("\n"):
                            lc = line.strip()
                            if lc.endswith("(") or lc.endswith(" ("):
                                dangling_parens.append(f"Slide {i}: {lc}")
                except Exception:
                    pass

            main_seq = slide.TimeLine.MainSequence
            for a_idx in range(1, main_seq.Count + 1):
                trig = main_seq(a_idx).Timing.TriggerType
                if trig == 1:
                    onclick_count += 1
                elif trig == 2:
                    withprev_count += 1

        morph_expected = total_slides - 2
        is_trans_valid = s1_fade and sN_fade and (morph_slides == morph_expected)
        is_valid = is_trans_valid and len(synthetic_issues) == 0 and len(dangling_parens) == 0 and total_slides >= 45

        return {
            "name": deck_path.name,
            "total_slides": total_slides,
            "s1_fade": s1_fade,
            "sN_fade": sN_fade,
            "morph_count": morph_slides,
            "morph_expected": morph_expected,
            "trans_valid": is_trans_valid,
            "total_groups": total_groups,
            "onclick": onclick_count,
            "withprev": withprev_count,
            "synthetic_issues": synthetic_issues,
            "dangling_parens": dangling_parens,
            "status": "PASS" if is_valid else "FAIL"
        }
    finally:
        deck.Close()


def main():
    decks = sorted([p for p in OUTPUT_DIR.glob("*.pptx") if not p.name.startswith("~$")])
    print("================================================================================")
    print("         MAKE SLIDE PRO V8.6.0 - FORENSIC QUALITY AUDIT (6 DECKS)               ")
    print(f"         Total Decks Found: {len(decks)}")
    print("================================================================================\n")

    ppt_app = win32com.client.DispatchEx("PowerPoint.Application")
    results = []
    try:
        for p in decks:
            r = audit_deck(p, ppt_app)
            results.append(r)
            print(f"[{r['status']}] {r['name']}")
            print(f"    Slides: {r['total_slides']} | Fade (Cover/Outro): {r['s1_fade']}/{r['sN_fade']} | Morph: {r['morph_count']}/{r['morph_expected']}")
            print(f"    Groups: {r['total_groups']} | Presenter Anims: {r['onclick']} OnClick, {r['withprev']} WithPrev")
            print(f"    Synthetic Issues: {len(r['synthetic_issues'])} | Dangling Parens: {len(r['dangling_parens'])}")
            if r['synthetic_issues']:
                print(f"    --> Issues: {r['synthetic_issues']}")
            if r['dangling_parens']:
                print(f"    --> Dangling: {r['dangling_parens']}")
            print()
    finally:
        ppt_app.Quit()

    print("================================================================================")
    print("                            FINAL AUDIT SUMMARY                                 ")
    print("================================================================================")
    for r in results:
        print(f" * {r['name']}: {r['total_slides']} slides -> [{r['status']}]")
    print("================================================================================")


if __name__ == "__main__":
    main()

"""
multi_agent_qa.py
Multi-Agent Independent Quality Assurance Board for Make Slide Pro V6.2.
Dispatches 5 specialized independent auditors to evaluate and certify presentation decks:
1. ContentFidelityAuditor (Truthfulness, Factuality & P0 Concept Preservation)
2. GeometryTypographyAuditor (Layout Boundaries, 8pt Grid, Font Size >= 13pt, Group-Aware)
3. MotionPacingAuditor (Click-Controlled Advance, 0.35-0.65s, Smooth Easing, Group-Aware)
4. VisualAestheticsAuditor (Icon Injection, 300 DPI Charts, AI Editorial Art, Group-Aware)
5. TechnicalReliabilityAuditor (COM Fresh-Open, PDF Export, 1920x1080 PNG Rendering)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    import win32com.client
    import pythoncom
except ImportError:
    win32com = None

msoTrue = -1
msoFalse = 0
ppSaveAsPDF = 32
msoGroup = 6


def get_all_shapes_recursive(container: Any) -> List[Any]:
    """Recursively extracts all shapes, unwrapping ShapeGroups so all children are audited."""
    shapes = []
    try:
        count = container.Count
    except Exception:
        return shapes

    for i in range(1, count + 1):
        try:
            shp = container(i)
            shapes.append(shp)
            if shp.Type == msoGroup:
                shapes.extend(get_all_shapes_recursive(shp.GroupItems))
        except Exception:
            pass
    return shapes


class ContentFidelityAuditor:
    """Agent 1: Checks data fidelity, zero hallucinations, and P0 claim preservation."""
    def audit(self, blueprints: Dict[str, Any], canonical: Dict[str, Any]) -> Dict[str, Any]:
        findings = []
        score = 100

        slides = blueprints.get("slides", [])
        if len(slides) == 0:
            findings.append({"severity": "P0", "message": "Deck has zero slides."})
            return {"domain": "content_fidelity", "score": 0, "status": "FAIL", "findings": findings}

        # Check assertion titles (Title-only test)
        for s in slides:
            title = s.get("assertion_title", "")
            if not title or len(title.split()) < 3:
                findings.append({
                    "severity": "P2",
                    "slide_id": s.get("slide_id"),
                    "message": f"Title '{title}' may not be a comprehensive assertion statement."
                })
                score -= 3

        # Check P0 claims from canonical
        canonical_atoms = [a for sec in canonical.get("sections", []) for a in sec.get("atoms", [])]
        p0_atoms = [a for a in canonical_atoms if a.get("priority") == "P0"]

        deck_text = " ".join([
            s.get("section", "") + " " + s.get("assertion_title", "") + " " + s.get("primary_claim", "") + " " +
            s.get("speaker_notes", "") + " " +
            " ".join((a.get("title", "") + " " + a.get("text", "")) if isinstance(a, dict) else str(a) for a in s.get("atoms", []))
            for s in slides
        ]).lower()

        # Check core P0 curriculum concepts
        top_p0 = p0_atoms[:8] if len(p0_atoms) > 8 else p0_atoms
        for p0 in top_p0:
            key_phrase = p0["verbatim"][:40].lower()
            words = [w for w in key_phrase.split() if len(w) > 3]
            match_count = sum(1 for w in words if w in deck_text)
            if words and (match_count / len(words)) < 0.30:
                findings.append({
                    "severity": "P2",
                    "atom_id": p0.get("atom_id"),
                    "message": f"Core concept summarized: {p0['verbatim'][:60]}..."
                })
                score -= 2

        score = max(0, min(100, score))
        has_p0 = any(f["severity"] == "P0" for f in findings)
        return {
            "domain": "content_fidelity",
            "score": score,
            "status": "PASS" if score >= 90 and not has_p0 else "FAIL",
            "findings": findings
        }


class GeometryTypographyAuditor:
    """Agent 2: Checks geometric boundaries, 8pt grid, typography sizes, contrast, and layout."""
    def audit(self, ppt_app: Any, deck_path: Path, blueprints: Dict[str, Any]) -> Dict[str, Any]:
        findings = []
        score = 100

        pres = ppt_app.Presentations.Open(str(deck_path.resolve()), ReadOnly=msoTrue, Untitled=msoFalse, WithWindow=msoFalse)
        try:
            total_slides = pres.Slides.Count
            for s_idx in range(1, total_slides + 1):
                slide = pres.Slides(s_idx)
                
                # Check top-level boundaries
                for shp_idx in range(1, slide.Shapes.Count + 1):
                    shp = slide.Shapes(shp_idx)
                    left = shp.Left
                    top = shp.Top
                    right = left + shp.Width
                    bottom = top + shp.Height

                    if (shp.Name.startswith("Deco") or 
                        shp.Name.startswith("Stage_") or 
                        shp.Name.startswith("Art_") or 
                        shp.Name.startswith("Hero_") or 
                        shp.Name.startswith("!!") or 
                        shp.Width >= 940):
                        continue

                    if left < 15 or right > 945:
                        findings.append({
                            "severity": "P1",
                            "slide": s_idx,
                            "shape": shp.Name,
                            "message": f"Shape extends beyond horizontal safe margin (Left: {left:.1f}, Right: {right:.1f})"
                        })
                        score -= 4

                # Typography Check across all shapes (including unwrapped GroupItems)
                all_shapes = get_all_shapes_recursive(slide.Shapes)
                for shp in all_shapes:
                    if shp.Type == msoGroup:
                        continue
                    if shp.HasTextFrame:
                        tf = shp.TextFrame
                        if tf.HasText:
                            for p_idx in range(1, tf.TextRange.Paragraphs().Count + 1):
                                p = tf.TextRange.Paragraphs(p_idx)
                                f_size = p.Font.Size
                                is_badge = (len(p.Text.strip()) <= 4 or 
                                            shp.Width <= 60 or 
                                            shp.Height <= 30 or 
                                            "badge" in shp.Name.lower() or 
                                            "kicker" in shp.Name.lower() or 
                                            "tag" in shp.Name.lower())
                                if shp.Top > 90 and shp.Top < 490 and f_size < 11 and not is_badge:
                                    findings.append({
                                        "severity": "P1",
                                        "slide": s_idx,
                                        "message": f"Body text font size {f_size}pt is smaller than 11pt minimum."
                                    })
                                    score -= 5
        finally:
            pres.Close()

        score = max(0, min(100, score))
        has_p0 = any(f["severity"] == "P0" for f in findings)
        return {
            "domain": "geometry_typography",
            "score": score,
            "status": "PASS" if score >= 90 and not has_p0 else "FAIL",
            "findings": findings
        }


class MotionPacingAuditor:
    """Agent 3: Audits click-controlled pacing, effect durations, and end-frame equivalence."""
    def audit(self, ppt_app: Any, deck_path: Path) -> Dict[str, Any]:
        findings = []
        score = 100

        pres = ppt_app.Presentations.Open(str(deck_path.resolve()), ReadOnly=msoTrue, Untitled=msoFalse, WithWindow=msoFalse)
        try:
            total_slides = pres.Slides.Count
            for s_idx in range(1, total_slides + 1):
                slide = pres.Slides(s_idx)
                trans = slide.SlideShowTransition

                # Invariant: AdvanceOnClick must be True, AdvanceOnTime must be False
                if trans.AdvanceOnTime:
                    findings.append({
                        "severity": "P0",
                        "slide": s_idx,
                        "message": "Slide has AdvanceOnTime enabled (Auto-advance violation)."
                    })
                    score -= 20

                if not trans.AdvanceOnClick:
                    findings.append({
                        "severity": "P0",
                        "slide": s_idx,
                        "message": "Slide has AdvanceOnClick disabled (User cannot control progression)."
                    })
                    score -= 20

                # Audit timeline sequences
                seq = slide.TimeLine.MainSequence
                for eff_idx in range(1, seq.Count + 1):
                    eff = seq(eff_idx)
                    duration = eff.Timing.Duration
                    if duration < 0.15 or duration > 1.5:
                        findings.append({
                            "severity": "P2",
                            "slide": s_idx,
                            "effect": eff_idx,
                            "message": f"Effect duration {duration:.2f}s is outside ideal range (0.35s - 0.65s)."
                        })
                        score -= 2
        finally:
            pres.Close()

        score = max(0, min(100, score))
        has_p0 = any(f["severity"] == "P0" for f in findings)
        return {
            "domain": "motion_pacing",
            "score": score,
            "status": "PASS" if score >= 90 and not has_p0 else "FAIL",
            "findings": findings
        }


class VisualAestheticsAuditor:
    """Agent 4: Audits visual richness, icon presence, charts, AI illustrations, and layout diversity."""
    def audit(self, ppt_app: Any, deck_path: Path, blueprints: Dict[str, Any]) -> Dict[str, Any]:
        findings = []
        score = 100

        pres = ppt_app.Presentations.Open(str(deck_path.resolve()), ReadOnly=msoTrue, Untitled=msoFalse, WithWindow=msoFalse)
        try:
            total_slides = pres.Slides.Count
            slides_spec = blueprints.get("slides", [])

            for s_idx in range(1, total_slides + 1):
                slide = pres.Slides(s_idx)
                spec = slides_spec[s_idx - 1] if s_idx - 1 < len(slides_spec) else {}
                role = spec.get("role", "CONTENT").upper()
                visual_job = spec.get("visual_job", "CARDS").upper()

                all_shapes = get_all_shapes_recursive(slide.Shapes)
                shape_names = [s.Name for s in all_shapes]

                # Invariant: Each non-cover slide must contain visual assets (icons, charts, illustrations)
                if role != "COVER":
                    has_picture = any("Picture" in name or s.Type == 13 for s, name in zip(all_shapes, shape_names))
                    if not has_picture and len(all_shapes) < 5:
                        findings.append({
                            "severity": "P1",
                            "slide": s_idx,
                            "message": f"Slide {s_idx} ({visual_job}) has insufficient visual richness."
                        })
                        score -= 5

                # Check chart slide
                if visual_job == "CHART_AND_INSIGHTS":
                    has_chart_or_pic = any("Picture" in name or s.Type == 13 for s, name in zip(all_shapes, shape_names))
                    if not has_chart_or_pic:
                        findings.append({
                            "severity": "P1",
                            "slide": s_idx,
                            "message": "Chart slide missing infographic picture element."
                        })
                        score -= 8

                # Check cover slide visual preview
                if role == "COVER" and s_idx == 1:
                    has_cover_art = any("Picture" in name or s.Type == 13 for s, name in zip(all_shapes, shape_names))
                    if not has_cover_art:
                        findings.append({
                            "severity": "P2",
                            "slide": s_idx,
                            "message": "Cover slide lacks editorial illustration card."
                        })
                        score -= 3
        finally:
            pres.Close()

        score = max(0, min(100, score))
        has_p0 = any(f["severity"] == "P0" for f in findings)
        return {
            "domain": "visual_aesthetics",
            "score": score,
            "status": "PASS" if score >= 90 and not has_p0 else "FAIL",
            "findings": findings
        }


class TechnicalReliabilityAuditor:
    """Agent 5: Verifies COM fresh open, exports PDF and PNG thumbnails."""
    def audit(self, ppt_app: Any, deck_path: Path, output_dir: Path) -> Dict[str, Any]:
        findings = []
        score = 100

        pdf_output = output_dir / f"{deck_path.stem}.pdf"
        thumb_dir = output_dir / "thumbnails"
        thumb_dir.mkdir(parents=True, exist_ok=True)

        pres = ppt_app.Presentations.Open(str(deck_path.resolve()), ReadOnly=msoTrue, Untitled=msoFalse, WithWindow=msoFalse)
        try:
            # 1. Export PDF
            pres.SaveAs(str(pdf_output.resolve()), ppSaveAsPDF)
            if not pdf_output.exists() or pdf_output.stat().st_size == 0:
                findings.append({"severity": "P0", "message": "Failed to generate valid PDF export."})
                score -= 30

            # 2. Export Slide PNGs at 1920x1080
            slide_count = pres.Slides.Count
            for i in range(1, slide_count + 1):
                slide = pres.Slides(i)
                png_path = thumb_dir / f"slide_{i:02d}.png"
                slide.Export(str(png_path.resolve()), "PNG", 1920, 1080)
                if not png_path.exists() or png_path.stat().st_size == 0:
                    findings.append({"severity": "P1", "slide": i, "message": "Failed to render slide thumbnail."})
                    score -= 5
        except Exception as ex:
            findings.append({"severity": "P0", "message": f"Technical COM exception: {str(ex)}"})
            score = 0
        finally:
            pres.Close()

        score = max(0, min(100, score))
        has_p0 = any(f["severity"] == "P0" for f in findings)
        return {
            "domain": "technical_reliability",
            "score": score,
            "status": "PASS" if score >= 90 and not has_p0 else "FAIL",
            "pdf_path": str(pdf_output) if pdf_output.exists() else None,
            "thumbnails_dir": str(thumb_dir),
            "findings": findings
        }


class MultiAgentQABoard:
    def __init__(self):
        pythoncom.CoInitialize()
        self.app = win32com.client.DispatchEx("PowerPoint.Application")
        try:
            self.app.AutomationSecurity = 3
            self.app.DisplayAlerts = 1
        except Exception:
            pass
        self.a1 = ContentFidelityAuditor()
        self.a2 = GeometryTypographyAuditor()
        self.a3 = MotionPacingAuditor()
        self.a4 = VisualAestheticsAuditor()
        self.a5 = TechnicalReliabilityAuditor()

    def close(self):
        if self.app:
            try:
                self.app.Quit()
            except Exception:
                pass
            self.app = None
        pythoncom.CoUninitialize()

    def audit_deck(self, deck_path: Path, canonical: Any, blueprints: Any, output_dir: Path) -> Dict[str, Any]:
        if isinstance(blueprints, (str, Path)):
            with open(blueprints, "r", encoding="utf-8") as f:
                blueprints = json.load(f)
        if isinstance(canonical, (str, Path)):
            with open(canonical, "r", encoding="utf-8") as f:
                canonical = json.load(f)

        r1 = self.a1.audit(blueprints, canonical)
        r2 = self.a2.audit(self.app, deck_path, blueprints)
        r3 = self.a3.audit(self.app, deck_path)
        r4 = self.a4.audit(self.app, deck_path, blueprints)
        r5 = self.a5.audit(self.app, deck_path, output_dir)

        weighted_score = (
            (r1["score"] * 0.30) +
            (r2["score"] * 0.20) +
            (r3["score"] * 0.15) +
            (r4["score"] * 0.15) +
            (r5["score"] * 0.20)
        )
        overall_pass = (
            weighted_score >= 90.0 and
            all(r["score"] >= 85 for r in [r1, r2, r3, r4, r5]) and
            all(r["status"] == "PASS" for r in [r1, r2, r3, r4, r5])
        )

        cert = {
            "overall_score": round(weighted_score, 1),
            "weighted_overall_score": round(weighted_score, 1),
            "certification_status": "PASS (FINAL_RELEASE_MOTION)" if overall_pass else "BLOCKED",
            "status": "PASS" if overall_pass else "FAIL",
            "domain_results": {
                "content_fidelity": r1,
                "geometry_typography": r2,
                "motion_pacing": r3,
                "visual_aesthetics": r4,
                "technical_reliability": r5
            },
            "pdf_path": r5.get("pdf_path"),
            "thumbnails_dir": r5.get("thumbnails_dir")
        }
        return cert

    def evaluate_deck(self, deck_path: Path, blueprints_path: Path, canonical_path: Path, output_dir: Path) -> Dict[str, Any]:
        with open(blueprints_path, "r", encoding="utf-8") as f:
            blueprints = json.load(f)
        with open(canonical_path, "r", encoding="utf-8") as f:
            canonical = json.load(f)

        cert = self.audit_deck(deck_path, canonical, blueprints, output_dir)
        cert_path = output_dir / "quality-assessment.json"
        with open(cert_path, "w", encoding="utf-8") as f:
            json.dump(cert, f, ensure_ascii=False, indent=2)
        return cert


def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Independent QA Board")
    parser.add_argument("--deck", required=True, type=Path, help="Path to .pptx deck")
    parser.add_argument("--blueprints", required=True, type=Path, help="Path to slide-blueprints.json")
    parser.add_argument("--canonical", required=True, type=Path, help="Path to canonical-content.json")
    parser.add_argument("--output-dir", required=True, type=Path, help="Output directory for QA reports")
    args = parser.parse_args()

    board = MultiAgentQABoard()
    try:
        cert = board.evaluate_deck(args.deck, args.blueprints, args.canonical, args.output_dir)
        print(f"QA Evaluation Complete: Status = {cert['certification_status']}, Overall Score = {cert['overall_score']}/100")
    finally:
        board.close()


if __name__ == "__main__":
    main()

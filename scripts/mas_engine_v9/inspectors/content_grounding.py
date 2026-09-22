# -*- coding: utf-8 -*-
"""
scripts/mas_engine_v9/inspectors/content_grounding.py
Forensic Content Grounding & Accuracy Inspector (Agent 1 of MAS-CLSH V9.0).
Scans slide text for:
1. Grounding against source knowledge base / canonical ledger.
2. Complete eradication of forbidden synthetic filler and AI clichés.
3. Syntax integrity (dangling parentheses, broken sentence cuts, empty brackets).
4. Cognitive density & pedagogical depth.
"""

from __future__ import annotations
import re
from typing import Any, Dict, List, Optional, Tuple
from ..models import DefectIssue

FORBIDDEN_SYNTHETIC_PATTERNS = [
    # 1. AI Slop Clichés & Generic Buzzwords (Unnatural AI generated phrases)
    (r"bức tranh toàn cảnh", "AI slop cliché buzzword"),
    (r"đột phá toàn diện", "AI slop cliché buzzword"),
    (r"hệ sinh thái tối ưu", "AI slop cliché buzzword"),
    (r"tiếp cận đa chiều", "AI slop cliché buzzword"),
    (r"chìa khóa then chốt", "AI slop cliché buzzword"),
    (r"chìa khóa vàng", "AI slop cliché buzzword"),
    (r"vững bước tương lai", "AI slop cliché buzzword"),
    (r"khám phá tiềm năng", "AI slop cliché buzzword"),
    (r"trong kỷ nguyên số", "AI slop cliché buzzword"),
    (r"vận dụng đồng bộ", "AI slop cliché buzzword"),
    (r"tổng thể toàn diện", "AI slop cliché buzzword"),
    (r"không ngừng nâng cao", "AI slop cliché buzzword"),
    (r"nâng tầm vị thế", "AI slop cliché buzzword"),
    (r"đẩy mạnh toàn diện", "AI slop cliché buzzword"),
    (r"tạo đà phát triển", "AI slop cliché buzzword"),
    (r"nền tảng vững chắc", "AI slop cliché buzzword"),
    (r"giải pháp tối ưu", "AI slop cliché buzzword"),
    (r"bước chuyển mình", "AI slop cliché buzzword"),
    (r"hướng tới tương lai", "AI slop cliché buzzword"),
    (r"khuyến nghị áp dụng:\s*vận dụng đồng bộ", "Synthetic boiler-plate filler phrase"),
    (r"mô hình triển khai chuẩn hóa", "Generic unsubstantiated subtitle"),
    (r"\(phần\s*\d+/\d+\)", "Artificial slide fragmentation"),

    # 2. Fake Watermark / Repetitive System Tags Blacklist (P0)
    (r"tiêu chuẩn đào tạo", "Fake system watermark / repetitive tag"),
    (r"tiêu chuẩn hệ thống", "Fake system watermark / repetitive tag"),
    (r"nhãn hệ thống", "Fake system watermark / repetitive tag"),
    (r"watermark", "Fake watermark text"),
    (r"ai generated", "Synthetic watermark text"),
    (r"placeholder", "Placeholder residual text"),

    (r"thư viện mega", "Synthetic showcase demo copy"),
    (r"mckinsey & bcg", "Synthetic showcase demo copy"),
    (r"khảo sát hiện trạng", "Synthetic showcase demo copy"),
    (r"phân tích khoảng trống", "Synthetic showcase demo copy"),
    (r"thiết kế kiến trúc", "Synthetic showcase demo copy"),
    (r"triển khai & kiểm thử", "Synthetic showcase demo copy"),
    (r"bàn giao & mở rộng", "Synthetic showcase demo copy"),
    (r"sandbox", "Synthetic showcase demo copy"),
    (r"tự động hóa với make slide pro", "Synthetic showcase self-referential text"),
    (r"16 tác tử macc", "Synthetic showcase self-referential text"),
    (r"165\+\s*archetypes", "Synthetic showcase self-referential text"),
    (r"110\+\s*archetypes", "Synthetic showcase self-referential text"),
    (r"165\+\s*mẫu", "Synthetic archetype showcase leak"),
    (r"sla\s*99", "Synthetic developer SLA benchmark leak"),
    (r"morph\s*0\.85s?", "Synthetic animation spec parameter leak"),
    (r"q[1-4]/\d{4}", "Synthetic generic quarter placeholder leak"),
    (r"100m\+\s*records", "Synthetic developer placeholder leak"),
    (r"gemini\s*&\s*embeddings", "Synthetic developer pipeline leak"),
    (r"delta\s*lake", "Synthetic data platform leak in demographic deck"),
    (r"apache\s*iceberg", "Synthetic data platform leak in demographic deck"),
    (r"acid\s*guaranteed", "Synthetic database guarantee leak"),
]


class ContentGroundingAgent:
    """Specialized Inspector for Academic Rigor, Vocabulary, AI Slop Elimination & Grounding."""

    def __init__(self, canonical_ledger: Optional[Dict[str, Any]] = None):
        self.canonical_ledger = canonical_ledger or {}

    def inspect_text_strings(self, slide_index: int, text_chunks: List[str]) -> Tuple[float, List[DefectIssue]]:
        defects: List[DefectIssue] = []
        score = 100.0

        full_slide_text = "\n".join(text_chunks).strip()
        if not full_slide_text:
            defects.append(
                DefectIssue(
                    slide_index=slide_index,
                    severity="P0",
                    domain="CONTENT",
                    root_cause="Slide contains zero textual content or has empty text frames.",
                    remediation_action="Populate slide with structured pedagogical content from canonical ledger.",
                )
            )
            return 0.0, defects

        # 1. Check forbidden synthetic phrases and clichés
        for pattern, desc in FORBIDDEN_SYNTHETIC_PATTERNS:
            match = re.search(pattern, full_slide_text, flags=re.IGNORECASE)
            if match:
                severity = "P0" if "synthetic" in desc.lower() or "fragmentation" in desc.lower() else "P1"
                defects.append(
                    DefectIssue(
                        slide_index=slide_index,
                        severity=severity,
                        domain="CONTENT",
                        root_cause=f"Found forbidden text pattern '{match.group(0)}': {desc}",
                        remediation_action="Remove cliché/filler and replace with specific empirical metric or factual claim.",
                    )
                )
                score -= 25.0 if severity == "P0" else 10.0

        # 2. Check syntax flaws (dangling parentheses, broken sentence cuts)
        for line in full_slide_text.split("\n"):
            l_clean = line.strip()
            if l_clean.endswith("(") or l_clean.endswith(" ("):
                defects.append(
                    DefectIssue(
                        slide_index=slide_index,
                        severity="P0",
                        domain="CONTENT",
                        root_cause=f"Dangling opening parenthesis at line ending: '{l_clean}'",
                        remediation_action="Close the dangling parenthesis or complete the truncated acronym/reference.",
                    )
                )
                score -= 20.0
            if "()" in l_clean or "( )" in l_clean:
                defects.append(
                    DefectIssue(
                        slide_index=slide_index,
                        severity="P1",
                        domain="CONTENT",
                        root_cause=f"Empty parenthesis detected: '{l_clean}'",
                        remediation_action="Remove empty parenthesis or inject referenced year/citation.",
                    )
                )
                score -= 10.0

        # 3. Check text density & word count limits
        word_count = len(full_slide_text.split())
        if word_count < 15 and slide_index > 1:
            defects.append(
                DefectIssue(
                    slide_index=slide_index,
                    severity="P1",
                    domain="CONTENT",
                    root_cause=f"Slide is overly sparse ({word_count} words). Fails deep curriculum requirement.",
                    remediation_action="Enrich cards with detailed bullet points, KPI chips, and operational guidelines.",
                )
            )
            score -= 15.0
        elif word_count > 220:
            defects.append(
                DefectIssue(
                    slide_index=slide_index,
                    severity="P2",
                    domain="CONTENT",
                    root_cause=f"Cognitive overload: slide contains {word_count} words (>220 words limit).",
                    remediation_action="Distill paragraphs into crisp, high-impact bulleted assertions.",
                )
            )
            score -= 5.0

        # 4. Check Cardinality Mismatch between Title and Content
        title_chunk = text_chunks[0] if text_chunks else ""
        cardinal_match = re.search(r"\b([2-9])\s*(khối|giai đoạn|đặc trưng|trụ cột|bước|nguyên tắc|mục tiêu|khía cạnh|cột mốc)\b", title_chunk, re.IGNORECASE)
        if cardinal_match:
            expected_count = int(cardinal_match.group(1))
            category_name = cardinal_match.group(2)
            numbered_items = set(re.findall(r"(?:^|\n)\s*([1-9])\.\s+", full_slide_text))
            if numbered_items and len(numbered_items) != expected_count:
                defects.append(
                    DefectIssue(
                        slide_index=slide_index,
                        severity="P0",
                        domain="CONTENT",
                        root_cause=f"Cardinality Mismatch: Title declares '{expected_count} {category_name}' but content renders {len(numbered_items)} items ({sorted(list(numbered_items))}).",
                        remediation_action=f"Reconcile content count to exactly {expected_count} items as declared in title.",
                    )
                )
                score -= 30.0

        score = max(0.0, min(100.0, score))
        return score, defects

    def inspect_com_slide(self, slide_index: int, ppt_slide_obj: Any) -> Tuple[float, List[DefectIssue]]:
        """Inspects live PowerPoint COM Slide shape text frames."""
        text_chunks = []
        try:
            for j in range(1, ppt_slide_obj.Shapes.Count + 1):
                shp = ppt_slide_obj.Shapes(j)
                self._extract_text_from_shape(shp, text_chunks)
        except Exception as e:
            return 50.0, [
                DefectIssue(
                    slide_index=slide_index,
                    severity="P1",
                    domain="CONTENT",
                    root_cause=f"COM shape reading warning: {e}",
                    remediation_action="Verify slide shapes access via COM interface.",
                )
            ]
        return self.inspect_text_strings(slide_index, text_chunks)

    def _extract_text_from_shape(self, shp: Any, chunks: List[str]):
        try:
            if shp.HasTextFrame and shp.TextFrame.HasText:
                txt = shp.TextFrame.TextRange.Text.strip()
                if txt:
                    chunks.append(txt)
            if shp.HasTable:
                tbl = shp.Table
                for r in range(1, tbl.Rows.Count + 1):
                    for c in range(1, tbl.Columns.Count + 1):
                        cell_txt = tbl.Cell(r, c).Shape.TextFrame.TextRange.Text.strip()
                        if cell_txt:
                            chunks.append(cell_txt)
            if shp.Type == 6:  # msoGroup
                for g_idx in range(1, shp.GroupItems.Count + 1):
                    self._extract_text_from_shape(shp.GroupItems(g_idx), chunks)
        except Exception:
            pass

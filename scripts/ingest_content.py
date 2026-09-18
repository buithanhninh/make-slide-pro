"""
ingest_content.py
Universal Content Ingestion & Structuring Engine for Make Slide Pro V7.3.
Parses DOCX, PDF, TXT, or MD documents into canonical content, claims, and data ledgers.
Supports table extraction, mathematical formula detection, and pedagogical hierarchy mapping.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import docx
except ImportError:
    docx = None

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    import pypdf
except ImportError:
    pypdf = None

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def clean_source_text(raw_text: str) -> str:
    """Cleans raw text, stripping robotic ellipses, normalizing spacing and quotes."""
    txt = re.sub(r"\s+", " ", raw_text).strip()
    txt = re.sub(r"\s*(\.\.\.|…)\s*$", "", txt).strip()
    return txt


def is_math_formula(text: str) -> bool:
    """Detects whether text contains a significant mathematical formula or definition."""
    clean = text.strip()
    formula_patterns = [
        r"\b[A-Za-z0-9_]{1,8}\s*=\s*[^=]+(\*|\/|\+|\-|\×|\÷|\^|\Σ|ln|exp)",
        r"\b(công thức|phương trình|đẳng thức|tính theo công thức)\s*[:=]",
        r"\b(TFR|CBR|CDR|ASFR|ASDR|IMR|U5MR|SRB|YDR|ADR|HDI|P_t|P_0|P_tb)\b\s*=",
        r"[\=]\s*[\(\[].*[\)\]]\s*[\*\/\+\-]",
    ]
    for pat in formula_patterns:
        if re.search(pat, clean, re.IGNORECASE):
            return True
    return False


def classify_semantic_role(text: str) -> str:
    """Classifies the scholarly role of a content atom."""
    lower = text.lower()
    if is_math_formula(text):
        return "MATHEMATICAL_FORMULA"
    if (("dân cư" in lower and "dân số" in lower) or 
        ("tĩnh" in lower and "động" in lower) or 
        ("hẹp" in lower and "rộng" in lower) or 
        any(k in lower for k in ["phân biệt", "khác nhau", "so với", "ngược lại", "mặt đối lập", "đối sánh", "ưu điểm vs nhược điểm"])):
        return "DIALECTICAL_PAIR"
    if any(k in lower for k in ["khái niệm", "định nghĩa", "được hiểu là", "là một môn khoa học", "là môn học", "nghĩa vụ của", "bản chất là"]):
        return "CORE_DEFINITION"
    if bool(re.search(r"\b\d+([.,]\d+)?\s*(%|người|triệu|tỷ|năm|thế kỷ|‰|usd|km2|km²)\b", text)) or any(k in lower for k in ["tỷ lệ", "tỷ số", "thống kê", "số liệu", "chỉ số"]):
        return "STATISTICAL_EVIDENCE"
    if any(k in lower for k in ["quy luật", "cơ chế", "tác động", "ảnh hưởng", "nguyên nhân", "hậu quả", "mối quan hệ", "xu hướng", "vận động", "chuyển dịch", "bước 1", "bước 2", "giai đoạn"]):
        return "DYNAMIC_MECHANISM"
    if any(k in lower for k in ["chính sách", "chiến lược", "giải pháp", "ứng phó", "an sinh", "phát triển bền vững", "kiến nghị", "mục tiêu", "định hướng", "hành động"]):
        return "STRATEGIC_IMPLICATION"
    return "BACKGROUND_CONTEXT"


class ContentIngestor:
    """Universal multi-format document ingestor for Word, PDF, Text, and Markdown."""

    def ingest_document(self, file_path: Path) -> Dict[str, Any]:
        file_path = Path(file_path)
        suffix = file_path.suffix.lower()
        if suffix in [".docx", ".doc"]:
            return self.ingest_docx(file_path)
        elif suffix == ".pdf":
            return self.ingest_pdf(file_path)
        elif suffix in [".txt", ".md", ".markdown"]:
            return self.ingest_text(file_path)
        else:
            try:
                return self.ingest_text(file_path)
            except Exception:
                raise ValueError(f"Unsupported file format: {suffix} for {file_path}")

    def ingest_docx(self, file_path: Path) -> Dict[str, Any]:
        if not docx:
            raise RuntimeError("python-docx is required for docx ingestion. Run 'pip install python-docx'.")

        doc = docx.Document(str(file_path))
        sections: List[Dict[str, Any]] = []
        current_section = {
            "section_id": "SEC_00",
            "title": file_path.stem.replace("_", " "),
            "level": 1,
            "paragraphs": [],
            "atoms": []
        }

        sec_counter = 0
        atom_counter = 0

        for p in doc.paragraphs:
            text = clean_source_text(p.text)
            if not text:
                continue

            style = p.style.name.lower()
            is_heading_style = "heading" in style
            is_heading_pattern = bool(re.match(r"^(Chương|Bài|Phần|Mục|[I|V|X]+\.|\d+\.|\d+\.\d+)\s+[A-ZÀ-Ỹ]", text))
            is_bold_short = len(text) < 90 and any(r.bold for r in p.runs if r.text.strip())

            if is_heading_style or is_heading_pattern or is_bold_short:
                if current_section["paragraphs"] or current_section["atoms"]:
                    sections.append(current_section)
                sec_counter += 1
                level = 1
                if "heading 2" in style or bool(re.match(r"^\d+\.\d+\s+", text)):
                    level = 2
                elif "heading 3" in style or bool(re.match(r"^\d+\.\d+\.\d+\s+", text)):
                    level = 3
                current_section = {
                    "section_id": f"SEC_{sec_counter:02d}",
                    "title": text,
                    "level": level,
                    "paragraphs": [],
                    "atoms": []
                }
            else:
                current_section["paragraphs"].append(text)
                atom_counter += 1

                semantic_role = classify_semantic_role(text)
                is_formula = (semantic_role == "MATHEMATICAL_FORMULA")
                
                if semantic_role in ["CORE_DEFINITION", "DIALECTICAL_PAIR", "MATHEMATICAL_FORMULA"] or any(k in text.lower() for k in ["mục tiêu", "nguyên tắc", "cốt lõi"]):
                    priority = "P0"
                elif any(k in text.lower() for k in ["chẳng hạn", "ví dụ", "minh họa:"]):
                    priority = "P2"
                else:
                    priority = "P1"

                atom = {
                    "atom_id": f"ATOM_{atom_counter:03d}",
                    "section_id": current_section["section_id"],
                    "priority": priority,
                    "semantic_role": semantic_role,
                    "verbatim": text,
                    "normalized": text,
                    "sha256": sha256_text(text),
                    "is_formula": is_formula,
                    "contains_metric": bool(re.search(r"\b\d+([.,]\d+)?\s*(%|người|triệu|tỷ|năm|thế kỷ|‰)?\b", text)),
                    "destination": "VISIBLE_SLIDE"
                }
                current_section["atoms"].append(atom)

        # Ingest Tables from docx
        table_counter = 0
        for tbl in doc.tables:
            if not tbl.rows:
                continue
            headers = [clean_source_text(cell.text) for cell in tbl.rows[0].cells]
            clean_headers = []
            seen = set()
            for h in headers:
                val = h or f"Cột {len(clean_headers)+1}"
                if val in seen:
                    val = f"{val}_{len(clean_headers)+1}"
                seen.add(val)
                clean_headers.append(val)

            rows_data = []
            for row in tbl.rows[1:]:
                row_vals = [clean_source_text(cell.text) for cell in row.cells]
                if any(row_vals):
                    rows_data.append(row_vals)

            if clean_headers and rows_data:
                table_counter += 1
                atom_counter += 1
                col_w = round(1.0 / len(clean_headers), 2)
                col_widths = [col_w] * len(clean_headers)

                table_atom = {
                    "atom_id": f"ATOM_{atom_counter:03d}",
                    "section_id": current_section["section_id"],
                    "priority": "P0",
                    "semantic_role": "TABLE_MATRIX",
                    "verbatim": f"Dữ liệu bảng tổng hợp {len(clean_headers)} cột và {len(rows_data)} dòng.",
                    "normalized": "Bảng số liệu tổng hợp",
                    "sha256": sha256_text(str(rows_data)),
                    "is_table": True,
                    "table_data": {
                        "headers": clean_headers,
                        "rows": rows_data[:8],
                        "col_widths": col_widths
                    },
                    "destination": "VISIBLE_SLIDE"
                }
                current_section["atoms"].append(table_atom)

        if current_section["paragraphs"] or current_section["atoms"]:
            sections.append(current_section)

        return self._finalize_ledgers(file_path, sections)

    def ingest_pdf(self, file_path: Path) -> Dict[str, Any]:
        """Ingests text content and structure from a PDF file using PyMuPDF or pypdf."""
        sections: List[Dict[str, Any]] = []
        current_section = {
            "section_id": "SEC_00",
            "title": file_path.stem.replace("_", " "),
            "level": 1,
            "paragraphs": [],
            "atoms": []
        }

        full_text_lines = []
        if fitz:
            doc = fitz.open(str(file_path))
            for page in doc:
                text = page.get_text("text")
                for line in text.splitlines():
                    cl = clean_source_text(line)
                    if cl:
                        full_text_lines.append(cl)
            doc.close()
        elif pypdf:
            reader = pypdf.PdfReader(str(file_path))
            for page in reader.pages:
                text = page.extract_text() or ""
                for line in text.splitlines():
                    cl = clean_source_text(line)
                    if cl:
                        full_text_lines.append(cl)
        else:
            raise RuntimeError("Neither PyMuPDF (fitz) nor pypdf is installed.")

        sec_counter = 0
        atom_counter = 0

        for line in full_text_lines:
            is_heading_pattern = bool(re.match(r"^(Chương|Bài|Phần|Mục|[I|V|X]+\.|\d+\.|\d+\.\d+)\s+[A-ZÀ-Ỹ]", line))
            is_all_caps = line.isupper() and 10 < len(line) < 80

            if is_heading_pattern or is_all_caps:
                if current_section["paragraphs"] or current_section["atoms"]:
                    sections.append(current_section)
                sec_counter += 1
                current_section = {
                    "section_id": f"SEC_{sec_counter:02d}",
                    "title": line,
                    "level": 1 if (is_all_caps or re.match(r"^[I|V|X]+\.", line)) else 2,
                    "paragraphs": [],
                    "atoms": []
                }
            else:
                current_section["paragraphs"].append(line)
                atom_counter += 1
                semantic_role = classify_semantic_role(line)
                is_formula = (semantic_role == "MATHEMATICAL_FORMULA")
                
                atom = {
                    "atom_id": f"ATOM_{atom_counter:03d}",
                    "section_id": current_section["section_id"],
                    "priority": "P0" if is_formula or semantic_role in ["CORE_DEFINITION", "DIALECTICAL_PAIR"] else "P1",
                    "semantic_role": semantic_role,
                    "verbatim": line,
                    "normalized": line,
                    "sha256": sha256_text(line),
                    "is_formula": is_formula,
                    "contains_metric": bool(re.search(r"\b\d+([.,]\d+)?\s*(%|người|triệu|tỷ|năm|thế kỷ|‰)?\b", line)),
                    "destination": "VISIBLE_SLIDE"
                }
                current_section["atoms"].append(atom)

        if current_section["paragraphs"] or current_section["atoms"]:
            sections.append(current_section)

        return self._finalize_ledgers(file_path, sections)

    def ingest_text(self, file_path: Path) -> Dict[str, Any]:
        """Ingests plain text or Markdown files."""
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        sections: List[Dict[str, Any]] = []
        current_section = {
            "section_id": "SEC_00",
            "title": file_path.stem.replace("_", " "),
            "level": 1,
            "paragraphs": [],
            "atoms": []
        }

        sec_counter = 0
        atom_counter = 0

        for line in content.splitlines():
            line_str = clean_source_text(line)
            if not line_str:
                continue

            is_md_header = line_str.startswith("#")
            is_num_header = bool(re.match(r"^(Chương|Bài|Phần|Mục|[I|V|X]+\.|\d+\.|\d+\.\d+)\s+[A-ZÀ-Ỹ]", line_str))

            if is_md_header or is_num_header:
                if current_section["paragraphs"] or current_section["atoms"]:
                    sections.append(current_section)
                sec_counter += 1
                clean_title = re.sub(r"^#+\s*", "", line_str)
                current_section = {
                    "section_id": f"SEC_{sec_counter:02d}",
                    "title": clean_title,
                    "level": 1 if line_str.startswith("# ") else 2,
                    "paragraphs": [],
                    "atoms": []
                }
            else:
                current_section["paragraphs"].append(line_str)
                atom_counter += 1
                semantic_role = classify_semantic_role(line_str)
                is_formula = (semantic_role == "MATHEMATICAL_FORMULA")

                atom = {
                    "atom_id": f"ATOM_{atom_counter:03d}",
                    "section_id": current_section["section_id"],
                    "priority": "P0" if is_formula or semantic_role in ["CORE_DEFINITION", "DIALECTICAL_PAIR"] else "P1",
                    "semantic_role": semantic_role,
                    "verbatim": line_str,
                    "normalized": line_str,
                    "sha256": sha256_text(line_str),
                    "is_formula": is_formula,
                    "contains_metric": bool(re.search(r"\b\d+([.,]\d+)?\s*(%|người|triệu|tỷ|năm|thế kỷ|‰)?\b", line_str)),
                    "destination": "VISIBLE_SLIDE"
                }
                current_section["atoms"].append(atom)

        if current_section["paragraphs"] or current_section["atoms"]:
            sections.append(current_section)

        return self._finalize_ledgers(file_path, sections)

    def _finalize_ledgers(self, file_path: Path, sections: List[Dict[str, Any]]) -> Dict[str, Any]:
        all_atoms = [atom for sec in sections for atom in sec.get("atoms", [])]

        metrics = []
        metric_counter = 0
        for sec in sections:
            for atom in sec.get("atoms", []):
                matches = re.finditer(r"\b(\d+([.,]\d+)?)\s*(%|người|tiết|năm|thế kỷ|‰|usd|tỷ|triệu)?\b", atom["verbatim"])
                for m in matches:
                    val_str = m.group(1)
                    unit_str = m.group(3) or ""
                    metric_counter += 1
                    metrics.append({
                        "metric_id": f"MET_{metric_counter:03d}",
                        "atom_id": atom["atom_id"],
                        "raw_value": val_str,
                        "unit": unit_str,
                        "context": atom["verbatim"][:120]
                    })

        try:
            file_bytes = file_path.read_bytes()
            sha256 = sha256_text(file_bytes.decode("latin1", errors="ignore"))
        except Exception:
            sha256 = "N/A"

        canonical_content = {
            "schema_version": "1.0",
            "source_path": str(file_path),
            "source_sha256": sha256,
            "total_sections": len(sections),
            "total_atoms": len(all_atoms),
            "sections": sections
        }

        claim_ledger = {
            "schema_version": "1.0",
            "source_path": str(file_path),
            "claims": [
                {
                    "claim_id": f"CLM_{i+1:03d}",
                    "atom_id": atom["atom_id"],
                    "priority": atom["priority"],
                    "statement": atom["verbatim"],
                    "verified": True
                }
                for i, atom in enumerate(all_atoms)
            ]
        }

        data_ledger = {
            "schema_version": "1.0",
            "source_path": str(file_path),
            "metrics": metrics
        }

        return {
            "canonical_content": canonical_content,
            "claim_ledger": claim_ledger,
            "data_ledger": data_ledger
        }


def main():
    parser = argparse.ArgumentParser(description="Universal Content Ingestion for Make Slide Pro")
    parser.add_argument("--input", required=True, type=Path, help="Input source document (.docx, .pdf, .txt, .md)")
    parser.add_argument("--output-dir", required=True, type=Path, help="Output directory for ledgers")
    args = parser.parse_args()

    ingestor = ContentIngestor()
    results = ingestor.ingest_document(args.input)

    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(out_dir / "canonical-content.json", "w", encoding="utf-8") as f:
        json.dump(results["canonical_content"], f, ensure_ascii=False, indent=2)

    with open(out_dir / "claim-ledger.json", "w", encoding="utf-8") as f:
        json.dump(results["claim_ledger"], f, ensure_ascii=False, indent=2)

    with open(out_dir / "data-ledger.json", "w", encoding="utf-8") as f:
        json.dump(results["data_ledger"], f, ensure_ascii=False, indent=2)

    print(f"✔ Universal Ingestion complete: {results['canonical_content']['total_atoms']} atoms, {len(results['data_ledger']['metrics'])} metrics extracted.")


if __name__ == "__main__":
    main()

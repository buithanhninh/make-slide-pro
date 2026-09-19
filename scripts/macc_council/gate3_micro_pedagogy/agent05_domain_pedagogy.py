"""
scripts/macc_council/gate3_micro_pedagogy/agent05_domain_pedagogy.py
Agent 5: DomainPedagogyScholar (Domain Pedagogy & Scientific Factuality).
Audits domain accuracy, concept rigor, and professional technical jargon definitions.
Hardened with comprehensive domain ontology, semantic distance extraction, and auto-remediation.
"""

from __future__ import annotations

import copy
import re
from typing import Any, Dict, List, Optional, Tuple
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, Severity


class DomainPedagogyScholar(BaseCouncilAgent):
    """
    Agent 05: Domain Pedagogy Scholar.
    Ensures pedagogical clarity, scientific/economic rigor, and domain-appropriate terminology.
    Prevents false technical equivalences and misattributed domain concepts across macroeconomics,
    demographics, banking, and deep technology.
    """

    # Domain ontology rules: (metric_identifier_regex, forbidden_unit_regex, reason, correct_unit, auto_replace_pattern)
    DOMAIN_RULES: List[Dict[str, Any]] = [
        {
            "id": "gdp_per_capita",
            "concept_name": "GDP bình quân đầu người",
            "concept_regex": re.compile(r"\b(gdp\s+bình\s+quân\s+đầu\s+người|thu\s+nhập\s+bình\s+quân\s+đầu\s+người|gdp\/người|gdp\s+per\s+capita)\b", re.IGNORECASE),
            # Forbidden: billions/trillions USD or VND, or millions USD (impossible per capita). Does NOT flag valid '105 triệu VNĐ/người' or '4.300 USD/người'.
            "forbidden_regex": re.compile(r"(\b\d+(?:[.,]\d+)?\s*(?:tỷ|tỉ|nghìn\s*tỷ)\s*(?:usd|vnđ|đồng)|\b\d+(?:[.,]\d+)?\s*triệu\s*usd)", re.IGNORECASE),
            "reason": "GDP bình quân đầu người không thể tính bằng hàng tỷ USD/đồng mà tính theo USD/người/năm hoặc triệu VNĐ/người.",
            "correct_unit": "USD/người",
            "replace_func": lambda s: re.sub(r"(tỷ|tỉ|nghìn\s*tỷ)\s*usd", "USD/người", s, flags=re.IGNORECASE)
        },
        {
            "id": "total_fertility_rate",
            "concept_name": "Tỷ suất sinh thay thế (TFR)",
            "concept_regex": re.compile(r"\b(tỷ\s+suất\s+sinh\s+thay\s+thế|mức\s+sinh\s+thay\s+thế|tỷ\s+suất\s+sinh|tfr)\b", re.IGNORECASE),
            "forbidden_regex": re.compile(r"(\b\d+(?:[.,]\d+)?\s*%)", re.IGNORECASE),
            "reason": "Tỷ suất sinh thay thế (TFR) đo bằng số con/phụ nữ (chuẩn là 2,1 con/phụ nữ), không đo bằng tỷ lệ phần trăm (%).",
            "correct_unit": "con/phụ nữ",
            "replace_func": lambda s: re.sub(r"(\d+(?:[.,]\d+)?)\s*%", r"\1 con/phụ nữ", s)
        },
        {
            "id": "life_expectancy",
            "concept_name": "Tuổi thọ trung bình",
            "concept_regex": re.compile(r"\b(tuổi\s+thọ\s+trung\s+bình|kỳ\s+vọng\s+sống\s+bình\s+quân|tuổi\s+thọ\s+bình\s+quân)\b", re.IGNORECASE),
            "forbidden_regex": re.compile(r"(\b\d+(?:[.,]\d+)?\s*%)", re.IGNORECASE),
            "reason": "Tuổi thọ trung bình đo bằng số tuổi (năm), không đo bằng phần trăm (%).",
            "correct_unit": "tuổi",
            "replace_func": lambda s: re.sub(r"(\d+(?:[.,]\d+)?)\s*%", r"\1 tuổi", s)
        },
        {
            "id": "semiconductor_node",
            "concept_name": "Tiến trình bán dẫn / đúc chip",
            "concept_regex": re.compile(r"(?:\b(?:tiến\s+trình|node|công\s+nghệ)\b.*?\b(?:bán\s+dẫn|đúc\s+chip|chip|vi\s+mạch)\b|\b(?:bán\s+dẫn|đúc\s+chip|chip|vi\s+mạch)\b.*?\b(?:tiến\s+trình|node)\b)", re.IGNORECASE),
            "forbidden_regex": re.compile(r"(\b\d+(?:[.,]\d+)?\s*(?:ghz|mhz|gb|tb|mm|cm)\b)", re.IGNORECASE),
            "reason": "Tiến trình công nghệ bán dẫn đo bằng nanomet (nm) hoặc angstrom (A), không đo bằng tần số (GHz) hay dung lượng.",
            "correct_unit": "nm",
            "replace_func": lambda s: re.sub(r"(\d+(?:[.,]\d+)?)\s*(?:ghz|mhz|gb|tb|mm|cm)\b", r"\1 nm", s, flags=re.IGNORECASE)
        },
        {
            "id": "npl_ratio",
            "concept_name": "Tỷ lệ nợ xấu (NPL)",
            "concept_regex": re.compile(r"\b(tỷ\s+lệ\s+nợ\s+xấu|tỷ\s+lệ\s+npl|tỷ\s+trọng\s+nợ\s+xấu|nợ\s+xấu\s*\(?\s*npl\s*\)?)\b", re.IGNORECASE),
            "forbidden_regex": re.compile(r"(\b\d+(?:[.,]\d+)?\s*(?:tỷ|tỉ|nghìn\s*tỷ|triệu)\s*(?:đồng|vnđ|usd)\b)", re.IGNORECASE),
            "reason": "Tỷ lệ nợ xấu (NPL ratio) là một tỷ lệ tương đối đo bằng phần trăm (%), không thể đo bằng số tiền tuyệt đối.",
            "correct_unit": "%",
            "replace_func": lambda s: re.sub(r"(tỷ|tỉ|nghìn\s*tỷ|triệu)\s*(?:đồng|vnđ|usd)\b", "%", s, flags=re.IGNORECASE)
        },
        {
            "id": "forex_reserves",
            "concept_name": "Dự trữ ngoại hối",
            "concept_regex": re.compile(r"\b(dự\s+trữ\s+ngoại\s+hối|dự\s+trữ\s+ngoại\s+tệ)\b", re.IGNORECASE),
            "forbidden_regex": re.compile(r"(\b\d+(?:[.,]\d+)?\s*%)", re.IGNORECASE),
            "reason": "Dự trữ ngoại hối đo bằng lượng giá trị tiền tệ thực tế (thường là tỷ USD), không đo bằng phần trăm (%).",
            "correct_unit": "tỷ USD",
            "replace_func": lambda s: re.sub(r"(\d+(?:[.,]\d+)?)\s*%", r"\1 tỷ USD", s)
        }
    ]

    def __init__(self):
        super().__init__(name="DomainPedagogyScholar", gate="Gate 3: Micro-Pedagogy & Scientific Precision")

    def _get_slides(self, target: Any) -> List[Dict[str, Any]]:
        if isinstance(target, list):
            return target
        if isinstance(target, dict):
            return target.get("slides", [target])
        return []

    def _split_clauses(self, text: str) -> List[str]:
        # Decimal-safe sentence splitting: don't split on dots or commas surrounded by digits
        return [c.strip() for c in re.split(r"(?<!\d)[.?!;\n]+(?!\d)", text) if c.strip()]

    def audit(self, target: Any, context: Optional[Dict[str, Any]] = None) -> List[AgentFinding]:
        findings: List[AgentFinding] = []
        slides = self._get_slides(target)

        for s in slides:
            slide_id = s.get("slide_id", "unknown_slide")
            slide_text = self.extract_slide_text(s)
            clauses = self._split_clauses(slide_text)

            # Check each clause for domain rules
            for clause in clauses:
                for rule in self.DOMAIN_RULES:
                    concept_match = rule["concept_regex"].search(clause)
                    if not concept_match:
                        # Also check if concept and forbidden match are in the same clause
                        continue

                    # If nominal GDP is mentioned, ensure it's not confused with per capita
                    if rule["id"] == "gdp_per_capita":
                        # Must strictly match per capita phrases
                        if not re.search(r"\b(bình\s+quân\s+đầu\s+người|thu\s+nhập\s+bình\s+quân|đầu\s+người|per\s+capita)\b", clause, re.IGNORECASE):
                            continue

                    forbidden_match = rule["forbidden_regex"].search(clause)
                    if forbidden_match:
                        concept_name = rule["concept_name"]
                        evidence = clause
                        erroneous_value = forbidden_match.group(0)
                        correct_val = rule["replace_func"](erroneous_value)

                        findings.append(
                            AgentFinding(
                                agent=self.name,
                                gate=self.gate,
                                slide_id=slide_id,
                                severity=Severity.P1,
                                issue=f"Sai lệch khái niệm / đơn vị chuyên ngành: '{concept_name}'",
                                rationale=rule["reason"],
                                suggestion=f"Hiệu chỉnh đơn vị đo lường của '{concept_name}' sang '{rule['correct_unit']}'.",
                                evidence=evidence,
                                original_value=erroneous_value,
                                suggested_value=correct_val
                            )
                        )

        return findings

    def auto_remediate(self, target: Any, findings: List[AgentFinding], context: Optional[Dict[str, Any]] = None) -> Any:
        """
        Auto-remediates domain concept & unit mismatches.
        Corrects erroneous units in slide texts, titles, cards, and body items while preserving figures.
        """
        remediated_target = copy.deepcopy(target)
        slides = self._get_slides(remediated_target)

        # Build map of (slide_id, original_value) -> suggested_value
        fix_map: Dict[Tuple[str, str], str] = {}
        for f in findings:
            if f.agent == self.name and f.original_value and f.suggested_value:
                fix_map[(f.slide_id, f.original_value)] = f.suggested_value

        if not fix_map:
            return remediated_target

        for s in slides:
            slide_id = s.get("slide_id", "unknown_slide")

            def _clean_text(text: str) -> str:
                if not isinstance(text, str):
                    return text
                new_text = text
                for (sid, orig_val), sugg_val in fix_map.items():
                    if sid == slide_id and orig_val in new_text:
                        new_text = new_text.replace(orig_val, sugg_val)
                    # Also try rule replacement directly if concept is present
                    for rule in self.DOMAIN_RULES:
                        if rule["concept_regex"].search(new_text):
                            forb = rule["forbidden_regex"].search(new_text)
                            if forb:
                                new_text = new_text.replace(forb.group(0), rule["replace_func"](forb.group(0)))
                return new_text

            for k in ["title", "subtitle", "assertion_title", "primary_claim", "speaker_notes", "headline"]:
                if k in s and isinstance(s[k], str):
                    s[k] = _clean_text(s[k])

            for col_key in ["atoms", "cards", "content_items", "boxes", "items"]:
                for item in s.get(col_key, []):
                    if isinstance(item, dict):
                        for field in ["title", "body", "text", "description", "label", "value", "verbatim", "mechanism", "kicker", "metric_value", "metric_label"]:
                            if field in item and isinstance(item[field], str):
                                item[field] = _clean_text(item[field])

            table = s.get("table_data")
            if isinstance(table, dict):
                headers = table.get("headers", [])
                if isinstance(headers, list):
                    table["headers"] = [_clean_text(h) if isinstance(h, str) else h for h in headers]
                rows = table.get("rows", [])
                if isinstance(rows, list):
                    for r in rows:
                        if isinstance(r, list):
                            for idx, cell in enumerate(r):
                                if isinstance(cell, str):
                                    r[idx] = _clean_text(cell)

        return remediated_target

"""
scripts/macc_council/base_agent.py
Abstract Base Agent definition for all specialized council inspectors.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from .models import AgentFinding, Severity


class BaseCouncilAgent(ABC):
    """Abstract Base Class for all 16 Specialized Council Agents."""

    def __init__(self, name: str, gate: str):
        self.name = name
        self.gate = gate

    @abstractmethod
    def audit(self, target: Any, context: Optional[Dict[str, Any]] = None) -> List[AgentFinding]:
        """
        Audits a slide or entire deck against the agent's strict specialized criteria.
        Returns a list of AgentFinding objects.
        """
        pass

    def auto_remediate(self, target: Any, findings: List[AgentFinding], context: Optional[Dict[str, Any]] = None) -> Any:
        """
        Optionally repairs the target in-place based on the detected findings.
        Returns the remediated target.
        """
        return target

    def extract_slide_text(self, slide: Dict[str, Any]) -> str:
        """Helper to extract all searchable textual content safely from a slide dictionary across all blueprint schemas."""
        if not isinstance(slide, dict):
            return ""

        texts: List[str] = []
        for k in ["assertion_title", "title", "headline", "primary_claim", "subtitle", "section", "speaker_notes"]:
            val = slide.get(k)
            if val and isinstance(val, str):
                texts.append(val)

        # Blueprint atoms
        atoms = slide.get("atoms")
        if isinstance(atoms, list):
            for atom in atoms:
                if isinstance(atom, dict):
                    for ak in ["title", "text", "body", "mechanism", "kicker", "tag", "metric_label"]:
                        v = atom.get(ak)
                        if v and isinstance(v, str):
                            texts.append(v)
                    mv = atom.get("metric_value")
                    if mv is not None:
                        texts.append(str(mv))
                elif atom is not None:
                    texts.append(str(atom))

        # Generic content_items / cards / boxes
        for col_key in ["content_items", "cards", "boxes", "items"]:
            col = slide.get(col_key)
            if isinstance(col, list):
                for item in col:
                    if isinstance(item, dict):
                        for ik in ["title", "body", "text", "description", "headline", "metric_label"]:
                            v = item.get(ik)
                            if v and isinstance(v, str):
                                texts.append(v)
                        mv = item.get("metric_value")
                        if mv is not None:
                            texts.append(str(mv))
                    elif item is not None:
                        texts.append(str(item))

        # Bullets
        for bk in ["bullets", "bullet_points"]:
            col = slide.get(bk)
            if isinstance(col, list):
                for b in col:
                    if b is not None:
                        texts.append(str(b))

        # Table data
        table = slide.get("table_data")
        if isinstance(table, dict):
            headers = table.get("headers")
            if isinstance(headers, list):
                texts.extend(str(h) for h in headers if h is not None)
            rows = table.get("rows")
            if isinstance(rows, list):
                for r in rows:
                    if isinstance(r, list):
                        texts.extend(str(c) for c in r if c is not None)
                    elif isinstance(r, dict):
                        texts.extend(str(v) for v in r.values() if v is not None)

        return "\n".join(t for t in texts if t)

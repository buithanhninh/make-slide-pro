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
        """Helper to extract all searchable textual content from a slide dictionary across all blueprint schemas."""
        texts = [
            slide.get("assertion_title", ""),
            slide.get("title", ""),
            slide.get("headline", ""),
            slide.get("primary_claim", ""),
            slide.get("subtitle", ""),
            slide.get("section", ""),
            slide.get("speaker_notes", "")
        ]
        # Blueprint atoms
        for atom in slide.get("atoms", []):
            if isinstance(atom, dict):
                texts.extend([
                    atom.get("title", ""),
                    atom.get("text", ""),
                    atom.get("body", ""),
                    atom.get("mechanism", ""),
                    atom.get("kicker", ""),
                    atom.get("tag", ""),
                    str(atom.get("metric_value", "")),
                    atom.get("metric_label", "")
                ])
            else:
                texts.append(str(atom))

        # Generic content_items / cards / boxes
        for item in slide.get("content_items", []) + slide.get("cards", []) + slide.get("boxes", []):
            if isinstance(item, dict):
                texts.extend([
                    item.get("title", ""),
                    item.get("body", ""),
                    item.get("text", ""),
                    item.get("description", ""),
                    item.get("headline", ""),
                    str(item.get("metric_value", "")),
                    item.get("metric_label", "")
                ])
            else:
                texts.append(str(item))

        # Bullets
        for b in slide.get("bullets", []) + slide.get("bullet_points", []):
            texts.append(str(b))

        # Table data
        table = slide.get("table_data")
        if isinstance(table, dict):
            headers = table.get("headers", [])
            if isinstance(headers, list):
                texts.extend(str(h) for h in headers if h)
            rows = table.get("rows", [])
            if isinstance(rows, list):
                for r in rows:
                    if isinstance(r, list):
                        texts.extend(str(c) for c in r if c)
                    elif isinstance(r, dict):
                        texts.extend(str(v) for v in r.values() if v)

        return "\n".join(t for t in texts if t)

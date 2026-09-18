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
        """Helper to extract all searchable textual content from a slide dictionary."""
        texts = [
            slide.get("assertion_title", ""),
            slide.get("primary_claim", ""),
            slide.get("section", ""),
            slide.get("speaker_notes", "")
        ]
        for atom in slide.get("atoms", []):
            if isinstance(atom, dict):
                texts.append(atom.get("title", ""))
                texts.append(atom.get("text", ""))
                texts.append(atom.get("mechanism", ""))
                texts.append(atom.get("kicker", ""))
                texts.append(atom.get("tag", ""))
            else:
                texts.append(str(atom))
        return "\n".join(t for t in texts if t)

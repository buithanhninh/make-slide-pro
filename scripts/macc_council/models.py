"""
scripts/macc_council/models.py
Data models and type definitions for the 16-Agent Omniscient Council (MACC-QA V8.0).
"""

from __future__ import annotations

import enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class Severity(str, enum.Enum):
    P0 = "P0"  # Blocker / Veto: Hallucination, PII leak, severe math error, contradictory data
    P1 = "P1"  # Critical: Missing proof, cognitive overload, broken narrative, visual collision
    P2 = "P2"  # Warning: Cosmetic style, minor spacing, sub-optimal layout rhythm


class AgentFinding(BaseModel):
    agent: str
    gate: str
    slide_id: str
    severity: Severity
    issue: str
    rationale: str
    suggestion: str
    evidence: Optional[str] = None
    original_value: Optional[str] = None
    suggested_value: Optional[str] = None


class GateReport(BaseModel):
    gate_name: str
    passed: bool
    findings: List[AgentFinding] = Field(default_factory=list)
    score: float = 100.0


class CouncilAuditReport(BaseModel):
    certified: bool = False
    total_rounds: int = 1
    final_score: float = 100.0
    p0_count: int = 0
    p1_count: int = 0
    p2_count: int = 0
    gate_reports: Dict[str, GateReport] = Field(default_factory=dict)
    all_findings: List[AgentFinding] = Field(default_factory=list)
    remediated_slides: Optional[List[Dict[str, Any]]] = None

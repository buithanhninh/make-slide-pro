# -*- coding: utf-8 -*-
"""
scripts/mas_engine_v9/models.py
Pydantic V2 State Contracts, Defect Specifications, and Audit Report Schemas
for Make Slide Pro V9.1 Multi-Agent Closed-Loop Self-Healing System (MAS-CLSH V9.1).
"""

from __future__ import annotations
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field

if not hasattr(BaseModel, "model_dump"):
    BaseModel.model_dump = BaseModel.dict


class DefectIssue(BaseModel):
    """Specific flaw detected on a slide with root-cause categorization and action."""
    slide_index: int = Field(description="1-based index of the slide in presentation")
    severity: Literal["P0", "P1", "P2"] = Field(
        description="P0 = Blocker/Critical (must heal), P1 = Major (quality degradation), P2 = Minor/Polish"
    )
    domain: Literal["CONTENT", "MOTION", "LAYOUT", "DATAVIZ"] = Field(
        description="Forensic domain responsible for the defect"
    )
    root_cause: str = Field(description="Explanatory root-cause identification")
    remediation_action: str = Field(description="Prescriptive action for the self-healing engine")


class SlideAuditResult(BaseModel):
    """Audit scores and defects discovered on an individual slide."""
    slide_index: int
    content_score: float = Field(default=100.0, ge=0.0, le=100.0)
    motion_score: float = Field(default=100.0, ge=0.0, le=100.0)
    layout_score: float = Field(default=100.0, ge=0.0, le=100.0)
    dataviz_score: float = Field(default=100.0, ge=0.0, le=100.0)
    overall_score: float = Field(default=100.0, ge=0.0, le=100.0)
    has_illustration: bool = False
    has_chart: bool = False
    has_table: bool = False
    defects: List[DefectIssue] = Field(default_factory=list)


class MASAuditReport(BaseModel):
    """Comprehensive presentation-wide forensic audit report."""
    deck_path: str
    total_slides: int
    overall_score: float = Field(default=100.0, ge=0.0, le=100.0)
    p0_count: int = 0
    p1_count: int = 0
    p2_count: int = 0
    illustration_count: int = 0
    illustration_ratio: float = 0.0
    chart_count: int = 0
    table_count: int = 0
    framework_count: int = 0
    slop_words_detected: List[str] = Field(default_factory=list)
    watermarks_detected: List[str] = Field(default_factory=list)
    slide_audits: Dict[int, SlideAuditResult] = Field(default_factory=dict)
    is_certified: bool = False
    audit_timestamp: Optional[str] = None


class RemediationDirective(BaseModel):
    """Actionable instruction for the surgical slide re-generator."""
    slide_index: int
    target_domain: Literal["CONTENT", "MOTION", "LAYOUT", "DATAVIZ", "CONSOLIDATED"]
    root_cause: str
    remediation_action: str
    updated_blueprint: Optional[Dict[str, Any]] = None


class MASSystemState(BaseModel):
    """Runtime State Graph Schema for Multi-Agent Closed-Loop Self-Healing."""
    iteration: int = Field(default=0, description="Current remediation cycle")
    max_iterations: int = Field(default=3, description="Hard termination invariant")
    deck_path: str
    doc_name: str = ""
    total_slides: int = 0
    slide_audits: Dict[int, SlideAuditResult] = Field(default_factory=dict)
    remediation_queue: List[int] = Field(default_factory=list)
    healed_slides: List[int] = Field(default_factory=list)
    is_converged: bool = False
    trajectory: List[str] = Field(default_factory=list)

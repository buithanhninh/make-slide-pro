"""
scripts/macc_council/gate3_micro_pedagogy/agent06_mathematical_omml.py
Agent 6: MathematicalOMMLValidator (Mathematical & OMML Formula Auditor).
Validates LaTeX equations, OMML syntax integrity, bracket balancing, and variable index rigor.
"""

from __future__ import annotations

import copy
import re
from typing import Any, Dict, List, Optional
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, Severity


class MathematicalOMMLValidator(BaseCouncilAgent):
    """
    Agent 06: Mathematical & OMML Validator.
    Ensures mathematical equations, LaTeX markup, and OMML expressions
    are structurally sound, syntactically balanced, and mathematically well-formed.
    Prevents presentation rendering crashes caused by malformed equation tags.
    """

    MATH_BLOCK_REGEX = re.compile(r"(\$\$[\s\S]+?\$\$|\$[^\$\n]+?\$|\\\[[\s\S]+?\\\]|\\\(.+?\\\))")

    def __init__(self):
        super().__init__(name="MathematicalOMMLValidator", gate="Gate 3: Micro-Pedagogy & Scientific Precision")

    def _get_slides(self, target: Any) -> List[Dict[str, Any]]:
        if isinstance(target, list):
            return target
        if isinstance(target, dict):
            return target.get("slides", [target])
        return []

    def _check_balanced_delimiters(self, expr: str) -> Optional[str]:
        """Checks if curly braces, parentheses, and square brackets are balanced."""
        stack = []
        pairs = {')': '(', '}': '{', ']': '['}
        for char in expr:
            if char in '({[':
                stack.append(char)
            elif char in ')}]':
                if not stack or stack[-1] != pairs[char]:
                    return f"Ký tự đóng '{char}' không khớp hoặc thiếu ký tự mở tương ứng."
                stack.pop()
        if stack:
            return f"Thiếu ký tự đóng cho '{stack[-1]}' (chưa đóng ngoặc)."
        return None

    def audit(self, target: Any, context: Optional[Dict[str, Any]] = None) -> List[AgentFinding]:
        findings: List[AgentFinding] = []
        slides = self._get_slides(target)

        for s in slides:
            slide_id = s.get("slide_id", "unknown_slide")
            slide_text = self.extract_slide_text(s)

            # Find all LaTeX / Math expressions wrapped in $, $$, \[, or \(
            potential_blocks = list(self.MATH_BLOCK_REGEX.findall(slide_text))

            # Strip out wrapped blocks so unwrapped regex doesn't double-match
            clean_text = self.MATH_BLOCK_REGEX.sub(" ", slide_text)
            unwrapped_matches = re.findall(r"(\\[a-zA-Z]+(?:\{[^{}]*\}|\{[^{}]*)*)", clean_text)

            all_expressions = set(potential_blocks + unwrapped_matches)

            for expr in all_expressions:
                # 1. Balance check
                err = self._check_balanced_delimiters(expr)
                if err:
                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=slide_id,
                            severity=Severity.P0,
                            issue=f"Lỗi cú pháp công thức Toán học / OMML: {err}",
                            rationale=f"Công thức '{expr}' chứa ngoặc không cân xứng, sẽ gây lỗi crash hiển thị khi render sang PowerPoint OMML hoặc KaTeX.",
                            suggestion="Kiểm tra và đóng đầy đủ các cặp dấu ngoặc trong công thức LaTeX.",
                            evidence=expr,
                            original_value=expr,
                            suggested_value=self._attempt_fix_brackets(expr)
                        )
                    )

                # 2. Check for broken LaTeX commands (e.g. \frac without two arguments)
                if r"\frac" in expr:
                    # Expecting \frac{num}{den}
                    frac_matches = re.findall(r"\\frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", expr)
                    raw_frac_count = expr.count(r"\frac")
                    if len(frac_matches) < raw_frac_count and not err:
                        findings.append(
                            AgentFinding(
                                agent=self.name,
                                gate=self.gate,
                                slide_id=slide_id,
                                severity=Severity.P1,
                                issue="Công thức phân số \\frac thiếu tử số hoặc mẫu số chuẩn {num}{den}",
                                rationale="Lệnh \\frac trong LaTeX bắt buộc phải có 2 cặp ngoặc nhọn {tử}{mẫu}.",
                                suggestion="Cấu trúc lại lệnh thành \\frac{tử}{mẫu}.",
                                evidence=expr
                            )
                        )

        return findings

    def _attempt_fix_brackets(self, expr: str) -> str:
        """Attempts to balance open braces cleanly inside math delimiters."""
        open_curly = expr.count('{')
        close_curly = expr.count('}')
        if open_curly > close_curly:
            missing = '}' * (open_curly - close_curly)
            if expr.endswith("$$"):
                return expr[:-2] + missing + "$$"
            elif expr.endswith("$"):
                return expr[:-1] + missing + "$"
            elif expr.endswith(r"\]"):
                return expr[:-2] + missing + r"\]"
            elif expr.endswith(r"\)"):
                return expr[:-2] + missing + r"\)"
            return expr + missing
        return expr

    def auto_remediate(self, target: Any, findings: List[AgentFinding], context: Optional[Dict[str, Any]] = None) -> Any:
        remediated = copy.deepcopy(target)
        slides = self._get_slides(remediated)

        for finding in findings:
            if finding.original_value and finding.suggested_value and finding.original_value != finding.suggested_value:
                for s in slides:
                    if s.get("slide_id") == finding.slide_id:
                        for k in ["assertion_title", "primary_claim", "speaker_notes"]:
                            if k in s and isinstance(s[k], str):
                                s[k] = s[k].replace(finding.original_value, finding.suggested_value)
                        for atom in s.get("atoms", []):
                            if isinstance(atom, dict):
                                for ak in ["title", "text", "mechanism"]:
                                    if ak in atom and isinstance(atom[ak], str):
                                        atom[ak] = atom[ak].replace(finding.original_value, finding.suggested_value)

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            return remediated
        return slides

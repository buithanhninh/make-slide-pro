"""
scripts/macc_council/gate3_micro_pedagogy/agent06_mathematical_omml.py
Agent 6: MathematicalOMMLValidator (Mathematical & OMML Formula Auditor).
Validates LaTeX equations, OMML syntax integrity, bracket balancing, currency shielding, and auto-remediation.
Hardened with double-superscript/subscript guards, delimiter balancing, and schema-agnostic traversal.
"""

from __future__ import annotations

import copy
import re
from typing import Any, Dict, List, Optional, Tuple
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, Severity


class MathematicalOMMLValidator(BaseCouncilAgent):
    """
    Agent 06: Mathematical & OMML Validator.
    Ensures mathematical equations, LaTeX markup, and OMML expressions
    are structurally sound, syntactically balanced, and mathematically well-formed.
    Prevents presentation rendering crashes caused by malformed equation tags or unclosed delimiters.
    """

    # Matches financial currency mentions like $150, $45M, $2.5 billion
    CURRENCY_REGEX = re.compile(
        r"(?<!\\)\$(\d+(?:[.,]\d+)?\s*(?:[kKmMbBtT]|triệu|tỷ|nghìn|tỉ|million|billion|trillion)?\b)"
    )

    # Standard balanced math blocks
    MATH_BLOCK_REGEX = re.compile(
        r"(\$\$[\s\S]+?\$\$|(?<!\\)\$(?!\d)[^\$\n]+?(?<!\\)\$|\\\[[\s\S]+?\\\]|\\\(.+?\\\))"
    )

    def __init__(self):
        super().__init__(name="MathematicalOMMLValidator", gate="Gate 3: Micro-Pedagogy & Scientific Precision")

    def _get_slides(self, target: Any) -> List[Dict[str, Any]]:
        if isinstance(target, list):
            return target
        if isinstance(target, dict):
            return target.get("slides", [target])
        return []

    def _shield_currencies(self, text: str) -> Tuple[str, List[Tuple[str, str]]]:
        """Temporarily replaces financial currency strings ($150M) with placeholder tokens."""
        shields: List[Tuple[str, str]] = []
        def _repl(m: re.Match) -> str:
            token = f"__CURRENCY_TOKEN_{len(shields)}__"
            shields.append((token, m.group(0)))
            return token
        shielded_text = self.CURRENCY_REGEX.sub(_repl, text)
        return shielded_text, shields

    def _check_balanced_delimiters(self, expr: str) -> Optional[str]:
        """Checks if curly braces, parentheses, and square brackets are balanced, exempting standard half-open intervals."""
        # Check if expr is a valid mathematical interval like [0, 1) or (a, b]
        clean_expr = expr.strip("$ \t\r\n")
        if re.match(r"^[\(\[]\s*[^,\(\)\[\]]+\s*,\s*[^,\(\)\[\]]+\s*[\)\]]$", clean_expr):
            return None

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

    def _parse_brace_group(self, s: str, start: int) -> Optional[Tuple[str, int]]:
        """Parses a balanced {content} starting at or after start index. Returns (content, end_idx) or None."""
        idx = start
        while idx < len(s) and s[idx].isspace():
            idx += 1
        if idx >= len(s) or s[idx] != '{':
            return None
        depth = 0
        content_start = idx + 1
        for i in range(idx, len(s)):
            if s[i] == '{' and (i == 0 or s[i - 1] != '\\'):
                depth += 1
            elif s[i] == '}' and (i == 0 or s[i - 1] != '\\'):
                depth -= 1
                if depth == 0:
                    return s[content_start:i], i + 1
        return None

    def _validate_frac_arguments(self, expr: str) -> bool:
        """Verifies that every \\frac in expr has two well-formed brace groups {num}{den}, supporting arbitrary nesting."""
        pos = 0
        while True:
            pos = expr.find(r"\frac", pos)
            if pos == -1:
                break
            end_cmd = pos + 5
            if end_cmd < len(expr) and expr[end_cmd].isalpha():
                pos = end_cmd
                continue
            g1 = self._parse_brace_group(expr, end_cmd)
            if not g1:
                return False
            g2 = self._parse_brace_group(expr, g1[1])
            if not g2:
                return False
            pos = end_cmd
        return True

    def _check_unclosed_math_delimiters(self, text: str) -> List[Tuple[str, str, str]]:
        """
        Detects unclosed math delimiters in slide text.
        Returns list of (delimiter_name, unclosed_snippet, suggestion).
        """
        issues = []
        # Check unclosed $$
        double_dollar_count = text.count("$$")
        if double_dollar_count % 2 != 0:
            last_pos = text.rfind("$$")
            snippet = text[last_pos:min(len(text), last_pos + 60)]
            issues.append(("$$", snippet, "Bổ sung ký tự đóng '$$' cho khối công thức toán học."))

        # Check unclosed \[ and \]
        open_bracket_math = text.count(r"\[")
        close_bracket_math = text.count(r"\]")
        if open_bracket_math > close_bracket_math:
            last_pos = text.rfind(r"\[")
            snippet = text[last_pos:min(len(text), last_pos + 60)]
            issues.append((r"\[", snippet, r"Bổ sung ký tự đóng '\]' cho công thức block math."))

        # Check unclosed \( and \)
        open_paren_math = text.count(r"\(")
        close_paren_math = text.count(r"\)")
        if open_paren_math > close_paren_math:
            last_pos = text.rfind(r"\(")
            snippet = text[last_pos:min(len(text), last_pos + 60)]
            issues.append((r"\(", snippet, r"Bổ sung ký tự đóng '\)' cho công thức inline math."))

        # Check unclosed single $ (excluding $$)
        text_without_double_dollar = text.replace("$$", "")
        # Filter escaped dollars \$
        raw_dollars = [m.start() for m in re.finditer(r"(?<!\\)\$", text_without_double_dollar)]
        if len(raw_dollars) % 2 != 0:
            last_pos = raw_dollars[-1]
            snippet = text_without_double_dollar[last_pos:min(len(text_without_double_dollar), last_pos + 60)]
            issues.append(("$", snippet, "Bổ sung ký tự đóng '$' cho công thức inline math."))

        return issues

    def audit(self, target: Any, context: Optional[Dict[str, Any]] = None) -> List[AgentFinding]:
        findings: List[AgentFinding] = []
        slides = self._get_slides(target)

        for s in slides:
            slide_id = s.get("slide_id", "unknown_slide")
            slide_text = self.extract_slide_text(s)

            # 1. Shield financial currencies first to prevent false positives ($150M)
            shielded_text, _ = self._shield_currencies(slide_text)

            # 2. Check unclosed global math delimiters ($$, \[, \(, $)
            unclosed_delimiters = self._check_unclosed_math_delimiters(shielded_text)
            for delim, snippet, sugg in unclosed_delimiters:
                findings.append(
                    AgentFinding(
                        agent=self.name,
                        gate=self.gate,
                        slide_id=slide_id,
                        severity=Severity.P0,
                        issue=f"Lỗi thiếu ký tự đóng delimiter toán học '{delim}'",
                        rationale=f"Khối công thức '{snippet}...' mở bằng '{delim}' nhưng không có ký tự đóng, sẽ gây crash khi render slide.",
                        suggestion=sugg,
                        evidence=snippet,
                        original_value=snippet,
                        suggested_value=snippet + delim
                    )
                )

            # 3. Find all well-delimited math expressions
            potential_blocks = list(self.MATH_BLOCK_REGEX.findall(shielded_text))

            # Strip out wrapped blocks so unwrapped command regex doesn't duplicate
            clean_text = self.MATH_BLOCK_REGEX.sub(" ", shielded_text)
            unwrapped_matches = re.findall(r"(\\[a-zA-Z]+(?:\{[^{}]*\}|\{[^{}]*)*)", clean_text)

            all_expressions = set(potential_blocks + unwrapped_matches)

            for expr in all_expressions:
                # Delimiter balance check
                err = self._check_balanced_delimiters(expr)
                if err:
                    fixed_expr = self._attempt_fix_brackets(expr)
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
                            suggested_value=fixed_expr
                        )
                    )

                # Check for broken \frac (needs two arguments {num}{den})
                if r"\frac" in expr and not err:
                    if not self._validate_frac_arguments(expr):
                        findings.append(
                            AgentFinding(
                                agent=self.name,
                                gate=self.gate,
                                slide_id=slide_id,
                                severity=Severity.P1,
                                issue="Công thức phân số \\frac thiếu tử số hoặc mẫu số chuẩn {num}{den}",
                                rationale="Lệnh \\frac trong LaTeX bắt buộc phải có 2 cặp ngoặc nhọn {tử}{mẫu}.",
                                suggestion="Cấu trúc lại lệnh thành \\frac{tử}{mẫu}.",
                                evidence=expr,
                                original_value=expr,
                                suggested_value=re.sub(r"\\frac\s*\{([^{}]+)\}(?!\{)", r"\\frac{\1}{1}", expr)
                            )
                        )

                # Check for double superscripts / subscripts without grouping (e.g. x^2^3 or a_i_j)
                double_super = re.search(r"(\w+\^[^{}\s\+\-\*\/\=\<\>\,\;]+\^[^{}\s\+\-\*\/\=\<\>\,\;]+)", expr)
                double_sub = re.search(r"(\w+\_[^{}\s\+\-\*\/\=\<\>\,\;]+\_[^{}\s\+\-\*\/\=\<\>\,\;]+)", expr)
                if double_super or double_sub:
                    bad_item = double_super.group(0) if double_super else double_sub.group(0) # type: ignore
                    fixed_item = self._fix_double_scripts(bad_item)
                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=slide_id,
                            severity=Severity.P1,
                            issue=f"Lỗi cú pháp lũy thừa / chỉ số liên tiếp không có ngoặc nhọn: '{bad_item}'",
                            rationale="PowerPoint OMML và KaTeX không chấp nhận x^a^b hoặc a_i_j liên tiếp mà bắt buộc phải nhóm {}.",
                            suggestion=f"Nhóm lại bằng ngoặc nhọn: '{fixed_item}'.",
                            evidence=expr,
                            original_value=bad_item,
                            suggested_value=fixed_item
                        )
                    )

                # Check for trailing unescaped backslash inside math block
                if re.search(r"(?<!\\)\\\s*(?:\$|\\\]|\\\)|$)", expr):
                    clean_expr = re.sub(r"(?<!\\)\\\s*(\$|\\\]|\\\)|$)", r"\1", expr)
                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=slide_id,
                            severity=Severity.P1,
                            issue="Ký tự backslash '\\' kết thúc lơ lửng trong công thức toán học",
                            rationale="Ký tự gạch chéo ngược không có tên lệnh đi kèm ở cuối công thức sẽ gây lỗi parser LaTeX/OMML.",
                            suggestion="Loại bỏ ký tự gạch chéo ngược thừa.",
                            evidence=expr,
                            original_value=expr,
                            suggested_value=clean_expr
                        )
                    )

        return findings

    def _fix_double_scripts(self, item: str) -> str:
        # e.g. x^2^3 -> x^{2^3}
        super_m = re.match(r"(\w+)\^([^{}\s\+\-\*\/\=\<\>\,\;]+)\^([^{}\s\+\-\*\/\=\<\>\,\;]+)", item)
        if super_m:
            return f"{super_m.group(1)}^{{{super_m.group(2)}^{{{super_m.group(3)}}}}}"
        sub_m = re.match(r"(\w+)\_([^{}\s\+\-\*\/\=\<\>\,\;]+)\_([^{}\s\+\-\*\/\=\<\>\,\;]+)", item)
        if sub_m:
            return f"{sub_m.group(1)}_{{{sub_m.group(2)}_{{{sub_m.group(3)}}}}}"
        return item

    def _attempt_fix_brackets(self, expr: str) -> str:
        """Attempts to balance open braces cleanly inside math delimiters."""
        open_curly = expr.count('{')
        close_curly = expr.count('}')
        fixed = expr
        if open_curly > close_curly:
            missing = '}' * (open_curly - close_curly)
            if fixed.endswith("$$"):
                fixed = fixed[:-2] + missing + "$$"
            elif fixed.endswith("$"):
                fixed = fixed[:-1] + missing + "$"
            elif fixed.endswith(r"\]"):
                fixed = fixed[:-2] + missing + r"\]"
            elif fixed.endswith(r"\)"):
                fixed = fixed[:-2] + missing + r"\)"
            else:
                fixed = fixed + missing
        return fixed

    def auto_remediate(self, target: Any, findings: List[AgentFinding], context: Optional[Dict[str, Any]] = None) -> Any:
        remediated = copy.deepcopy(target)
        slides = self._get_slides(remediated)

        # Map of (slide_id, original_value) -> suggested_value
        fix_map: List[Tuple[str, str, str]] = []
        for finding in findings:
            if finding.agent == self.name and finding.original_value and finding.suggested_value and finding.original_value != finding.suggested_value:
                fix_map.append((finding.slide_id, finding.original_value, finding.suggested_value))

        for slide_id, orig_val, sugg_val in fix_map:
            for s in slides:
                if s.get("slide_id") == slide_id:
                    def _replace_in_field(val: Any) -> Any:
                        if isinstance(val, str):
                            if orig_val in val:
                                return val.replace(orig_val, sugg_val)
                            # Handle unclosed delimiter by appending if needed
                            if orig_val.startswith("$$") and "$$" not in val[2:]:
                                return val + "$$"
                            if orig_val.startswith("$") and val.count("$") % 2 != 0:
                                return val + "$"
                        return val

                    for k in ["assertion_title", "title", "headline", "primary_claim", "speaker_notes"]:
                        if k in s:
                            s[k] = _replace_in_field(s[k])
                    for atom in (s.get("atoms") or []):
                        if isinstance(atom, dict):
                            for ak in ["title", "text", "body", "mechanism"]:
                                if ak in atom:
                                    atom[ak] = _replace_in_field(atom[ak])
                    items = (s.get("content_items") or []) + (s.get("cards") or []) + (s.get("boxes") or [])
                    for item in items:
                        if isinstance(item, dict):
                            for ik in ["title", "text", "body", "headline", "description"]:
                                if ik in item:
                                    item[ik] = _replace_in_field(item[ik])

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            return remediated
        return slides

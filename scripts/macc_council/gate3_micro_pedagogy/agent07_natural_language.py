"""
scripts/macc_council/gate3_micro_pedagogy/agent07_natural_language.py
Agent 7: NaturalLanguagePurist (AI Cliché Blacklist & Business Tone Purist).
Purges generic AI boilerplate, filler rhetoric, lazy ellipsis, and conversational sludge across Vietnamese & English.
Hardened with comprehensive multi-lingual cliché catalogs, math shielding, and schema-agnostic auto-remediation.
"""

from __future__ import annotations

import copy
import re
from typing import Any, Dict, List, Optional, Tuple
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, Severity


class NaturalLanguagePurist(BaseCouncilAgent):
    """
    Agent 07: Natural Language Purist.
    Identifies and eliminates generic AI clichés, wordy passive voice,
    trailing ellipsis (... / v.v...), and uninformative filler phrases in Vietnamese and English.
    """

    MATH_BLOCK_REGEX = re.compile(
        r"(\$\$[\s\S]+?\$\$|\$[^\$\n]+?\$|\\\[[\s\S]+?\\\]|\\\(.+?\\\))"
    )

    # Multi-lingual cliché definitions: (regex, description, default_replacement)
    AI_CLICHE_RULES = [
        # --- Vietnamese Clichés ---
        (
            re.compile(r"\b(trong\s+kỷ\s+nguyên\s+số(?:\s+ngày\s+nay)?)\b", re.IGNORECASE),
            "Sáo rỗng AI cliché tiếng Việt (kỷ nguyên số)",
            ""
        ),
        (
            re.compile(r"\b(thời\s+đại\s+4\.0|trong\s+thời\s+đại\s+4\.0)\b", re.IGNORECASE),
            "Sáo rỗng AI cliché tiếng Việt (thời đại 4.0)",
            ""
        ),
        (
            re.compile(r"\b(không\s+thể\s+phủ\s+nhận\s+rằng)\b", re.IGNORECASE),
            "Khẩu ngữ dài dòng thừa thãi tiếng Việt",
            ""
        ),
        (
            re.compile(r"\b(như\s+chúng\s+ta\s+đã\s+biết|ai\s+cũng\s+biết\s+rằng)\b", re.IGNORECASE),
            "Khẩu ngữ thuyết trình thừa thãi",
            ""
        ),
        (
            re.compile(r"\b(đóng\s+vai\s+trò\s+(?:vô\s+cùng|hết\s+sức|rất)\s+quan\s+trọng(?:\s+trong\s+việc)?)\b", re.IGNORECASE),
            "Sáo rỗng thụ động tiếng Việt",
            "trọng tâm trong "
        ),
        (
            re.compile(r"\b(hành\s+trình\s+vươn\s+mình|bứt\s+phá\s+mọi\s+giới\s+hạn)\b", re.IGNORECASE),
            "Văn phong hoa mỹ quá đà tiếng Việt",
            "chiến lược phát triển"
        ),
        (
            re.compile(r"\b(chìa\s+khóa\s+vạn\s+năng|viên\s+đạn\s+bạc)\b", re.IGNORECASE),
            "Biểu tượng sáo rỗng phi khoa học",
            "giải pháp then chốt"
        ),

        # --- English Clichés ---
        (
            re.compile(r"\b(in\s+today's\s+(?:rapidly\s+changing|fast-paced|dynamic|digital)\s+(?:world|era|landscape))\b", re.IGNORECASE),
            "English AI Boilerplate (in today's world/era)",
            ""
        ),
        (
            re.compile(r"\b((?:let's\s+)?delve(?:\s+deeply)?\s+into)\b", re.IGNORECASE),
            "English AI Cliché (delve into)",
            "examine"
        ),
        (
            re.compile(r"\b(game\s*changer|game-changing)\b", re.IGNORECASE),
            "English Overused Buzzword (game changer)",
            "breakthrough"
        ),
        (
            re.compile(r"\b(testament\s+to)\b", re.IGNORECASE),
            "English AI Cliché (testament to)",
            "evidence of"
        ),
        (
            re.compile(r"\b(paradigm\s+shift)\b", re.IGNORECASE),
            "English Buzzword (paradigm shift)",
            "fundamental change"
        ),
        (
            re.compile(r"\b(tapestry\s+of|beacon\s+of\s+hope)\b", re.IGNORECASE),
            "English Metaphorical AI Sludge",
            ""
        ),

        # --- Lazy Inconclusive Ellipsis ---
        (
            re.compile(r"(\bv\.v\.\.\.|\bvân\s+vân\.\.\.|(?<!\.)\.\.\.(?!\.))", re.IGNORECASE),
            "Dấu chấm lửng cẩu thả / thiếu dứt khoát",
            "."
        )
    ]

    def __init__(self):
        super().__init__(name="NaturalLanguagePurist", gate="Gate 3: Micro-Pedagogy & Scientific Precision")

    def _get_slides(self, target: Any) -> List[Dict[str, Any]]:
        if isinstance(target, list):
            return target
        if isinstance(target, dict):
            return target.get("slides", [target])
        return []

    def _shield_math(self, text: str) -> Tuple[str, List[Tuple[str, str]]]:
        shields: List[Tuple[str, str]] = []
        def _repl(m: re.Match) -> str:
            tok = f"__MATH_SHIELD_{len(shields)}__"
            shields.append((tok, m.group(0)))
            return tok
        shielded = self.MATH_BLOCK_REGEX.sub(_repl, text)
        return shielded, shields

    def audit(self, target: Any, context: Optional[Dict[str, Any]] = None) -> List[AgentFinding]:
        findings: List[AgentFinding] = []
        slides = self._get_slides(target)

        for s in slides:
            slide_id = s.get("slide_id", "unknown_slide")
            slide_text = self.extract_slide_text(s)

            # Shield math blocks so math ellipsis (\dots, ...) won't trigger lazy ellipsis rule
            shielded_text, _ = self._shield_math(slide_text)

            for pattern, label, replacement in self.AI_CLICHE_RULES:
                for match in pattern.finditer(shielded_text):
                    phrase = match.group(0)

                    # Guard against false positives:
                    # e.g., "Cách mạng công nghiệp lần thứ tư" or official resolution references
                    if "4.0" in phrase and "cách mạng công nghiệp" in slide_text.lower():
                        # If the phrase itself is part of official title, skip
                        start_pos = max(0, match.start() - 30)
                        pre_ctx = shielded_text[start_pos:match.start()].lower()
                        if "nghị quyết" in pre_ctx or "quyết định" in pre_ctx or "đề án" in pre_ctx:
                            continue

                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=slide_id,
                            severity=Severity.P1,
                            issue=f"Phát hiện văn phong sáo rỗng: '{phrase}' ({label})",
                            rationale="Slide chuyên nghiệp cần ngôn ngữ sắc bén, súc tích và hành động; tránh các cụm từ đệm AI tự động tạo ra.",
                            suggestion=f"Loại bỏ hoặc thay thế cụm từ '{phrase}' bằng động từ hành động hoặc dữ liệu trực tiếp.",
                            evidence=phrase,
                            original_value=phrase,
                            suggested_value=replacement
                        )
                    )

        return findings

    def auto_remediate(self, target: Any, findings: List[AgentFinding], context: Optional[Dict[str, Any]] = None) -> Any:
        remediated = copy.deepcopy(target)
        slides = self._get_slides(remediated)

        # Build replacement map: pattern -> replacement
        for s in slides:
            def _clean_str(text: str) -> str:
                if not isinstance(text, str):
                    return text
                clean = text
                # Shield math blocks
                shielded, shields = self._shield_math(clean)

                for pattern, _, rep in self.AI_CLICHE_RULES:
                    # Clean punctuation around removal
                    if rep == "":
                        # Also clean leading/trailing commas or spaces
                        pat_with_comma = re.compile(pattern.pattern + r"\s*,\s*", pattern.flags)
                        shielded = pat_with_comma.sub("", shielded)
                        shielded = pattern.sub("", shielded)
                    elif rep == ".":
                        shielded = re.sub(pattern.pattern + r"\s*", ". ", shielded)
                    else:
                        shielded = pattern.sub(rep, shielded)

                # Clean multiple spaces and double periods
                shielded = re.sub(r"\s+", " ", shielded)
                shielded = re.sub(r"\.\s*\.", ".", shielded)
                shielded = re.sub(r"^\s*,\s*", "", shielded).strip()

                # Capitalize first letter of sentences if needed
                if shielded and shielded[0].islower():
                    shielded = shielded[0].upper() + shielded[1:]

                # Restore math shields
                for tok, orig in shields:
                    shielded = shielded.replace(tok, orig)

                return shielded

            for k in ["assertion_title", "title", "headline", "primary_claim", "subtitle", "speaker_notes"]:
                if k in s:
                    s[k] = _clean_str(s[k])

            for atom in (s.get("atoms") or []):
                if isinstance(atom, dict):
                    for ak in ["title", "text", "body", "mechanism", "kicker"]:
                        if ak in atom:
                            atom[ak] = _clean_str(atom[ak])

            items = (s.get("content_items") or []) + (s.get("cards") or []) + (s.get("boxes") or [])
            for item in items:
                if isinstance(item, dict):
                    for ik in ["title", "text", "body", "headline", "description"]:
                        if ik in item:
                            item[ik] = _clean_str(item[ik])

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            return remediated
        return slides

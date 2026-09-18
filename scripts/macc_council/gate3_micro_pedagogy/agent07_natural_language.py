"""
scripts/macc_council/gate3_micro_pedagogy/agent07_natural_language.py
Agent 7: NaturalLanguagePurist (AI Cliché Blacklist & Business Tone Purist).
Purges generic AI boilerplate, filler rhetoric, lazy ellipsis, and conversational sludge.
"""

from __future__ import annotations

import copy
import re
from typing import Any, Dict, List, Optional
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, Severity


class NaturalLanguagePurist(BaseCouncilAgent):
    """
    Agent 07: Natural Language Purist.
    Identifies and eliminates generic AI clichés, wordy passive voice,
    trailing ellipsis (... / v.v...), and uninformative filler phrases.
    """

    AI_CLICHE_PATTERNS = [
        (re.compile(r"\b(trong\s+kỷ\s+nguyên\s+số(?:\s+ngày\s+nay)?)\b", re.IGNORECASE), "Sáo rỗng AI cliché (kỷ nguyên số)"),
        (re.compile(r"\b(trong\s+thời\s+đại\s+4\.0)\b", re.IGNORECASE), "Sáo rỗng AI cliché (thời đại 4.0)"),
        (re.compile(r"\b(không\s+thể\s+phủ\s+nhận\s+rằng)\b", re.IGNORECASE), "Khẩu ngữ dài dòng thừa thãi"),
        (re.compile(r"\b(như\s+chúng\s+ta\s+đã\s+biết)\b", re.IGNORECASE), "Khẩu ngữ thừa thãi"),
        (re.compile(r"\b(đóng\s+vai\s+trò\s+(?:vô\s+cùng|hết\s+sức|rất)\s+quan\s+trọng)\b", re.IGNORECASE), "Sáo rỗng thụ động"),
        (re.compile(r"\b(hành\s+trình\s+vươn\s+mình)\b", re.IGNORECASE), "Văn phong hoa mỹ quá đà"),
        (re.compile(r"\b(v\.v\.\.\.|vân\s+vân\.\.\.|\.\.\.)\b", re.IGNORECASE), "Dấu chấm lửng cẩu thả / thiếu dứt khoát")
    ]

    def __init__(self):
        super().__init__(name="NaturalLanguagePurist", gate="Gate 3: Micro-Pedagogy & Scientific Precision")

    def _get_slides(self, target: Any) -> List[Dict[str, Any]]:
        if isinstance(target, list):
            return target
        if isinstance(target, dict):
            return target.get("slides", [target])
        return []

    def audit(self, target: Any, context: Optional[Dict[str, Any]] = None) -> List[AgentFinding]:
        findings: List[AgentFinding] = []
        slides = self._get_slides(target)

        for s in slides:
            slide_id = s.get("slide_id", "unknown_slide")
            slide_text = self.extract_slide_text(s)

            for pattern, label in self.AI_CLICHE_PATTERNS:
                for match in pattern.finditer(slide_text):
                    phrase = match.group(0)
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
                            suggested_value=""
                        )
                    )

        return findings

    def auto_remediate(self, target: Any, findings: List[AgentFinding], context: Optional[Dict[str, Any]] = None) -> Any:
        remediated = copy.deepcopy(target)
        slides = self._get_slides(remediated)

        replacements = [
            (re.compile(r"\btrong\s+kỷ\s+nguyên\s+số(?:\s+ngày\s+nay)?\s*,?\s*", re.IGNORECASE), ""),
            (re.compile(r"\btrong\s+thời\s+đại\s+4\.0\s*,?\s*", re.IGNORECASE), ""),
            (re.compile(r"\bkhông\s+thể\s+phủ\s+nhận\s+rằng\s*,?\s*", re.IGNORECASE), ""),
            (re.compile(r"\bnhư\s+chúng\s+ta\s+đã\s+biết\s*,?\s*", re.IGNORECASE), ""),
            (re.compile(r"\bđóng\s+vai\s+trò\s+(?:vô\s+cùng|hết\s+sức|rất)\s+quan\s+trọng\s+trong\s+việc\s*", re.IGNORECASE), "trực tiếp "),
            (re.compile(r"\bđóng\s+vai\s+trò\s+(?:vô\s+cùng|hết\s+sức|rất)\s+quan\s+trọng\b", re.IGNORECASE), "trọng tâm"),
            (re.compile(r"\s*(?:v\.v\.\.\.|vân\s+vân\.\.\.|\.\.\.)", re.IGNORECASE), ".")
        ]

        for s in slides:
            for k in ["assertion_title", "primary_claim", "speaker_notes"]:
                if k in s and isinstance(s[k], str):
                    for pat, rep in replacements:
                        s[k] = pat.sub(rep, s[k]).strip()
            for atom in s.get("atoms", []):
                if isinstance(atom, dict):
                    for ak in ["title", "text", "mechanism", "kicker"]:
                        if ak in atom and isinstance(atom[ak], str):
                            for pat, rep in replacements:
                                atom[ak] = pat.sub(rep, atom[ak]).strip()

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            return remediated
        return slides

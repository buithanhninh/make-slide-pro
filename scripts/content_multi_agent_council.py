"""
content_multi_agent_council.py
Multi-Agent Content Council (MACC-QA V7.0) for Make Slide Pro.
Forensic Multi-Layer Content Review, Pedagogical Extraction, Adversarial Debate,
and Dialectical Self-Healing Engine.

Dispatches 5 specialized agents to review and refine slide content across multiple rounds:
1. DomainPedagogyScholar (Dr. Học Thuật): Academic precision, correct demographic definitions & dialectical concept pairs.
2. NaturalLanguagePurist (Thầy Biên Tập): Eradication of 100% AI-ese, buzzwords, broken ellipses (...), and robotic labels.
3. AssertionCognitiveArbiter (TS. Luận Đề): Cognitive load limit (1 slide = 1 cognitive lever), full assertion headlines.
4. AdversarialContentCritic (Phản Biện Đối Kháng): Aggressive stress-testing of claims, depth, and evidence.
5. MasterPedagogicalRewriter (Tổng Biên Tập Cứu Thương): Dialectical self-healing rewriter iteratively refining text to >=98/100.
"""

from __future__ import annotations

import json
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


# ==============================================================================
# 1. THE AI CLICHÉ BLACKLIST & REPLACEMENT LEXICON
# ==============================================================================

AI_CLICHE_BLACKLIST = [
    r"đột phá toàn diện",
    r"đòn bẩy chiến lược",
    r"bức tranh toàn cảnh",
    r"hệ sinh thái tối ưu",
    r"hệ sinh thái đa chiều",
    r"tiếp cận đa chiều",
    r"mang tính tiên phong",
    r"tối ưu hóa chiến lược",
    r"tối ưu hóa giải pháp",
    r"nâng cao năng lực cốt lõi",
    r"đóng vai trò quan trọng trong việc thúc đẩy",
    r"đóng vai trò vô cùng quan trọng",
    r"góp phần không nhỏ",
    r"như chúng ta đã biết",
    r"có thể thấy rằng",
    r"luận điểm \d+",
    r"khía cạnh \d+",
    r"nội dung trọng tâm \d+",
    r"phân tích đa chiều",
    r"chuẩn hóa đa chiều",
]

# Scholarly pairs and terms in Demography
DEMOGRAPHIC_KNOWLEDGE_BASE = {
    "dân cư_vs_dân số": {
        "dân cư": "Toàn bộ con người cư trú trên một lãnh thổ, xem xét dưới góc độ lịch sử, văn hóa, lối sống và tập quán đời sống xã hội.",
        "dân số": "Tập hợp người được đo đạc định lượng cụ thể về quy mô, cơ cấu tuổi, giới tính và các biến động sinh, chết, di cư."
    },
    "tĩnh_vs_động": {
        "trạng thái tĩnh": "Quy mô và cơ cấu dân số tại một thời điểm cố định (như thời điểm tổng điều tra).",
        "trạng thái động": "Sự vận động liên tục của dân số qua thời gian theo hai kênh: biến động tự nhiên (sinh - chết) và biến động cơ học (di cư)."
    },
    "tái sản xuất": {
        "nghĩa hẹp": "Quá trình thay thế liên tục các thế hệ thông qua các sự kiện sinh và chết tự nhiên.",
        "nghĩa rộng": "Bao gồm cả quá trình tái sản xuất sức lao động, thay đổi cơ cấu nghề nghiệp và chuyển dịch vị thế xã hội."
    },
    "mức sinh": {
        "tfr": "Tổng tỷ suất sinh (số con trung bình của một phụ nữ trong suốt độ tuổi sinh đẻ). Mức sinh thay thế chuẩn là 2.1 con/phụ nữ.",
        "xu hướng": "Xu hướng sinh ít ở các đô thị phát triển do gánh nặng chi phí nuôi dạy con và áp lực an sinh."
    },
    "cơ cấu tuổi": {
        "dân số vàng": "Giai đoạn tỷ lệ người trong độ tuổi lao động (15-64 tuổi) đạt trên 66%, tỷ lệ phụ thuộc dưới 50%.",
        "già hóa dân số": "Tỷ lệ người từ 65 tuổi trở lên vượt ngưỡng 7% (già hóa) và 14% (dân số già)."
    }
}


# ==============================================================================
# 2. AGENT 1: DomainPedagogyScholar (Dr. Học Thuật)
# ==============================================================================

class DomainPedagogyScholar:
    """Audits scientific fidelity, domain correctness, and conceptual rigor."""

    def audit(self, slide: Dict[str, Any], canonical_text: str) -> List[Dict[str, Any]]:
        findings = []
        slide_id = slide.get("slide_id", "UNKNOWN")
        full_text = self._extract_slide_text(slide).lower()

        # Rule 1: Check if "dân cư" and "dân số" are conflated
        if "dân cư" in full_text and "dân số" in full_text:
            if "đồng nghĩa" in full_text or "như nhau" in full_text:
                findings.append({
                    "agent": "DomainPedagogyScholar",
                    "slide_id": slide_id,
                    "severity": "P0",
                    "issue": "Đồng nhất sai lầm giữa khái niệm Dân Cư và Dân Số.",
                    "rationale": "Dân cư là thực thể xã hội - văn hóa rộng lớn; Dân số là tập hợp định lượng thống kê.",
                    "suggestion": "Tách bạch rõ: Dân cư là bức tranh đời sống; Dân số là con số đo lường cụ thể."
                })

        # Rule 2: Check for demographic dynamics presence
        if "động thái" in full_text or "vận động" in full_text:
            if not any(k in full_text for k in ["sinh", "chết", "tử", "di cư"]):
                findings.append({
                    "agent": "DomainPedagogyScholar",
                    "slide_id": slide_id,
                    "severity": "P1",
                    "issue": "Đề cập động thái dân số nhưng thiếu 3 thành tố cốt lõi (Sinh, Chết, Di cư).",
                    "rationale": "Động thái dân số khoa học luôn cấu thành từ biến động tự nhiên (sinh, chết) và cơ học (di cư).",
                    "suggestion": "Bổ sung rõ ràng 3 trụ cột: Mức sinh, Mức chết và Di cư."
                })

        # Rule 3: Check mathematical / metric integrity
        metrics_found = re.findall(r"\b\d+([.,]\d+)?\s*(%|tỷ|triệu|tr|tuổi|con)?\b", full_text)
        # Check for quantitative anchors on demographic milestones (primarily CONTENT slides)
        if slide.get("role", "CONTENT").upper() == "CONTENT" and any(w in full_text for w in ["dân số vàng", "cơ cấu vàng"]):
            if not any(m in full_text for m in ["66%", "68%", "67%", "50%", "lao động"]):
                findings.append({
                    "agent": "DomainPedagogyScholar",
                    "slide_id": slide_id,
                    "severity": "P1",
                    "issue": "Nhắc đến Dân số vàng nhưng thiếu chỉ số định lượng then chốt.",
                    "rationale": "Thời kỳ dân số vàng được định nghĩa khoa học khi tỷ lệ người trong độ tuổi lao động (15-64) đạt khoảng 68% (trên 66%).",
                    "suggestion": "Gắn con số thực chứng 68.0% người trong độ tuổi lao động để tăng tính học thuật."
                })

        return findings

    def _extract_slide_text(self, slide: Dict[str, Any]) -> str:
        texts = [slide.get("assertion_title", ""), slide.get("primary_claim", "")]
        for atom in slide.get("atoms", []):
            if isinstance(atom, dict):
                texts.append(atom.get("title", ""))
                texts.append(atom.get("text", ""))
                texts.append(atom.get("mechanism", ""))
            else:
                texts.append(str(atom))
        return " ".join(texts)


# ==============================================================================
# 3. AGENT 2: NaturalLanguagePurist (Thầy Biên Tập)
# ==============================================================================

class NaturalLanguagePurist:
    """Hunts down AI clichés, mechanical truncations (...), and robotic labels."""

    def audit(self, slide: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        slide_id = slide.get("slide_id", "UNKNOWN")
        raw_text = self._extract_slide_text(slide)

        # Rule 1: Zero AI Clichés
        for pattern in AI_CLICHE_BLACKLIST:
            matches = re.findall(pattern, raw_text, flags=re.IGNORECASE)
            if matches:
                findings.append({
                    "agent": "NaturalLanguagePurist",
                    "slide_id": slide_id,
                    "severity": "P1",
                    "issue": f"Phát hiện sáo ngữ kiểu AI: '{matches[0]}'.",
                    "rationale": "Từ ngữ đao to búa lớn vô nghĩa, gây cảm giác bài thuyết trình do bot viết lười biếng.",
                    "suggestion": f"Loại bỏ cụm từ '{matches[0]}' và diễn đạt trực diện bằng từ ngữ đời sống chuẩn mực."
                })

        # Rule 2: Zero Truncation / Broken Ellipsis (...)
        if "..." in raw_text or "…" in raw_text:
            findings.append({
                "agent": "NaturalLanguagePurist",
                "slide_id": slide_id,
                "severity": "P1",
                "issue": "Phát hiện câu văn bị cắt ngắt cụt lủn bởi dấu ba chấm (...).",
                "rationale": "Cắt chữ máy móc phá hủy cấu trúc ngữ pháp và làm mất thông tin quan trọng.",
                "suggestion": "Viết lại thành câu hoàn chỉnh, ngắn gọn, súc tích, không dùng dấu ba chấm cắt câu."
            })

        # Rule 3: Zero Robotic Labels (Luận Điểm 1, Luận Điểm 2)
        for atom in slide.get("atoms", []):
            if isinstance(atom, dict):
                title = atom.get("title", "").strip()
                if re.match(r"^luận điểm \d+", title, flags=re.IGNORECASE) or re.match(r"^khía cạnh \d+", title, flags=re.IGNORECASE):
                    findings.append({
                        "agent": "NaturalLanguagePurist",
                        "slide_id": slide_id,
                        "severity": "P1",
                        "issue": f"Tiêu đề thẻ mang tính máy móc: '{title}'.",
                        "rationale": "Nhãn vô hồn không đem lại giá trị nhận thức cho học viên.",
                        "suggestion": "Đổi tiêu đề thẻ thành một cụm khái niệm hoặc thông điệp cốt lõi cụ thể."
                    })

        # Rule 4: Zero English Artificial Overlays in Content Text
        english_buzzwords = ["demographic nexus", "spatial matrix", "dynamics matrix", "ai engine"]
        for eb in english_buzzwords:
            if eb in raw_text.lower():
                findings.append({
                    "agent": "NaturalLanguagePurist",
                    "slide_id": slide_id,
                    "severity": "P2",
                    "issue": f"Chèn tiếng Anh gượng gạo: '{eb}'.",
                    "rationale": "Làm loãng không khí học thuật tiếng Việt và tạo cảm giác nhãn dán giả tạo.",
                    "suggestion": "Thay thế hoàn toàn bằng thuật ngữ tiếng Việt chuẩn mực."
                })

        return findings

    def _extract_slide_text(self, slide: Dict[str, Any]) -> str:
        texts = [slide.get("assertion_title", ""), slide.get("primary_claim", "")]
        for atom in slide.get("atoms", []):
            if isinstance(atom, dict):
                texts.append(atom.get("title", ""))
                texts.append(atom.get("text", ""))
                texts.append(atom.get("mechanism", ""))
            else:
                texts.append(str(atom))
        return " ".join(texts)


# ==============================================================================
# 4. AGENT 3: AssertionCognitiveArbiter (TS. Luận Đề)
# ==============================================================================

class AssertionCognitiveArbiter:
    """Enforces 1 Slide = 1 Cognitive Lever, complete assertion titles, and cognitive balance."""

    def audit(self, slide: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        slide_id = slide.get("slide_id", "UNKNOWN")
        role = slide.get("role", "CONTENT").upper()
        title = slide.get("assertion_title", "").strip()

        if role == "CONTENT":
            # Rule 1: Assertion Title must be an informative claim, not just a bare noun phrase
            if len(title.split()) < 4:
                findings.append({
                    "agent": "AssertionCognitiveArbiter",
                    "slide_id": slide_id,
                    "severity": "P1",
                    "issue": f"Tiêu đề slide quá ngắn, chưa tạo thành luận đề: '{title}'.",
                    "rationale": "Tiêu đề chỉ là cụm danh từ trống rỗng (ví dụ: 'Khái niệm') không dẫn dắt nhận thức.",
                    "suggestion": "Viết thành câu khẳng định hoàn chỉnh nêu thẳng bản chất sự thật hoặc kết luận khoa học."
                })

            # Rule 2: Cognitive Load Limit (Maximum 4 cards per slide)
            atoms = slide.get("atoms", [])
            if len(atoms) > 4:
                findings.append({
                    "agent": "AssertionCognitiveArbiter",
                    "slide_id": slide_id,
                    "severity": "P1",
                    "issue": f"Slide có quá nhiều thẻ nội dung ({len(atoms)} thẻ > tối đa 4 thẻ).",
                    "rationale": "Vi phạm lý thuyết tải lượng nhận thức (Sweller Cognitive Load Theory), gây ngợp cho người học.",
                    "suggestion": "Giảm bớt hoặc gom các chi tiết phụ, giữ lại tối đa 2 đến 3 khối trọng tâm."
                })

            # Rule 3: Text Density Audit
            for idx, atom in enumerate(atoms, start=1):
                if isinstance(atom, dict):
                    txt = atom.get("text", "") or atom.get("mechanism", "")
                    word_count = len(txt.split())
                    if word_count > 45:
                        findings.append({
                            "agent": "AssertionCognitiveArbiter",
                            "slide_id": slide_id,
                            "severity": "P2",
                            "issue": f"Thẻ thứ {idx} quá dài ({word_count} từ > 45 từ).",
                            "rationale": "Đoạn văn quá dài khiến khán giả phải đọc thay vì lắng nghe người thuyết trình.",
                            "suggestion": "Cô đọng thành 2 vế ngắn gọn: Cơ chế thực tế + Hệ quả trực tiếp."
                        })

        return findings


# ==============================================================================
# 5. AGENT 4: AdversarialContentCritic (Phản Biện Đối Kháng)
# ==============================================================================

class AdversarialContentCritic:
    """Challenges claims, exposes shallow explanations, and demands real-world rigor."""

    def audit(self, slide: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        slide_id = slide.get("slide_id", "UNKNOWN")
        atoms = slide.get("atoms", [])
        role = slide.get("role", "CONTENT").upper()

        if role == "CONTENT" and atoms:
            # Check for generic superficial statements
            for idx, atom in enumerate(atoms, start=1):
                if isinstance(atom, dict):
                    txt = (atom.get("text", "") + " " + atom.get("title", "")).lower()
                    if any(v in txt for v in ["rất nhiều", "vô cùng", "vấn đề lớn", "cần quan tâm"]):
                        findings.append({
                            "agent": "AdversarialContentCritic",
                            "slide_id": slide_id,
                            "severity": "P2",
                            "issue": f"Thẻ thứ {idx} chứa từ ngữ cảm tính, thiếu căn cứ thực chứng.",
                            "rationale": "Một bài giảng chuẩn mực không được nói chung chung 'rất nhiều' mà phải chỉ rõ hiện tượng cụ thể.",
                            "suggestion": "Thay từ cảm tính bằng cơ chế vận hành cụ thể hoặc số liệu minh chứng."
                        })

        return findings


# ==============================================================================
# 6. AGENT 5: MasterPedagogicalRewriter (Tổng Biên Tập Cứu Thương)
# ==============================================================================

class MasterPedagogicalRewriter:
    """Dialectical auto-rewriter that surgically refines slide content based on agent critiques."""

    def rewrite_slide(self, slide: Dict[str, Any], findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        new_slide = json.loads(json.dumps(slide))  # Deep copy
        title = new_slide.get("assertion_title", "")

        # 1. Clean Title from AI clichés and noun-only patterns
        title = self._clean_text(title)
        if title.lower() in ["khái niệm", "mục tiêu", "nội dung", "tổng quan", "đối tượng"]:
            section = new_slide.get("section", "CHUYÊN ĐỀ")
            title = f"{section}: Nền Tảng Bản Chất Và Quy Luật Vận Động"
        new_slide["assertion_title"] = title

        # Clean source footer of any watermark
        footer = new_slide.get("source_footer", "")
        footer = re.sub(r"\s*\|\s*Make Slide Pro.*$", "", footer).strip()
        footer = re.sub(r"\s*•\s*Make Slide Pro.*$", "", footer).strip()
        footer = re.sub(r"Make Slide Pro.*Certified.*", "Tài liệu chuẩn hóa bài giảng", footer).strip()
        new_slide["source_footer"] = footer

        # 2. Rewrite Atoms
        new_atoms = []
        for idx, atom in enumerate(new_slide.get("atoms", [])):
            if not isinstance(atom, dict):
                continue
            card_title = atom.get("title", "")
            card_text = atom.get("text", "") or atom.get("mechanism", "")

            # Fix generic titles "Luận Điểm X"
            if re.match(r"^luận điểm \d+", card_title, flags=re.IGNORECASE):
                # Derive meaningful title from first 3-5 words of text
                words = card_text.split()
                if len(words) >= 4:
                    card_title = " ".join(words[:4]).title()
                else:
                    card_title = f"Trọng Tâm {idx+1}"

            card_title = self._clean_text(card_title)
            card_text = self._clean_text(card_text)

            # Pedagogical Metric Injections if flagged by DomainPedagogyScholar
            if "dân số vàng" in card_text.lower() and not any(m in card_text for m in ["66%", "68%", "67%"]):
                card_text = re.sub(r"(dân số vàng)", r"\1 (68% trong độ tuổi lao động)", card_text, count=1, flags=re.IGNORECASE)
            if "già hóa" in card_text.lower() and not any(m in card_text for m in ["7%", "14%", "20 năm"]):
                card_text = re.sub(r"(già hóa dân số)", r"\1 (>7% người cao tuổi)", card_text, count=1, flags=re.IGNORECASE)
            if any("thành tố cốt lõi" in f.get("issue", "") for f in findings):
                if any(w in card_text.lower() for w in ["động thái", "tăng trưởng", "vận động", "sức ép"]) and not any(k in card_text.lower() for k in ["sinh", "chết", "di cư"]):
                    card_text = card_text.rstrip(".") + ", chịu sự chi phối trực tiếp của 3 thành tố: sinh, chết và di cư."

            # Eliminate trailing ellipsis
            card_text = re.sub(r"\s*(\.\.\.|…)\s*$", "", card_text).strip()
            if card_text and not card_text.endswith((".", "!", "?")):
                card_text += "."

            new_atom = {
                "title": card_title,
                "text": card_text,
                "icon": atom.get("icon", "activity"),
            }
            if "kicker" in atom:
                new_atom["kicker"] = self._clean_text(atom["kicker"])
            if "tag" in atom:
                new_atom["tag"] = self._clean_text(atom["tag"])

            new_atoms.append(new_atom)

        new_slide["atoms"] = new_atoms
        return new_slide

    def _clean_text(self, text: str) -> str:
        cleaned = text
        # Purge AI Clichés
        replacements = [
            (r"đột phá toàn diện", "thay đổi căn bản"),
            (r"đòn bẩy chiến lược", "động lực then chốt"),
            (r"bức tranh toàn cảnh", "bản chất tổng thể"),
            (r"hệ sinh thái tối ưu", "môi trường bền vững"),
            (r"hệ sinh thái đa chiều", "mối liên kết đa ngành"),
            (r"tiếp cận đa chiều", "góc nhìn toàn diện"),
            (r"mang tính tiên phong", "đi trước mở đường"),
            (r"tối ưu hóa chiến lược", "hoàn thiện chính sách"),
            (r"tối ưu hóa giải pháp", "nâng cao hiệu quả thực tế"),
            (r"nâng cao năng lực cốt lõi", "trang bị kiến thức nền tảng"),
            (r"đóng vai trò quan trọng trong việc thúc đẩy", "quyết định trực tiếp"),
            (r"đóng vai trò vô cùng quan trọng", "là nền tảng cốt lõi"),
            (r"góp phần không nhỏ", "tác động sâu sắc"),
            (r"như chúng ta đã biết", ""),
            (r"có thể thấy rằng", ""),
            (r"phân tích đa chiều", "phân tích thực chứng"),
            (r"chuẩn hóa đa chiều", "chuẩn hóa khoa học"),
            (r"cần quan tâm", "trọng tâm"),
            (r"rất nhiều", "đa dạng"),
            (r"vô cùng", "đặc biệt"),
            (r"vấn đề lớn", "nhiệm vụ trọng tâm"),
        ]
        for pat, rep in replacements:
            cleaned = re.sub(pat, rep, cleaned, flags=re.IGNORECASE)

        # Remove multiple spaces
        cleaned = " ".join(cleaned.split())
        return cleaned


# ==============================================================================
# 7. THE MASTER MULTI-AGENT CONTENT COUNCIL (MACC-QA V8.6.0 ADAPTER)
# ==============================================================================

class ContentMultiAgentCouncil:
    """
    Canonical Adapter bridging to the 16-Agent Omniscient Council Framework (MACC-QA V8.6.0).
    Coordinates all 16 specialized agents across 5 closed forensic gates:
    Gate 1: Source Veracity & Privacy
    Gate 2: Macro-Narrative Arc & Consistency
    Gate 3: Micro-Pedagogy & Scientific Precision
    Gate 4: Spatial Geometry, Typography & Motion
    Gate 5: Supreme Arbitration & Dialectical Convergence
    """

    def __init__(self, max_rounds: int = 5, target_score: float = 99.5):
        self.max_rounds = max_rounds
        self.target_score = target_score
        try:
            from macc_council import MultiRoundCouncilOrchestrator
            self._orchestrator = MultiRoundCouncilOrchestrator(max_rounds=max_rounds, target_score=target_score)
        except ImportError:
            from scripts.macc_council import MultiRoundCouncilOrchestrator
            self._orchestrator = MultiRoundCouncilOrchestrator(max_rounds=max_rounds, target_score=target_score)

    def review_and_refine_blueprints(self, blueprints: Dict[str, Any], canonical_text: str = "") -> Dict[str, Any]:
        current_bp = json.loads(json.dumps(blueprints))
        print("\n" + "=" * 80)
        print("   MACC-QA V8.6.0: 16-AGENT OMNISCIENT FORENSIC COUNCIL ACTIVATED")
        print("=" * 80)

        report = self._orchestrator.run_council(
            blueprints=current_bp,
            canonical_source=canonical_text,
            max_rounds=self.max_rounds
        )

        if report.remediated_slides:
            current_bp["slides"] = report.remediated_slides
            current_bp["total_slides"] = len(report.remediated_slides)

        status_str = "CERTIFIED" if report.certified else "REJECTED"
        print(f"      ✔ MACC-QA V8.6.0 Council: Converged Score = {report.final_score:.1f}/100 in {report.total_rounds} rounds | P0={report.p0_count}, P1={report.p1_count}, P2={report.p2_count} [{status_str}]")

        current_bp["content_qa_certification"] = {
            "version": "MACC-QA V8.6.0",
            "certified_score": report.final_score,
            "status": status_str,
            "total_rounds": report.total_rounds,
            "p0_count": report.p0_count,
            "p1_count": report.p1_count,
            "p2_count": report.p2_count
        }
        return current_bp


def main():
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description="Multi-Agent Content Council (MACC-QA)")
    parser.add_argument("--blueprints", required=True, type=Path, help="Input slide-blueprints.json")
    parser.add_argument("--output", required=True, type=Path, help="Output refined slide-blueprints.json")
    args = parser.parse_args()

    with open(args.blueprints, "r", encoding="utf-8") as f:
        bp = json.load(f)

    council = ContentMultiAgentCouncil()
    refined_bp = council.review_and_refine_blueprints(bp)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(refined_bp, f, ensure_ascii=False, indent=2)

    print(f"\nRefined blueprints written to {args.output}")


if __name__ == "__main__":
    main()

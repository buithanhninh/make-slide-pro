"""
tests/macc_council/test_gate3.py
Adversarial Unit Tests for Gate 3: Micro-Pedagogy & Scientific Precision
Tests Agents 5 through 10.
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from scripts.macc_council.gate3_micro_pedagogy import (
    DomainPedagogyScholar,
    MathematicalOMMLValidator,
    NaturalLanguagePurist,
    AssertionCognitiveArbiter,
    AdversarialContentCritic,
    MasterPedagogicalRewriter
)
from scripts.macc_council.models import Severity


def test_agent05_domain_pedagogy():
    agent = DomainPedagogyScholar()
    deck = {
        "slides": [
            {
                "slide_id": "s1",
                "assertion_title": "Tăng trưởng kinh tế và thu nhập người dân",
                "primary_claim": "GDP bình quân đầu người: 120 tỷ USD là con số vượt bậc."
            },
            {
                "slide_id": "s2",
                "assertion_title": "Biến động nhân khẩu học",
                "primary_claim": "Tỷ suất sinh thay thế: 15% cần được duy trì ổn định."
            }
        ]
    }
    findings = agent.audit(deck)
    assert len(findings) == 2, f"Expected 2 domain mismatch findings, got {len(findings)}"
    assert any("GDP bình quân đầu người" in f.issue for f in findings)
    assert any("Tỷ suất sinh thay thế" in f.issue for f in findings)
    print("✔ test_agent05_domain_pedagogy passed")


def test_agent06_mathematical_omml():
    agent = MathematicalOMMLValidator()
    deck = {
        "slides": [
            {
                "slide_id": "s1",
                "assertion_title": "Mô hình tính toán hiệu suất",
                "primary_claim": r"Công thức tối ưu: $\frac{A + B}{C$ mang lại kết quả cao."  # Missing closing }
            },
            {
                "slide_id": "s2",
                "assertion_title": "Công thức chuẩn hóa",
                "primary_claim": r"Hàm mục tiêu: $\sum_{i=1}^n x_i^2 = 1$ đạt giá trị hội tụ."  # Valid formula
            }
        ]
    }
    findings = agent.audit(deck)
    p0_issues = [f for f in findings if f.severity == Severity.P0]
    assert len(p0_issues) >= 1, "Must flag unbalanced math brackets as P0"
    assert "chưa đóng ngoặc" in p0_issues[0].issue or "không khớp" in p0_issues[0].issue

    # Test auto-remediation
    remediated = agent.auto_remediate(deck, findings)
    remediated_findings = agent.audit(remediated)
    assert len(remediated_findings) == 0, "Remediated formula must be valid and pass audit"
    print("✔ test_agent06_mathematical_omml passed")


def test_agent07_natural_language_cliches():
    agent = NaturalLanguagePurist()
    deck = {
        "slides": [
            {
                "slide_id": "s1",
                "assertion_title": "Trong kỷ nguyên số ngày nay chuyển đổi số là tất yếu",
                "primary_claim": "Không thể phủ nhận rằng công nghệ đóng vai trò vô cùng quan trọng trong việc thúc đẩy tăng trưởng...",
                "atoms": [
                    {"title": "Dữ liệu lớn", "text": "Hành trình vươn mình của doanh nghiệp trong thời đại 4.0 v.v..."}
                ]
            }
        ]
    }
    findings = agent.audit(deck)
    assert len(findings) >= 4, f"Expected >= 4 cliché findings, got {len(findings)}"
    print(f"✔ test_agent07_natural_language_cliches detected {len(findings)} clichés")

    # Auto-remediation
    remediated = agent.auto_remediate(deck, findings)
    rem_text = agent.extract_slide_text(remediated["slides"][0]).lower()
    assert "trong kỷ nguyên số ngày nay" not in rem_text
    assert "trong thời đại 4.0" not in rem_text
    assert "v.v..." not in rem_text
    print("✔ test_agent07_natural_language_cliches auto-remediation passed")


def test_agent08_assertion_and_cognitive_load():
    agent = AssertionCognitiveArbiter()
    deck = {
        "slides": [
            {
                "slide_id": "s1",
                "assertion_title": "Tổng quan",  # Lazy topic label
                "archetype": "3_cards",
                "atoms": [
                    {"title": "Card 1", "text": "Text 1"},
                    {"title": "Card 2", "text": "Text 2"},
                    {"title": "Card 3", "text": "Text 3"},
                    {"title": "Card 4", "text": "Text 4"},
                    {"title": "Card 5", "text": "Text 5"},
                    {"title": "Card 6", "text": "Text 6"}  # Overload (6 > 4)
                ]
            }
        ]
    }
    findings = agent.audit(deck)
    assert any("Lazy Topic Label" in f.issue for f in findings), "Must flag lazy topic label"
    assert any("Cognitive Overload" in f.issue for f in findings), "Must flag atom overload"

    # Auto-remediation: Trims atoms to 4 and saves overflow to speaker_notes
    remediated = agent.auto_remediate(deck, findings)
    assert len(remediated["slides"][0]["atoms"]) == 4, "Must cap atoms at 4"
    assert "Card 5" in remediated["slides"][0]["speaker_notes"]
    print("✔ test_agent08_assertion_and_cognitive_load passed")


def test_agent09_adversarial_critic():
    agent = AdversarialContentCritic()
    deck = {
        "slides": [
            {
                "slide_id": "s1",
                "assertion_title": "Giải pháp AI bảo mật tuyệt đối",
                "primary_claim": "Phần mềm tốt nhất thị trường với 100% khách hàng hài lòng."
            }
        ]
    }
    findings = agent.audit(deck)
    assert len(findings) >= 3, f"Expected >= 3 red-team findings, got {len(findings)}"

    # Auto-remediation: Tempered language
    remediated = agent.auto_remediate(deck, findings)
    rem_text = agent.extract_slide_text(remediated["slides"][0])
    assert "bảo mật tuyệt đối" not in rem_text.lower()
    assert "tốt nhất thị trường" not in rem_text.lower()
    assert "100% khách hàng hài lòng" not in rem_text.lower()
    print("✔ test_agent09_adversarial_critic passed")


def test_agent10_master_rewriter():
    agent = MasterPedagogicalRewriter()
    deck = {
        "slides": [
            {
                "slide_id": "s1",
                "section": "Chính sách",
                "assertion_title": "Giải pháp",  # Short/empty topic label
                "primary_claim": "",
                "atoms": [
                    {"title": "Đầu tư hạ tầng số", "text": "Nâng cấp mạng lưới viễn thông băng thông rộng."}
                ]
            }
        ]
    }
    findings = agent.audit(deck)
    assert any("primary_claim" in f.issue for f in findings)

    remediated = agent.auto_remediate(deck, findings)
    s1 = remediated["slides"][0]
    assert len(s1["assertion_title"].split()) >= 4, "Must synthesize sentence headline"
    assert len(s1["primary_claim"]) > 0, "Must synthesize primary claim"
    print("✔ test_agent10_master_rewriter passed")


if __name__ == "__main__":
    print("Running Gate 3 Unit Tests...")
    test_agent05_domain_pedagogy()
    test_agent06_mathematical_omml()
    test_agent07_natural_language_cliches()
    test_agent08_assertion_and_cognitive_load()
    test_agent09_adversarial_critic()
    test_agent10_master_rewriter()
    print("🎉 Gate 3 Unit Tests Passed 100%!")

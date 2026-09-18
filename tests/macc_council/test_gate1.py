import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pytest
from scripts.macc_council.gate1_source_privacy import (
    SourceFidelityFactChecker,
    CompliancePrivacyGuardian
)
from scripts.macc_council.models import Severity


def test_source_fidelity_perfect_match():
    agent = SourceFidelityFactChecker()
    canonical_text = "Năm 2030, tỷ trọng năng lượng tái tạo đạt 31.5% với 185.000 lao động."
    slide = {
        "slide_id": "SLIDE_01",
        "assertion_title": "Tỷ trọng năng lượng tái tạo đạt 31.5% vào năm 2030",
        "primary_claim": "Tạo ra việc làm cho 185.000 lao động chất lượng cao.",
        "atoms": []
    }
    findings = agent.audit(slide, context={"canonical_text": canonical_text})
    assert len(findings) == 0, f"Expected 0 findings, got: {findings}"


def test_source_fidelity_hallucinated_percentage():
    agent = SourceFidelityFactChecker()
    canonical_text = "Năm 2030, tỷ trọng năng lượng tái tạo đạt 31.5%."
    slide = {
        "slide_id": "SLIDE_02",
        "assertion_title": "Tỷ trọng năng lượng tái tạo dự kiến đạt 85.5% vào năm 2030",
        "primary_claim": "Tăng trưởng vượt bậc.",
        "atoms": []
    }
    findings = agent.audit(slide, context={"canonical_text": canonical_text})
    assert any(f.severity == Severity.P0 and "85.5%" in f.issue for f in findings), "Failed to catch hallucinated 85.5%"


def test_compliance_privacy_detects_pii():
    agent = CompliancePrivacyGuardian()
    slide = {
        "slide_id": "SLIDE_03",
        "assertion_title": "Thông Tin Liên Hệ Báo Cáo Viên",
        "primary_claim": "Mọi thắc mắc liên hệ số CCCD: 001099012345 hoặc số điện thoại 0912345678, email nguyen.van.a@gmail.com.",
        "atoms": []
    }
    findings = agent.audit(slide)
    assert any(f.severity == Severity.P0 and "CCCD" in f.issue for f in findings), "Failed to detect CCCD"
    assert any(f.severity == Severity.P1 and "0912345678" in f.issue for f in findings), "Failed to detect phone number"
    assert any(f.severity == Severity.P1 and "nguyen.van.a@gmail.com" in f.issue for f in findings), "Failed to detect personal email"

    # Test auto-remediation (masking)
    remediated = agent.auto_remediate(slide, findings)
    rem_text = str(remediated)
    assert "0912***678" in rem_text, "Phone number was not masked"
    assert "contact@doanhnghiep.vn" in rem_text, "Email was not replaced"


def test_compliance_privacy_detects_api_key():
    agent = CompliancePrivacyGuardian()
    slide = {
        "slide_id": "SLIDE_04",
        "assertion_title": "Cấu Hình Hệ Thống AI",
        "primary_claim": "Hệ thống kết nối qua sk-abcdef1234567890abcdef123456.",
        "atoms": []
    }
    findings = agent.audit(slide)
    assert any(f.severity == Severity.P0 and "API Key" in f.issue for f in findings), "Failed to detect OpenAI secret key"


if __name__ == "__main__":
    test_source_fidelity_perfect_match()
    test_source_fidelity_hallucinated_percentage()
    test_compliance_privacy_detects_pii()
    test_compliance_privacy_detects_api_key()
    print("✔ Gate 1 Unit Tests Passed 100%!")

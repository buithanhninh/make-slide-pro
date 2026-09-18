"""
tests/macc_council/adversarial/test_agent02_hard.py
Adversarial Stress Test Matrix for Agent 02: CompliancePrivacyGuardian.
10 ruthless edge cases:
1. Formatted/Dotted/Spaced VN Phone numbers (0912.345.678, (+84) 903 111 222)
2. Formatted/Spaced CCCD (001 095 012 345, 079-090-123456)
3. Public corporate email (info@company.vn - NO FALSE POSITIVE)
4. Personal email leak (nguyen.van.a@gmail.com)
5. AWS Key & API Secret (AKIA..., sk-...)
6. JWT Bearer Token
7. Credit Card (16 digits formatted)
8. Strictly Confidential / Internal Only Marker
9. Large Financial Numbers (100.000.000 VNĐ - NO FALSE POSITIVE as CMND)
10. Full Auto-Remediation Masking Integrity
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

from scripts.macc_council.gate1_source_privacy import CompliancePrivacyGuardian
from scripts.macc_council.models import Severity


def run_all_adversarial_tests():
    agent = CompliancePrivacyGuardian()
    results = {}

    # Case 1: Formatted / Dotted VN Phone
    s1 = {"slide_id": "c1", "assertion_title": "Liên hệ hỗ trợ kỹ thuật", "primary_claim": "Hotline cá nhân: 0912.345.678 hoặc (+84) 903 111 222"}
    f1 = agent.audit(s1)
    p_f1 = [f for f in f1 if "điện thoại" in f.issue.lower()]
    results["Case 1 (Formatted Phone Numbers)"] = len(p_f1) >= 2

    # Case 2: Formatted CCCD
    s2 = {"slide_id": "c2", "assertion_title": "Thông tin nhân sự phụ trách", "primary_claim": "Số Căn cước công dân: 001 095 012 345"}
    f2 = agent.audit(s2)
    cccd_f = [f for f in f2 if "căn cước" in f.issue.lower() or "cccd" in f.issue.lower()]
    results["Case 2 (Formatted CCCD)"] = len(cccd_f) >= 1

    # Case 3: Public Corporate Email (NO FALSE POSITIVE)
    s3 = {"slide_id": "c3", "assertion_title": "Cổng thông tin tiếp nhận", "primary_claim": "Gửi hồ sơ về contact@vinfastauto.com hoặc info@fpt.com.vn"}
    f3 = agent.audit(s3)
    results["Case 3 (Corporate Email - No False Positive)"] = len(f3) == 0

    # Case 4: Personal Email Leak
    s4 = {"slide_id": "c4", "assertion_title": "Tác giả đề án", "primary_claim": "Email tác giả: nguyen.van.a@gmail.com"}
    f4 = agent.audit(s4)
    email_f = [f for f in f4 if "nguyen.van.a@gmail.com" in (f.evidence or "") or "nguyen.van.a@gmail.com" in (f.original_value or "") or "nguyen.van.a@gmail.com" in f.issue]
    results["Case 4 (Personal Email Leak)"] = len(email_f) >= 1

    # Case 5: AWS & OpenAI Key
    s5 = {"slide_id": "c5", "assertion_title": "Cấu hình API kết nối", "primary_claim": "API Key: AKIAIOSFODNN7EXAMPLE và sk-proj-1234567890abcdef12345678"}
    f5 = agent.audit(s5)
    key_f = [f for f in f5 if f.severity == Severity.P0 and ("api" in f.issue.lower() or "khóa" in f.issue.lower() or "secret" in f.issue.lower())]
    results["Case 5 (API Keys / Secrets)"] = len(key_f) >= 1

    # Case 6: JWT Token
    s6 = {"slide_id": "c6", "assertion_title": "Token xác thực", "primary_claim": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.doNotLeakThis"}
    f6 = agent.audit(s6)
    jwt_f = [f for f in f6 if f.severity == Severity.P0 and ("jwt" in f.issue.lower() or "token" in f.issue.lower() or "khóa" in f.issue.lower())]
    results["Case 6 (JWT Token)"] = len(jwt_f) >= 1

    # Case 7: Credit Card
    s7 = {"slide_id": "c7", "assertion_title": "Thông tin thanh toán mẫu", "primary_claim": "Thẻ Visa: 4532 1234 5678 9012"}
    f7 = agent.audit(s7)
    card_f = [f for f in f7 if f.severity == Severity.P0 and ("thẻ" in f.issue.lower() or "card" in f.issue.lower())]
    results["Case 7 (Credit Card Leak)"] = len(card_f) >= 1

    # Case 8: Confidential Marker
    s8 = {"slide_id": "c8", "assertion_title": "Kế hoạch M&A chiến lược", "primary_claim": "TÀI LIỆU LƯU HÀNH NỘI BỘ - TUYỆT MẬT"}
    f8 = agent.audit(s8)
    conf_f = [f for f in f8 if f.severity == Severity.P0 and ("tuyệt mật" in f.issue.lower() or "nội bộ" in f.issue.lower())]
    results["Case 8 (Confidential Marker)"] = len(conf_f) >= 1

    # Case 9: Large Financial Number (NO FALSE POSITIVE as CMND)
    s9 = {"slide_id": "c9", "assertion_title": "Ngân sách dự toán", "primary_claim": "Tổng kinh phí phê duyệt là 500000000 VNĐ (500 triệu)"}
    f9 = agent.audit(s9)
    # Must NOT flag 500000000 as CMND
    cmnd_false = [f for f in f9 if "cmnd" in f.issue.lower() or "căn cước" in f.issue.lower()]
    results["Case 9 (Financial Number - No False Positive)"] = len(cmnd_false) == 0

    # Case 10: Auto-Remediation Masking Integrity
    s10 = {"slide_id": "c10", "assertion_title": "Liên hệ", "primary_claim": "Gặp anh Nam CCCD: 001095012345, SĐT: 0912345678, email: nam@gmail.com"}
    f10 = agent.audit(s10)
    rem10 = agent.auto_remediate(s10, f10)
    claim10 = rem10["primary_claim"]
    masked_ok = ("001095" in claim10 and "012345" not in claim10) and ("0912" in claim10 and "345678" not in claim10) and ("nam@gmail.com" not in claim10)
    results["Case 10 (Auto-Remediation Masking)"] = masked_ok

    return results


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING ADVERSARIAL STRESS TEST MATRIX FOR AGENT 02")
    print("=" * 60)
    res = run_all_adversarial_tests()
    passed_count = sum(1 for v in res.values() if v)
    total_count = len(res)

    for case_name, passed in res.items():
        status = "PASSED" if passed else "FAILED"
        icon = "✔" if passed else "✘"
        print(f"{icon} [{status}] {case_name}")

    print("-" * 60)
    print(f"Total Score: {passed_count}/{total_count} ({passed_count/total_count*100:.1f}%)")
    print("=" * 60)

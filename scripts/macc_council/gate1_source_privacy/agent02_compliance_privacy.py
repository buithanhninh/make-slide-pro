"""
scripts/macc_council/gate1_source_privacy/agent02_compliance_privacy.py
Agent 2: CompliancePrivacyGuardian (Vệ Binh Pháp Lý & Bí Mật Doanh Nghiệp)
Detects PII leaks, exposed credentials, API keys, and sensitive enterprise markers.
"""

from __future__ import annotations

import re
import json
from typing import Any, Dict, List, Optional
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, Severity


class CompliancePrivacyGuardian(BaseCouncilAgent):
    """Audits privacy compliance, PII leaks (CCCD, phone, email), and confidential secrets."""

    def __init__(self):
        super().__init__(name="CompliancePrivacyGuardian", gate="Gate 1: Source Veracity & Privacy")

    def audit(self, slide: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> List[AgentFinding]:
        findings = []
        slide_id = slide.get("slide_id", "UNKNOWN")
        text = self.extract_slide_text(slide)

        # 1. Citizen ID (CCCD 12 digits or CMND 9 digits)
        cccd_matches = re.findall(r"\b(0\d{11}|\b\d{9})\b", text)
        for c in cccd_matches:
            # Avoid matching standard 9-digit financial amounts like 100000000 by checking context
            if any(w in text.lower() for w in ["cccd", "cmnd", "căn cước", "chứng minh"]):
                findings.append(AgentFinding(
                    agent=self.name,
                    gate=self.gate,
                    slide_id=slide_id,
                    severity=Severity.P0,
                    issue=f"Phát hiện số Căn cước công dân (CCCD) / CMND nhạy cảm: '{c}'.",
                    rationale="Vi phạm nghiêm trọng Nghị định 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân.",
                    suggestion="Che mờ số CCCD định danh (Ví dụ: '001099******').",
                    original_value=c,
                    suggested_value=f"{c[:6]}******"
                ))

        # 2. Vietnamese Mobile Phone Numbers (09xx, 08xx, 03xx, 07xx, 05xx)
        phone_matches = re.findall(r"(?:\+84|0)(?:3[2-9]|5[6|8|9]|7[0|6-9]|8[1-5]|9[0-4|6-9])[0-9]{7}\b", text)
        for p in phone_matches:
            findings.append(AgentFinding(
                agent=self.name,
                gate=self.gate,
                slide_id=slide_id,
                severity=Severity.P1,
                issue=f"Phát hiện số điện thoại cá nhân chưa ẩn danh: '{p}'.",
                rationale="Số điện thoại cá nhân không được xuất hiện công khai trên slide trình chiếu.",
                suggestion=f"Ẩn danh số điện thoại (Ví dụ: '{p[:4]}***{p[-3:]}').",
                original_value=p,
                suggested_value=f"{p[:4]}***{p[-3:]}"
            ))

        # 3. Personal Emails (@gmail.com, @yahoo.com)
        personal_emails = re.findall(r"\b[A-Za-z0-9._%+-]+@(gmail\.com|yahoo\.com|hotmail\.com)\b", text, re.IGNORECASE)
        for e_domain in personal_emails:
            full_emails = re.findall(r"\b[A-Za-z0-9._%+-]+@" + re.escape(e_domain) + r"\b", text, re.IGNORECASE)
            for fe in full_emails:
                findings.append(AgentFinding(
                    agent=self.name,
                    gate=self.gate,
                    slide_id=slide_id,
                    severity=Severity.P1,
                    issue=f"Phát hiện địa chỉ email cá nhân: '{fe}'.",
                    rationale="Bảo vệ quyền riêng tư của nhân sự và khách hàng.",
                    suggestion="Che bớt địa chỉ email hoặc thay bằng email phòng ban chung.",
                    original_value=fe,
                    suggested_value="contact@doanhnghiep.vn"
                ))

        # 4. API Keys & Secrets (AIza..., sk-..., ghp_..., password=...)
        secret_patterns = [
            r"\bAIza[0-9A-Za-z-_]{35}\b",
            r"\bsk-[a-zA-Z0-9]{20,}\b",
            r"\bghp_[a-zA-Z0-9]{36}\b",
            r"(?:mật\s*khẩu|password)\s*[:=]\s*['\"]?(\S+)['\"]?"
        ]
        for pat in secret_patterns:
            matches = re.findall(pat, text, re.IGNORECASE)
            if matches:
                findings.append(AgentFinding(
                    agent=self.name,
                    gate=self.gate,
                    slide_id=slide_id,
                    severity=Severity.P0,
                    issue="Phát hiện khóa bí mật / Mật khẩu / API Key trong nội dung slide.",
                    rationale="Nguy cơ lộ lọt thông tin an ninh mạng và tài khoản hệ thống nghiêm trọng.",
                    suggestion="Xóa bỏ hoàn toàn mã khóa bảo mật khỏi bài thuyết trình.",
                    original_value=str(matches[0])
                ))

        # 5. Strict Confidentiality Markers (INTERNAL ONLY, TUYỆT MẬT)
        confidential_markers = ["tuyệt mật", "strictly confidential", "internal only", "không phổ biến ra ngoài"]
        for cm in confidential_markers:
            if cm in text.lower():
                findings.append(AgentFinding(
                    agent=self.name,
                    gate=self.gate,
                    slide_id=slide_id,
                    severity=Severity.P1,
                    issue=f"Tài liệu chứa nhãn nhạy cảm doanh nghiệp: '{cm.upper()}'.",
                    rationale="Cần cảnh báo người dùng trước khi trình chiếu tại hội nghị công cộng.",
                    suggestion="Gỡ nhãn nhạy cảm hoặc thay thế bằng phiên bản tài liệu công bố công khai.",
                    original_value=cm
                ))

        return findings

    def auto_remediate(self, slide: Dict[str, Any], findings: List[AgentFinding], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Auto-remediates PII by masking sensitive patterns in-place."""
        slide_json = json.dumps(slide, ensure_ascii=False)
        for f in findings:
            if f.original_value and f.suggested_value:
                slide_json = slide_json.replace(f.original_value, f.suggested_value)
        return json.loads(slide_json)

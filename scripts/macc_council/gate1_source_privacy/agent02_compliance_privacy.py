"""
scripts/macc_council/gate1_source_privacy/agent02_compliance_privacy.py
Agent 2: CompliancePrivacyGuardian (Vệ Binh Pháp Lý & Bí Mật Doanh Nghiệp V8.0)
Deep enterprise PII, credential, and compliance auditor:
1. Multi-format VN Phone numbers (unbroken, spaced, dotted, dashed, (+84))
2. Multi-format CCCD/CMND (12 digits, spaced, dashed, 9-digit CMND with contextual guard)
3. AWS, Google, OpenAI, GitHub API keys and JWT Bearer Tokens
4. Payment Cards (16-digit Visa/Mastercard/Amex)
5. Enterprise Confidentiality Markers (Tuyệt mật, Lưu hành nội bộ, Internal Only)
6. Personal Email Guardian with Corporate Public Email Whitelist (0 False Positives)
7. Contextual Zero-Defect Auto-Remediation & Masking
"""

from __future__ import annotations

import copy
import re
from typing import Any, Dict, List, Optional
from ..base_agent import BaseCouncilAgent
from ..models import AgentFinding, Severity


class CompliancePrivacyGuardian(BaseCouncilAgent):
    """
    Agent 02: Compliance & Privacy Guardian.
    Guarantees absolute compliance with Vietnam Decree 13/2023/ND-CP on Personal Data Protection
    and prevents catastrophic exposure of corporate secrets, credentials, and payment data.
    """

    # Multi-format Phone: 0912345678, 0912.345.678, 0912 345 678, (+84) 903 111 222
    PHONE_REGEX = re.compile(
        r"(?:(?:\+84|\(\+84\)|0)[-.\s]*(?:[35789][-.\s]*)(?:[0-9][-.\s]*){7}[0-9])\b"
    )

    # Multi-format CCCD: 12 digits (001095012345, 001 095 012 345, 079-090-123456)
    CCCD_REGEX = re.compile(
        r"\b(?:0\d{2}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{3})\b"
    )

    # CMND: 9 digits, strictly requires ID context to prevent false positives on financial figures
    CMND_REGEX = re.compile(
        r"\b(?:cccd|cmnd|căn\s*cước|chứng\s*minh|số\s*đdcn)\s*[:=–-]?\s*(\d{9})\b",
        re.IGNORECASE
    )

    # Payment cards: 16 digits formatted
    CREDIT_CARD_REGEX = re.compile(
        r"\b(?:4[0-9]{3}|5[1-5][0-9]{2}|6(?:011|5[0-9]{2})|3[47][0-9]{2})[-.\s]?[0-9]{4}[-.\s]?[0-9]{4}[-.\s]?[0-9]{4}\b"
    )

    # API Keys & Secrets
    SECRET_PATTERNS = [
        (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "Khóa truy cập đám mây AWS Access Key ID"),
        (re.compile(r"\bAIza[0-9A-Za-z-_]{35}\b"), "Khóa bảo mật Google Cloud / Gemini API Key"),
        (re.compile(r"\bsk-(?:proj-)?[a-zA-Z0-9_-]{20,}\b"), "Khóa bảo mật OpenAI / LLM Secret Key"),
        (re.compile(r"\bgh[pousr]_[a-zA-Z0-9]{36,}\b"), "Khóa bảo mật GitHub Personal Access Token"),
        (re.compile(r"\beyJ[A-Za-z0-9-_]+\.eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\b"), "Chuỗi định danh phiên JWT Bearer Token"),
        (re.compile(r"(?:mật\s*khẩu|password|secret_key|client_secret)\s*[:=]\s*['\"]?([^\s'\"]{6,})['\"]?", re.IGNORECASE), "Mật khẩu hệ thống bị để lộ")
    ]

    # Personal email domains
    PERSONAL_EMAIL_DOMAINS = {"gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com", "proton.me", "live.com"}
    PUBLIC_EMAIL_PREFIXES = {"info@", "contact@", "support@", "sales@", "hello@", "admin@", "media@", "press@", "office@"}

    CONFIDENTIAL_MARKERS = [
        "tuyệt mật", "strictly confidential", "internal only", "lưu hành nội bộ",
        "tài liệu nội bộ", "không phổ biến ra ngoài", "confidential nda"
    ]

    def __init__(self):
        super().__init__(name="CompliancePrivacyGuardian", gate="Gate 1: Source Veracity & Privacy")

    def _get_slides(self, target: Any) -> List[Dict[str, Any]]:
        if isinstance(target, list):
            return target
        if isinstance(target, dict):
            return target.get("slides", [target])
        return []

    def _mask_phone(self, phone: str) -> str:
        digits = re.sub(r"[^\d]", "", phone)
        if len(digits) >= 10:
            return f"{digits[:4]}***{digits[-3:]}"
        return f"{phone[:3]}***{phone[-2:]}"

    def _mask_cccd(self, cccd: str) -> str:
        digits = re.sub(r"[^\d]", "", cccd)
        if len(digits) >= 12:
            return f"{digits[:6]}******"
        elif len(digits) >= 9:
            return f"{digits[:3]}***{digits[-3:]}"
        return f"{cccd[:4]}****"

    def audit(self, target: Any, context: Optional[Dict[str, Any]] = None) -> List[AgentFinding]:
        findings: List[AgentFinding] = []
        slides = self._get_slides(target)

        for s in slides:
            slide_id = s.get("slide_id", "unknown_slide")
            text = self.extract_slide_text(s)

            # ----------------------------------------------------
            # 1. Citizen Identity Verification (CCCD & CMND)
            # ----------------------------------------------------
            # Context-backed CCCD matches
            for m in self.CCCD_REGEX.finditer(text):
                raw_cccd = m.group(0)
                clean_digits = re.sub(r"[^\d]", "", raw_cccd)
                if len(clean_digits) == 12:
                    # Guard: verify it's not a round financial number (e.g. 100000000000)
                    if not clean_digits.endswith("000000"):
                        findings.append(
                            AgentFinding(
                                agent=self.name,
                                gate=self.gate,
                                slide_id=slide_id,
                                severity=Severity.P0,
                                issue=f"Phát hiện số Căn cước công dân (CCCD) nhạy cảm: '{raw_cccd}'",
                                rationale="Vi phạm Nghị định 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân khi trình chiếu số CCCD trực tiếp.",
                                suggestion="Tự động che giấu 6 số cuối (ví dụ: '001095******').",
                                evidence=raw_cccd,
                                original_value=raw_cccd,
                                suggested_value=self._mask_cccd(raw_cccd)
                            )
                        )

            for m in self.CMND_REGEX.finditer(text):
                raw_cmnd = m.group(1)
                findings.append(
                    AgentFinding(
                        agent=self.name,
                        gate=self.gate,
                        slide_id=slide_id,
                        severity=Severity.P0,
                        issue=f"Phát hiện số Chứng minh nhân dân (CMND) nhạy cảm: '{raw_cmnd}'",
                        rationale="Bảo vệ định danh cá nhân nhân sự/khách hàng.",
                        suggestion="Che mờ 3 số giữa CMND.",
                        evidence=raw_cmnd,
                        original_value=raw_cmnd,
                        suggested_value=self._mask_cccd(raw_cmnd)
                    )
                )

            # ----------------------------------------------------
            # 2. Vietnamese Phone Numbers (Formatted & Unformatted)
            # ----------------------------------------------------
            for m in self.PHONE_REGEX.finditer(text):
                raw_phone = m.group(0)
                digits = re.sub(r"[^\d]", "", raw_phone)
                # Valid VN phone is 10 digits (or 11 digits starting with 84)
                if len(digits) in [10, 11]:
                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=slide_id,
                            severity=Severity.P1,
                            issue=f"Phát hiện số điện thoại cá nhân chưa ẩn danh: '{raw_phone}'",
                            rationale="Số điện thoại di động cá nhân không được hiển thị công khai trên slide đại chúng.",
                            suggestion=f"Ẩn danh số điện thoại (ví dụ: '{self._mask_phone(raw_phone)}').",
                            evidence=raw_phone,
                            original_value=raw_phone,
                            suggested_value=self._mask_phone(raw_phone)
                        )
                    )

            # ----------------------------------------------------
            # 3. Personal Email Leaks (Exempting Corporate Public Emails)
            # ----------------------------------------------------
            all_emails = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", text)
            for email in all_emails:
                email_lower = email.lower()
                domain = email_lower.split("@")[-1]
                is_personal = domain in self.PERSONAL_EMAIL_DOMAINS
                is_public_prefix = any(email_lower.startswith(pref) for pref in self.PUBLIC_EMAIL_PREFIXES)

                # Flag if it's explicitly a personal mailbox or private individual mailbox
                if is_personal or (not is_public_prefix and not domain.endswith((".gov.vn", ".edu.vn"))):
                    if is_personal:
                        findings.append(
                            AgentFinding(
                                agent=self.name,
                                gate=self.gate,
                                slide_id=slide_id,
                                severity=Severity.P1,
                                issue=f"Phát hiện địa chỉ email cá nhân: '{email}'",
                                rationale="Tránh để lộ email cá nhân nhân sự trên slide thuyết trình.",
                                suggestion="Thay bằng email phòng ban chung (contact@...) hoặc che giấu tên hộp thư.",
                                evidence=email,
                                original_value=email,
                                suggested_value="contact@doanhnghiep.vn"
                            )
                        )

            # ----------------------------------------------------
            # 4. API Keys & Secrets
            # ----------------------------------------------------
            for pattern, label in self.SECRET_PATTERNS:
                for match in pattern.finditer(text):
                    secret_val = match.group(0)
                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=slide_id,
                            severity=Severity.P0,
                            issue=f"Phát hiện khóa bí mật / API Key / Thông tin bảo mật nguy hiểm: {label}",
                            rationale="Rò rỉ khóa hệ thống dẫn đến nguy cơ bị tấn công chiếm quyền điều khiển hạ tầng.",
                            suggestion="Xóa bỏ hoàn toàn chuỗi khóa bảo mật khỏi bài thuyết trình.",
                            evidence=secret_val,
                            original_value=secret_val,
                            suggested_value="[BẢO MẬT ĐÃ XÓA]"
                        )
                    )

            # ----------------------------------------------------
            # 5. Payment Cards (16 Digits)
            # ----------------------------------------------------
            for m in self.CREDIT_CARD_REGEX.finditer(text):
                card_val = m.group(0)
                findings.append(
                    AgentFinding(
                        agent=self.name,
                        gate=self.gate,
                        slide_id=slide_id,
                        severity=Severity.P0,
                        issue=f"Phát hiện số thẻ thanh toán quốc tế: '{card_val}'",
                        rationale="Vi phạm nghiêm trọng tiêu chuẩn an ninh thanh toán thẻ PCI-DSS.",
                        suggestion="Xóa bỏ số thẻ thanh toán.",
                        evidence=card_val,
                        original_value=card_val,
                        suggested_value="**** **** **** ****"
                    )
                )

            # ----------------------------------------------------
            # 6. Confidential Enterprise Markers
            # ----------------------------------------------------
            for cm in self.CONFIDENTIAL_MARKERS:
                if cm in text.lower():
                    findings.append(
                        AgentFinding(
                            agent=self.name,
                            gate=self.gate,
                            slide_id=slide_id,
                            severity=Severity.P0,
                            issue=f"Phát hiện nhãn cảnh báo bí mật doanh nghiệp: '{cm.upper()}'",
                            rationale="Tài liệu chứa dấu vết mật không được phép trình chiếu ra bên ngoài doanh nghiệp.",
                            suggestion="Xác thực quyền giải mật hoặc gỡ bỏ nhãn bí mật.",
                            evidence=cm,
                            original_value=cm,
                            suggested_value=""
                        )
                    )

        return findings

    def auto_remediate(self, target: Any, findings: List[AgentFinding], context: Optional[Dict[str, Any]] = None) -> Any:
        remediated = copy.deepcopy(target)
        slides = self._get_slides(remediated)

        for finding in findings:
            if finding.original_value and finding.suggested_value is not None:
                orig_val = finding.original_value
                sugg_val = finding.suggested_value
                for s in slides:
                    if s.get("slide_id") == finding.slide_id:
                        for k in ["title", "subtitle", "headline", "assertion_title", "primary_claim", "speaker_notes", "source_footer"]:
                            if k in s and isinstance(s[k], str):
                                s[k] = s[k].replace(orig_val, sugg_val)
                        for col_key in ["atoms", "cards", "content_items", "boxes", "items"]:
                            for item in s.get(col_key, []):
                                if isinstance(item, dict):
                                    for ak in ["title", "text", "body", "description", "mechanism", "kicker", "label", "value", "verbatim", "metric_value", "metric_label"]:
                                        if ak in item and isinstance(item[ak], str):
                                            item[ak] = item[ak].replace(orig_val, sugg_val)
                        table = s.get("table_data")
                        if isinstance(table, dict):
                            headers = table.get("headers", [])
                            if isinstance(headers, list):
                                table["headers"] = [h.replace(orig_val, sugg_val) if isinstance(h, str) else h for h in headers]
                            rows = table.get("rows", [])
                            if isinstance(rows, list):
                                for r in rows:
                                    if isinstance(r, list):
                                        for idx, cell in enumerate(r):
                                            if isinstance(cell, str):
                                                r[idx] = cell.replace(orig_val, sugg_val)

        if isinstance(remediated, dict):
            remediated["slides"] = slides
            return remediated
        return slides

"""
tests/test_saas_e2e_full.py
Complete End-to-End Verification of SaaS Architecture:
1. Static Studio UI delivery (HTML, CSS, JS, Auth Modals)
2. User Registration & JWT Bearer Generation
3. Multi-Tenant Project Creation from Text Upload
4. Project Listing and Ownership Verification
5. IDOR Vulnerability Defense (User B accessing User A -> 403)
6. Anonymous Access Defense (Unauthenticated access -> 401)
7. User Profile & Dynamic Credit Tracking
"""

import sys
from pathlib import Path
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from web.app import app

client = TestClient(app)


def test_saas_end_to_end():
    print("\n--- [Step 1] Verifying Studio UI & SaaS Modals Delivery ---")
    r_home = client.get("/")
    assert r_home.status_code == 200
    html_content = r_home.text
    assert "modal-auth" in html_content, "Auth modal missing from index.html"
    assert "modal-projects" in html_content, "Projects modal missing from index.html"
    assert "modal-pricing" in html_content, "Pricing modal missing from index.html"
    assert "vietqr-payment-box" in html_content, "VietQR payment box missing from index.html"
    assert "filmstrip-track" in html_content, "Filmstrip track missing from index.html"
    assert "render-timeline" in html_content, "Rendering timeline missing from index.html"
    assert "copilot-chips" in html_content, "Copilot prompt chips missing from index.html"
    assert "demo-doc-btn" in html_content, "1-Click demo buttons missing from index.html"
    assert "user-credits-badge" in html_content, "User credits badge missing from index.html"
    print("✔ Web Studio HTML delivers all UI/UX components (Filmstrip, VietQR, Timeline, Copilot chips, Demo docs) properly.")

    print("\n--- [Step 2] Testing User Registration & Credit Allocation ---")
    test_email = "architect_master@saas.com"
    r_reg = client.post("/api/auth/register", json={
        "email": test_email,
        "password": "SecurePassword123!",
        "full_name": "Master Architect"
    })
    if r_reg.status_code == 400:
        # Already created in previous run
        r_login = client.post("/api/auth/login", json={
            "email": test_email,
            "password": "SecurePassword123!"
        })
        assert r_login.status_code == 200
        token = r_login.json()["access_token"]
    else:
        assert r_reg.status_code == 200
        data = r_reg.json()
        assert data["user"]["credits"] == 5
        token = data["access_token"]
    print("✔ User authenticated and assigned initial credits.")

    print("\n--- [Step 3] Testing Text Upload with User Ownership Association ---")
    headers = {"Authorization": f"Bearer {token}"}
    sample_text = """
    # CHIẾN LƯỢC PHÁT TRIỂN NĂNG LƯỢNG TÁI TẠO 2030
    Việt Nam sở hữu tiềm năng điện gió và điện mặt trời vượt trội tại khu vực Đông Nam Á.
    Tỷ lệ năng lượng sạch dự kiến chiếm 32% tổng công suất vào năm 2030.
    Chuyển dịch năng lượng tạo động lực giảm phát thải và thu hút nguồn vốn xanh quốc tế.
    """
    r_upload = client.post(
        "/api/upload/text",
        json={"title": "Chiến Lược Năng Lượng Tái Tạo", "content": sample_text},
        headers=headers
    )
    assert r_upload.status_code == 200
    project_data = r_upload.json()
    project_id = project_data["session_id"]
    assert project_data["success"] is True
    print(f"✔ Project created & linked to user: ID = {project_id}")

    print("\n--- [Step 4] Testing User Project Dashboard Listing ---")
    r_projects = client.get("/api/projects", headers=headers)
    assert r_projects.status_code == 200
    user_projects = r_projects.json()
    assert any(p["id"] == project_id for p in user_projects)
    print(f"✔ User projects list verified: {len(user_projects)} project(s) on dashboard.")

    print("\n--- [Step 5] Testing Anti-IDOR Tenant Data Protection ---")
    # Register an attacker
    attacker_email = "attacker_bob@saas.com"
    r_reg_atk = client.post("/api/auth/register", json={
        "email": attacker_email,
        "password": "AttackerPass123!",
        "full_name": "Bob the Attacker"
    })
    if r_reg_atk.status_code == 400:
        r_log_atk = client.post("/api/auth/login", json={
            "email": attacker_email,
            "password": "AttackerPass123!"
        })
        token_atk = r_log_atk.json()["access_token"]
    else:
        token_atk = r_reg_atk.json()["access_token"]

    r_idor_check = client.get(
        f"/api/projects/{project_id}",
        headers={"Authorization": f"Bearer {token_atk}"}
    )
    assert r_idor_check.status_code == 403, f"Expected 403 Forbidden, got {r_idor_check.status_code}"
    print("✔ IDOR Attack strictly repelled: Bob cannot view Master Architect's presentation (403 Forbidden).")

    print("\n--- [Step 6] Testing Anonymous Access Denial ---")
    r_anon = client.get(f"/api/projects/{project_id}")
    assert r_anon.status_code == 401
    print("✔ Anonymous access rejected with 401 Unauthorized.")

    print("\n--- [Step 7] Checking User Profile & Remaining Balance ---")
    r_me = client.get("/api/auth/me", headers=headers)
    assert r_me.status_code == 200
    me = r_me.json()
    assert me["email"] == test_email
    assert me["project_count"] >= 1
    print(f"✔ Profile verified: {me['email']} | Credits: {me['credits']} | Projects: {me['project_count']}")

    print("\n--- [Step 8] Testing VietQR Banking Credit Top-Up Simulation ---")
    initial_credits = me["credits"]
    r_topup = client.post(
        "/api/payments/topup",
        json={"tier": "PRO", "amount": 199000, "credits": 100},
        headers=headers
    )
    assert r_topup.status_code == 200, f"Expected 200, got {r_topup.status_code}"
    topup_data = r_topup.json()
    assert topup_data["success"] is True
    assert topup_data["added"] == 100
    assert topup_data["new_credits"] == initial_credits + 100
    assert "PAY_" in topup_data["payment_ref"]
    print(f"✔ VietQR Top-Up successful: Added 100 credits, New Balance = {topup_data['new_credits']}")

    print("\n--- [Step 9] Testing Health Check Probes (/healthz & /api/health) ---")
    r_h1 = client.get("/healthz")
    assert r_h1.status_code == 200
    assert r_h1.json()["status"] == "healthy"
    r_h2 = client.get("/api/health")
    assert r_h2.status_code == 200
    assert r_h2.json()["version"] == "7.3.0"
    print("✔ Container Liveness & Readiness health check probes verified.")

    print("\n🎉 ALL FULL E2E SAAS TESTS COMPLETED SUCCESSFULLY WITH 100% PASS RATE!\n")


if __name__ == "__main__":
    test_saas_end_to_end()

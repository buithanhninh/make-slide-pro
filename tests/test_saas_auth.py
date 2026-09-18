"""
tests/test_saas_auth.py
Automated Multi-Tenant SaaS Security & Data Isolation Test Suite
Verifies:
- User registration & JWT authentication
- Tenant data isolation (User B cannot access User A's project -> 403 Forbidden)
- Credit management & deduction
- Unauthenticated access prevention (401 Unauthorized)
"""

import os
import sys
from pathlib import Path
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from web.app import app
from web.database import SessionLocal, User, Project

client = TestClient(app)


def test_saas_multi_tenant_isolation_and_credits():
    # 1. Register User A
    r_reg_a = client.post("/api/auth/register", json={
        "email": "alice@saas.com",
        "password": "password123",
        "full_name": "Alice Slide Architect"
    })
    if r_reg_a.status_code == 400 and "Email này đã được đăng ký" in r_reg_a.text:
        # Already exists, log in
        r_login_a = client.post("/api/auth/login", json={
            "email": "alice@saas.com",
            "password": "password123"
        })
        assert r_login_a.status_code == 200
        token_a = r_login_a.json()["access_token"]
    else:
        assert r_reg_a.status_code == 200
        token_a = r_reg_a.json()["access_token"]
        assert r_reg_a.json()["user"]["credits"] == 5
    print("✔ User A registered/logged in with 5 free credits.")

    # 2. Register User B
    r_reg_b = client.post("/api/auth/register", json={
        "email": "bob@saas.com",
        "password": "password123",
        "full_name": "Bob Guest"
    })
    if r_reg_b.status_code == 400 and "Email này đã được đăng ký" in r_reg_b.text:
        r_login_b = client.post("/api/auth/login", json={
            "email": "bob@saas.com",
            "password": "password123"
        })
        assert r_login_b.status_code == 200
        token_b = r_login_b.json()["access_token"]
    else:
        assert r_reg_b.status_code == 200
        token_b = r_reg_b.json()["access_token"]
    print("✔ User B registered/logged in.")

    # 3. Verify Profile Endpoint for User A
    r_me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token_a}"})
    assert r_me.status_code == 200
    me_data = r_me.json()
    assert me_data["email"] == "alice@saas.com"
    print(f"✔ Profile verified: {me_data['full_name']} | Credits: {me_data['credits']}")

    # 4. User A creates a project from test_sample_document.docx
    doc_path = PROJECT_ROOT / "test_sample_document.docx"
    assert doc_path.exists()

    with open(doc_path, "rb") as f:
        r_upload = client.post(
            "/api/projects/upload",
            files={"file": ("test_sample_document.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
            data={"depth_mode": "DEEP"},
            headers={"Authorization": f"Bearer {token_a}"}
        )
    assert r_upload.status_code == 200
    p_data = r_upload.json()
    project_id = p_data["project_id"]
    print(f"✔ User A created Project: '{p_data['title']}' (ID={project_id})")

    # 5. User A can view own project
    r_view_a = client.get(f"/api/projects/{project_id}", headers={"Authorization": f"Bearer {token_a}"})
    assert r_view_a.status_code == 200
    assert r_view_a.json()["id"] == project_id
    print("✔ User A can access own project successfully.")

    # 6. TENANT ISOLATION CHECK: User B attempts to access User A's project -> MUST BE 403 FORBIDDEN
    r_view_b = client.get(f"/api/projects/{project_id}", headers={"Authorization": f"Bearer {token_b}"})
    assert r_view_b.status_code == 403, f"Expected 403 Forbidden for User B, got {r_view_b.status_code}"
    print("✔ CRITICAL SECURITY PASS: User B cannot access User A's project (403 Forbidden verified).")

    # 7. Unauthenticated access without token -> MUST BE 401 UNAUTHORIZED
    r_anon = client.get(f"/api/projects/{project_id}")
    assert r_anon.status_code == 401
    print("✔ Unauthenticated access correctly rejected with 401 Unauthorized.")

    # 8. User A triggers render -> Credit deducted from 5 to 4
    init_credits = me_data["credits"]
    r_render = client.post(
        f"/api/projects/{project_id}/render",
        json={"session_id": project_id, "theme": "DARK"},
        headers={"Authorization": f"Bearer {token_a}"}
    )
    assert r_render.status_code == 200
    render_res = r_render.json()
    assert render_res["remaining_credits"] == init_credits - 1
    print(f"✔ Render triggered successfully. Credit deducted: {init_credits} -> {render_res['remaining_credits']}")

    # 9. Verify Resilient Status Recovery Endpoint
    r_status = client.get(f"/api/projects/{project_id}/status", headers={"Authorization": f"Bearer {token_a}"})
    assert r_status.status_code == 200
    assert r_status.json()["project_id"] == project_id
    print("✔ Resilient Status Recovery endpoint verified.")


if __name__ == "__main__":
    test_saas_multi_tenant_isolation_and_credits()
    print("\n🎉 ALL SAAS SECURITY & MULTI-TENANCY TESTS PASSED 100%!")

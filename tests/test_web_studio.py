"""
tests/test_web_studio.py
End-to-end API verification suite for Make Slide Pro Web Studio V7.3.
"""

import os
import sys
from pathlib import Path
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from web.app import app

client = TestClient(app)


def test_root_serves_spa():
    response = client.get("/")
    assert response.status_code == 200
    assert "Make Slide Pro Studio" in response.text
    print("✔ test_root_serves_spa passed.")


def test_asset_endpoints():
    r_ill = client.get("/api/assets/illustrations")
    assert r_ill.status_code == 200
    ills = r_ill.json()
    assert len(ills) >= 20
    assert any("ai_bai_1_community" in i["name"] for i in ills)

    r_charts = client.get("/api/assets/charts")
    assert r_charts.status_code == 200
    charts = r_charts.json()
    assert len(charts) >= 10
    print("✔ test_asset_endpoints passed.")


def test_upload_and_blueprint_lifecycle():
    doc_path = PROJECT_ROOT / "test_sample_document.docx"
    assert doc_path.exists(), "test_sample_document.docx must exist"

    with open(doc_path, "rb") as f:
        r_upload = client.post(
            "/api/upload/file",
            files={"file": ("test_sample_document.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
            data={"depth_mode": "DEEP"}
        )
    assert r_upload.status_code == 200
    data = r_upload.json()
    assert data["success"] is True
    session_id = data["session_id"]
    stats = data["stats"]
    assert stats["sections"] >= 3
    assert stats["slides"] >= 6
    print(f"✔ File uploaded. Session={session_id}, Slides={stats['slides']}")

    # Test Blueprint QA
    r_qa = client.post("/api/blueprint/qa", json={"session_id": session_id})
    assert r_qa.status_code == 200
    qa_data = r_qa.json()
    assert qa_data["score"] >= 90.0
    print(f"✔ MACC-QA certified with score: {qa_data['score']}/100")

    # Test AI Copilot
    r_copilot = client.post(
        "/api/copilot",
        json={"session_id": session_id, "command": "đổi slide 2 thành dạng SO SÁNH"}
    )
    assert r_copilot.status_code == 200
    copilot_data = r_copilot.json()
    assert copilot_data["success"] is True
    assert copilot_data["modified"] is True
    slides = copilot_data["blueprints"]["slides"]
    assert slides[1]["visual_job"] == "COMPARISON"
    print(f"✔ Copilot command executed: {copilot_data['message']}")

    # Test Text Upload
    r_text = client.post(
        "/api/upload/text",
        json={
            "title": "Chuyên Đề Trí Tuệ Nhân Tạo",
            "content": "Trí tuệ nhân tạo là nền tảng của chuyển đổi số. Phương trình chuẩn hóa: Y = W*X + b. Bảng số liệu phân bổ gồm 3 cột."
        }
    )
    assert r_text.status_code == 200
    text_data = r_text.json()
    assert text_data["success"] is True
    print(f"✔ Text upload successful. Session={text_data['session_id']}")


if __name__ == "__main__":
    test_root_serves_spa()
    test_asset_endpoints()
    test_upload_and_blueprint_lifecycle()
    print("\n🎉 ALL WEB STUDIO TESTS PASSED 100%!")

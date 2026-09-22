from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_check_rejects_empty_resume():
    response = client.post("/api/check", json={})
    assert response.status_code == 400


def test_import_rejects_unsupported_file_type():
    response = client.post(
        "/api/import", files={"file": ("resume.exe", b"not a resume", "application/octet-stream")}
    )
    assert response.status_code == 400


def test_import_rejects_empty_txt():
    response = client.post("/api/import", files={"file": ("resume.txt", b"   ", "text/plain")})
    assert response.status_code == 400

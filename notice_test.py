from dotenv import load_dotenv

load_dotenv('_env/dev.env', override=True)

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock
from datetime import datetime
from server.app import app

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3IiwiaXNzIjoidml2YSIsImlhdCI6MTczNTI4NTAzNCwiZXhwIjoxNzM1Mjg1OTM0fQ.qvH7QEHw3kul5171tK4ZaAtm7wdthnsCsKuBi5jOyIc"
headers = {"Authorization": f"Bearer {token}"}

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_notice_service(monkeypatch):
    mock_service = AsyncMock()
    monkeypatch.setattr(
        "server.infrastructure.di.container.ServerContainer.notice_service",
        lambda: mock_service
    )
    return mock_service

@pytest.fixture
def test_created_post(mock_notice_service):
    create_data = {
        "title": "Test Title",
        "content": "Test Content",
    }
    mock_notice_service.create_data.return_value = "new_post_id"
    
    response = TestClient(app).post("/posts", json=create_data, headers=headers)

    assert response.status_code == 200

    return {"post_id": response.json()}

@pytest.fixture
def test_created_post_error(mock_notice_service):
    create_data = {
        "title": "Test Title",
        "content": "Test Content",
    }
    mock_notice_service.create_data.return_value = "new_post_id"
    
    headers = {"Authorization": f"Bearer token"}
    response = TestClient(app).post("/posts", json=create_data, headers=headers)

    assert response.status_code == 401

    return {"post_id": response.json()}

def test_get_posts(client, mock_notice_service):
    mock_notice_service.get_all_datas.return_value = [
        {
            "id": "1",
            "title": "Test Title",
            "content": "Test Content",
            "user_id": 1,
            "created_at": datetime.now().isoformat(),
        }
    ]

    response = client.get("/posts")
    assert response.status_code == 200

def test_get_post(client, mock_notice_service, test_created_post):
    post_id = test_created_post["post_id"]
    assert post_id is not None, "post_id가 None입니다. test_create_notice를 먼저 실행하세요."

    mock_notice_service.get_data_by_data_id.return_value = {
        "id": post_id,
        "title": "Test Title",
        "content": "Test Content",
        "user_id": 1,
        "created_at": datetime.now().isoformat(),
    }
    response = client.get(f"/posts/{post_id}")
    assert response.status_code == 200

def test_update_post(client, mock_notice_service, test_created_post):
    post_id = test_created_post["post_id"]
    assert post_id is not None, "post_id가 None입니다. test_create_notice를 먼저 실행하세요."

    update_data = {
        "title": "Updated Title",
        "content": "Updated Content",
    }
    mock_notice_service.update_data_by_data_id.return_value = update_data
    response = client.put(f"/posts/{post_id}", json=update_data, headers=headers)
    assert response.status_code == 200


def test_update_post_error(client, mock_notice_service, test_created_post):
    post_id = test_created_post["post_id"]
    assert post_id is not None, "post_id가 None입니다. test_create_notice를 먼저 실행하세요."

    update_data = {
        "title": "Updated Title",
        "content": "Updated Content",
    }
    mock_notice_service.update_data_by_data_id.return_value = update_data

    headers = {"Authorization": f"Bearer token"}
    response = client.put(f"/posts/{post_id}", json=update_data, headers=headers)
    assert response.status_code == 401

def test_delete_post(client, mock_notice_service, test_created_post):
    post_id = test_created_post["post_id"]
    assert post_id is not None, "post_id가 None입니다. test_create_notice를 먼저 실행하세요."

    mock_notice_service.delete_data_by_data_id.return_value = 1
    response = client.delete(f"/posts/{post_id}", headers=headers)
    assert response.status_code == 200

def test_delete_post_error(client, mock_notice_service, test_created_post):
    post_id = test_created_post["post_id"]
    assert post_id is not None, "post_id가 None입니다. test_create_notice를 먼저 실행하세요."

    mock_notice_service.delete_data_by_data_id.return_value = 1

    headers = {"Authorization": f"Bearer token"}
    response = client.delete(f"/posts/{post_id}", headers=headers)
    assert response.status_code == 401
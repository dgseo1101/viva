from dotenv import load_dotenv
load_dotenv('_env/dev.env', override=True)

from datetime import datetime
import pytest
import pytest_asyncio
from httpx import AsyncClient
from httpx import ASGITransport
from unittest.mock import AsyncMock
import asyncio

from server.app import app
from server.application.services.users_service import UsersService
from core.application.dtos.auth_dto import (
    CreateAuthRequestDto,
    AuthResponseDto,
)
from server.application.dtos.auth_dto import (
    ResponseTokenDto,
    RefreshTokenRequestDto
)
from server.infrastructure.di.container import ServerContainer


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac


@pytest.fixture
def mock_users_service(monkeypatch):
    mock_service = AsyncMock(UsersService)
    monkeypatch.setattr(ServerContainer, 'users_service', mock_service)
    return mock_service


@pytest.mark.asyncio
async def test_signup(client, mock_users_service):
    mock_users_service.signup.return_value = AuthResponseDto(
        id=1,
        email="test_user",
        password_hash="mock_password_hash",
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat(),
    )

    create_data = CreateAuthRequestDto(email="test_user", password_hash="test_password")
    
    response = await client.post("/users/signup", json=create_data.model_dump())

    assert response.status_code == 200


@pytest_asyncio.fixture
async def test_login(client):
    login_data = CreateAuthRequestDto(email="hash_test", password_hash="password")
    
    response = await client.post("/users/login", json=login_data.model_dump())

    assert response.status_code == 200

    return response.json()


@pytest.mark.asyncio
async def test_refresh(client, test_login):
    refresh_token = test_login["refresh_token"] 
    refresh_data = RefreshTokenRequestDto(
        token=refresh_token
    )

    response = await client.post("/users/refresh", json=refresh_data.model_dump())

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_refresh_error(client):
    refresh_token = "refresh_token"
    refresh_data = RefreshTokenRequestDto(
        token=refresh_token
    )

    response = await client.post("/users/refresh", json=refresh_data.model_dump())

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_logout(client, mock_users_service, test_login):
    access_token = test_login["access_token"]
    mock_users_service.logout.return_value = 1

    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = await client.post("/users/logout", headers=headers)

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_logout_error(client):
    headers = {"Authorization": "Bearer access_token"}
    
    response = await client.post("/users/logout", headers=headers)

    assert response.status_code == 401
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from server.infrastructure.di.container import ServerContainer
from server.application.services.users_service import UsersService
from server.shard_kernel.auth_helper import validate_and_get_user_id

from core.application.dtos.auth_dto import (
    CreateAuthRequestDto,
    AuthResponseDto
)

from server.application.dtos.auth_dto import (
    ResponseTokenDto,
    RefreshTokenRequestDto,
    AccessTokenResponseDto
)

router = APIRouter()

@router.post("/users/signup", summary="회원가입", tags=["유저"])
@inject
async def signup(
    create_data: CreateAuthRequestDto,
    users_service: UsersService = Depends(Provide[ServerContainer.users_service]),
) -> AuthResponseDto:
    return await users_service.signup(create_data=create_data)

@router.post("/users/login", summary="로그인", tags=["유저"])
@inject
async def login(
    login_data: CreateAuthRequestDto,
    users_service: UsersService = Depends(Provide[ServerContainer.users_service]),
) -> ResponseTokenDto:
    return await users_service.login(login_data=login_data)

@router.post("/users/refresh", summary="refresh token", tags=["유저"])
@inject
async def refresh(
    refresh_token: RefreshTokenRequestDto,
    users_service: UsersService = Depends(Provide[ServerContainer.users_service]),
) -> AccessTokenResponseDto:
    return await users_service.refresh(refresh_token=refresh_token)

@router.post("/users/logout", summary="로그아웃", tags=["유저"])
@inject
async def logout(
    user_id: int = Depends(validate_and_get_user_id),
    users_service: UsersService = Depends(Provide[ServerContainer.users_service]),
) -> int:
    return await users_service.logout(user_id=user_id)
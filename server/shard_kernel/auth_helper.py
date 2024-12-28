# -*- coding: utf-8 -*-
from typing import Optional

import jwt
from dependency_injector.providers import Configuration
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Header, HTTPException

from core.infrastructure.di.container import CoreContainer
from server.application.services.users_service import UsersService
from server.infrastructure.di.container import ServerContainer


# JWT 토큰을 디코드하고 payload를 반환하는 함수
def decode_jwt_token(token: str, config: Configuration) -> dict:
    try:
        payload = jwt.decode(
            token, config["jwt"]["secret_key"], algorithms=[config["jwt"]["algorithm"]]
        )
        return payload
    except (jwt.ExpiredSignatureError, jwt.DecodeError):
        raise HTTPException(status_code=401, detail="Token is invalid or expired")


# 토큰에서 user_id를 추출하는 함수
@inject
async def get_user_id_by_token(token: str, config: Configuration) -> int:
    payload = decode_jwt_token(token, config)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token: user_id missing")
    return user_id


# Authorization 헤더에서 Bearer 토큰을 추출하는 함수
@inject
async def get_token_by_header_token(authorization: str, config: Configuration) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header is missing")

    try:
        token = authorization.split(" ")[1]  # "Bearer token"에서 token 추출
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid authorization format")

    decode_jwt_token(token, config)  # 토큰이 유효한지 검증
    return token


# 토큰을 검증하고 user_id를 반환하는 함수
@inject
async def validate_and_get_user_id(
    authorization: Optional[str] = Header(None),
    config: Configuration = Depends(Provide[CoreContainer.config]),
):
    token = await get_token_by_header_token(authorization=authorization, config=config)
    user_id = await get_user_id_by_token(token=token, config=config)
    return user_id

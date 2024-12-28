# -*- coding: utf-8 -*-
import logging
import datetime
from pytz import timezone
import jwt

from fastapi import HTTPException
from passlib.context import CryptContext

from dependency_injector.providers import Configuration
from core.application.services.base_service import BaseService
from core.application.dtos.auth_dto import (
    AuthResponseDto,
    CreateAuthRequestDto,
    UpdateAuthRequestDto,
)
from core.application.dtos.session_dto import CreateUserSessionRequestDto

from server.application.dtos.auth_dto import (
    ResponseTokenDto,
    RefreshTokenRequestDto,
    AccessTokenResponseDto
)

from server.infrastructure.repositories.session_repository import SessionRepository
from server.infrastructure.repositories.users_repository import UsersRepository


class UsersService(BaseService):
    def __init__(self, 
                 users_repository: UsersRepository,
                 session_repository: SessionRepository,
                 config: Configuration) -> None:
        super().__init__(base_repository=users_repository)
        self.logger = logging.getLogger(__name__)
        self.users_repository = users_repository
        self.session_repository = session_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        self.config = config

        self.jwt_secret_key = self.config["jwt"]["secret_key"]
        self.jwt_algorithm = self.config["jwt"]["algorithm"]
        self.service_name = self.config["service"]["name"]


    @property
    def create_dto(self):
        return CreateAuthRequestDto

    @property
    def response_dto(self):
        return AuthResponseDto

    @property
    def update_dto(self):
        return UpdateAuthRequestDto
    
    async def _create_access_token(self, user_id: int) -> str:
        payload = {
            "sub": str(user_id),
            "iss": self.service_name,
            "iat": datetime.datetime.now(timezone("Asia/Seoul")),
            "exp": datetime.datetime.now(timezone("Asia/Seoul"))
            + datetime.timedelta(minutes=15),
        }

        token = jwt.encode(payload, self.jwt_secret_key, algorithm=self.jwt_algorithm)

        return token

    async def _create_refresh_token(self, user_id: int) -> str:
        payload = {
            "sub": str(user_id),
            "iss": self.service_name,
            "iat": datetime.datetime.now(timezone("Asia/Seoul")),
            "exp": datetime.datetime.now(timezone("Asia/Seoul"))
            + datetime.timedelta(days=7),
        }

        refresh_token = jwt.encode(
            payload, self.jwt_secret_key, algorithm=self.jwt_algorithm
        )
        return refresh_token
    
    async def _decode_jwt_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token, self.config["jwt"]["secret_key"], algorithms=[self.config["jwt"]["algorithm"]]
            )
            return payload
        except (jwt.ExpiredSignatureError, jwt.DecodeError):
            raise HTTPException(status_code=401, detail="Token is invalid or expired")
        
    async def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    async def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
    
    async def signup(self, create_data: CreateAuthRequestDto):
        hashed_password = await self.hash_password(create_data.password_hash)

        create_data = CreateAuthRequestDto(
            email=create_data.email,
            password_hash=hashed_password
        )

        return await self.users_repository.create_data(create_data=create_data)

    async def login(self, login_data: CreateAuthRequestDto):
        user = await self.users_repository.exists_user_by_email(login_data=login_data)

        if user is None:
            raise HTTPException(status_code=401, detail="Invalid ID or Password")

        if not await self.verify_password(login_data.password_hash, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid ID or Password")

        user = await self.users_repository.get_data_by_email(email=login_data.email)

        access_token = await self._create_access_token(user_id=user.id)
        refresh_token = await self._create_refresh_token(user_id=user.id)

        session_create_data = CreateUserSessionRequestDto(
            user_id=user.id,
            token=refresh_token
        )

        await self.session_repository.create_data(create_data=session_create_data)

        return ResponseTokenDto(access_token=access_token, refresh_token=refresh_token)

    async def refresh(self, refresh_token: RefreshTokenRequestDto):
        exists_refresh_token = await self.session_repository.exists_refresh_token(refresh_token=refresh_token.token)

        if exists_refresh_token:
            refresh_token = await self._decode_jwt_token(token = refresh_token.token)
            access_token = await self._create_access_token(user_id=refresh_token.get("sub"))

            return AccessTokenResponseDto(token=access_token)
        else:
            raise HTTPException(status_code=401, detail="Invalid token")

    async def logout(self, user_id: int):
        await self.session_repository.delete_data_by_user_id(user_id=user_id)
        return 200
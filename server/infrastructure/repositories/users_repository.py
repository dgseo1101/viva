# -*- coding: utf-8 -*-
from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import exists

from core.infrastructure.database.models.user_model import UsersModel
from core.infrastructure.repositories.base_repository import BaseRepository
from core.application.dtos.auth_dto import CreateAuthRequestDto

from core.domain.entities.auth_entity import (
    AuthResponseEntity,
    CreateAuthRequestEntity,
    UpdateAuthRequestEntity,
)

SessionFactory = Callable[..., AbstractAsyncContextManager[AsyncSession]]


class UsersRepository(BaseRepository):
    def __init__(self, session: SessionFactory) -> None:
        self.session = session

    @property
    def model(self):
        return UsersModel  # 유저 엔티티를 반환

    @property
    def create_entity(self):
        # 여기에서 필요한 로직으로 엔티티를 생성할 수 있음
        return CreateAuthRequestEntity

    @property
    def return_entity(self):
        # 반환할 때 사용하는 DTO 또는 엔티티 정의
        return AuthResponseEntity

    @property
    def update_entity(self):
        # 업데이트 시 사용하는 엔티티나 로직
        return UpdateAuthRequestEntity
    
    async def exists_user_by_email(self, login_data: CreateAuthRequestDto):
        async with self.session() as session:
            stmt = select(UsersModel).where(UsersModel.email == login_data.email)
            result = await session.execute(stmt)
            data = result.scalars().first()

            if data:
                return AuthResponseEntity(**vars(data))
            
        return None
    
    async def get_data_by_email(self, email: str):
        async with self.session() as session:
            result = await session.execute(
                select(UsersModel).where(UsersModel.email == email)
            )
            data = result.scalars().first()
        
        return AuthResponseEntity(**vars(data))
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import Callable, Generic, List, Type, TypeVar

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.application.dtos.base import BaseRequest
from core.domain.entities.entity import Entity
from core.infrastructure.database.database import Base

SessionFactory = Callable[..., AbstractAsyncContextManager[AsyncSession]]

class BaseRepository(ABC):
    def __init__(self, session: SessionFactory) -> None:
        self.session = session

    @property
    @abstractmethod
    def model(self) -> Type[Base]:
        pass

    @property
    @abstractmethod
    def create_entity(self):
        pass

    @property
    @abstractmethod
    def return_entity(self):
        pass

    @property
    @abstractmethod
    def update_entity(self):
        pass

    async def create_data(self, create_data):
        async with self.session() as session:
            data = self.model(**create_data.model_dump(exclude_none=True))

            session.add(data)
            await session.commit()
            await session.refresh(data)

        return self.return_entity(**vars(data))

    async def create_datas(self, create_datas):
        async with self.session() as session:
            result = await session.execute(
                insert(self.model).values(
                    [
                        create_data.model_dump(exclude_none=True)
                        for create_data in create_datas
                    ]
                )
            )
            await session.commit()

            inserted_ids = [row[0] for row in result.inserted_primary_key_rows]

            result = await session.execute(
                select(self.model).where(self.model.id.in_(inserted_ids))
            )
            return [self.return_entity(**vars(data)) for data in result.scalars().all()]

    async def get_datas(self, page: int, page_size: int):
        async with self.session() as session:
            result = await session.execute(
                select(self.model).offset((page - 1) * page_size).limit(page_size)
            )
            datas = result.scalars().all()

        return [self.return_entity(**vars(data)) for data in datas]

    async def get_data_by_data_id(self, data_id: int):
        async with self.session() as session:
            result = await session.execute(
                select(self.model).filter(self.model.id == data_id)
            )
            data = result.scalar_one_or_none()

        return self.return_entity(**vars(data)) if data else None

    async def get_datas_by_data_id(self, data_id: int, page: int, page_size: int):
        async with self.session() as session:
            result = await session.execute(
                select(self.model)
                .filter(self.model.id == data_id)
                .offset((page - 1) * page_size)
                .limit(page_size)
            )
            datas = result.scalars().all()

        return [self.return_entity(**vars(data)) for data in datas]

    async def update_data_by_data_id(self, data_id: int, update_data):
        async with self.session() as session:
            result = await session.execute(
                select(self.model).filter(self.model.id == data_id)
            )
            data = result.scalar_one_or_none()

            if not data:
                return None

            for key, value in update_data.model_dump(exclude_none=True).items():
                setattr(data, key, value)

            await session.commit()
            await session.refresh(data)
            return self.return_entity(**vars(data))

    async def delete_data_by_data_id(self, data_id: int) -> None:
        async with self.session() as session:
            result = await session.execute(
                select(self.model).filter(self.model.id == data_id)
            )
            data = result.scalar_one_or_none()

            if data:
                await session.delete(data)
                await session.commit()

# -*- coding: utf-8 -*-
import logging

from core.application.services.base_service import BaseService
from core.application.dtos.notice_dto import (
    NoticeResponseDto,
    CreateNoticeRequestDto,
    UpdateNoticeRequestDto,
)
from server.infrastructure.repositories.notice_repository import NoticeRepository


class NoticeService():
    def __init__(self, notice_repository: NoticeRepository) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.notice_repository = notice_repository

    async def create_data(self, create_data: CreateNoticeRequestDto, user_id: int):
        return await self.notice_repository.create_data(create_data=create_data, user_id=user_id)
    
    async def get_all_datas(self, user_id=None, page = 1, page_size = 10):
        return await self.notice_repository.get_all_datas(user_id=user_id,
                                                          page=page,
                                                          page_size=page_size)
    
    async def get_data_by_data_id(self, data_id: str):
        return await self.notice_repository.get_data_by_data_id(data_id=data_id)
    
    async def update_data_by_data_id(self, data_id: str, update_data: UpdateNoticeRequestDto, user_id: int):
        return await self.notice_repository.update_data_by_data_id(data_id=data_id, update_data=update_data, user_id=user_id)
    
    async def delete_data_by_data_id(self, data_id: str, user_id: int):
        await self.notice_repository.delete_data_by_data_id(data_id=data_id, user_id=user_id)
        return 200
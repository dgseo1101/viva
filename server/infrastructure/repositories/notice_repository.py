# -*- coding: utf-8 -*-
from contextlib import AbstractAsyncContextManager
from typing import Callable
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException
from dependency_injector.providers import Configuration

from sqlalchemy.ext.asyncio import AsyncSession
from core.infrastructure.database.models.notice_model import NoticeModel
from core.domain.entities.notice_entity import (
    NoticeResponseEntity,
    CreateNoticeRequestEntity,
    UpdateNoticeRequestEntity,
)

from server.application.dtos.post_dto import UpdateNoticeResponseDto

SessionFactory = Callable[..., AbstractAsyncContextManager[AsyncSession]]


class NoticeRepository():
    def __init__(self,
                 config : Configuration) -> None:
        self.config = config
        self.client = MongoClient(self.config["mongodb"]["host"])  # MongoDB 주소
        self.db = self.client[self.config["mongodb"]["name"]]  # 데이터베이스 선택
        self.collection = self.db["posts"] 

    @property
    def model(self):
        return NoticeModel  # 유저 엔티티를 반환

    @property
    def create_entity(self):
        # 여기에서 필요한 로직으로 엔티티를 생성할 수 있음
        return CreateNoticeRequestEntity

    @property
    def return_entity(self):
        # 반환할 때 사용하는 DTO 또는 엔티티 정의
        return NoticeResponseEntity

    @property
    def update_entity(self):
        # 업데이트 시 사용하는 엔티티나 로직
        return UpdateNoticeRequestEntity
    
    async def create_data(self, create_data: CreateNoticeRequestEntity, user_id: int):
        post = {
            "title": create_data.title,
            "content": create_data.content,
            "user_id": user_id,
            "created_at": datetime.now(),
        }
        result = self.collection.insert_one(post)

        return str(result.inserted_id)

    async def get_all_datas(self, user_id=None, page = 1, page_size = 10):
        filter = {}
        if user_id:
            filter["user_id"] = str(user_id)

        skip = (page - 1) * page_size

        posts = self.collection.find(filter).skip(skip).limit(page_size)

        return [
            NoticeResponseEntity(**post, id=str(post["_id"])) for post in posts
        ]
    
    async def get_data_by_data_id(self, data_id: str):
        data_id = ObjectId(data_id)
        post = self.collection.find_one({"_id": data_id})

        return NoticeResponseEntity(**post, id=str(post["_id"]))
    
    async def update_data_by_data_id(self, data_id: str, update_data: UpdateNoticeRequestEntity, user_id: int):
        data_id = ObjectId(data_id)
        post = self.collection.find_one({"_id": data_id})

        if post["user_id"] == user_id:
            update_data = update_data.dict()
            update_data["user_id"] = user_id
            update_data["created_at"] = datetime.now()
        
            result = self.collection.update_one({"_id": data_id}, {"$set": update_data})

            return UpdateNoticeResponseDto(
                matched_count=result.matched_count,
                modified_count=result.modified_count,
                acknowledged=result.acknowledged,
                upserted_id=str(result.upserted_id) if result.upserted_id else None
            )
        else:
            raise HTTPException(status_code=401, detail="Invalid user")
    
    async def delete_data_by_data_id(self, data_id: str, user_id: int):
        data_id = ObjectId(data_id)
        post = self.collection.find_one({"_id": data_id})

        if post["user_id"] == user_id:
            result = self.collection.delete_one({"_id": data_id})
        else: 
            raise HTTPException(status_code=401, detail="Invalid user")

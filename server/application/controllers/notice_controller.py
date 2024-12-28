from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from server.infrastructure.di.container import ServerContainer
from server.application.services.notice_service import NoticeService
from server.shard_kernel.auth_helper import validate_and_get_user_id

from core.application.dtos.notice_dto import (
    CreateNoticeRequestDto,
    NoticeResponseDto,
    UpdateNoticeRequestDto
)

from server.application.dtos.post_dto import (
    UpdateNoticeResponseDto
)

router = APIRouter()

@router.post("/posts", summary="게시글 생성", tags=["게시판"])
@inject
async def create_notice(
    create_data: CreateNoticeRequestDto,
    user_id: int = Depends(validate_and_get_user_id),
    notice_service: NoticeService = Depends(Provide[ServerContainer.notice_service]),
) -> str:
    return await notice_service.create_data(user_id=user_id, create_data=create_data)

@router.get("/posts", summary="게시글 전체 조회", tags=["게시판"])
@inject
async def get_posts(
    user_id: int = None,
    page: int = 1,
    page_size: int = 10,
    notice_service: NoticeService = Depends(Provide[ServerContainer.notice_service]),
) -> List[NoticeResponseDto]:
    return await notice_service.get_all_datas(user_id=user_id, page=page, page_size=page_size)

@router.get("/posts/{post_id}", summary="특정 게시물 조회", tags=["게시판"])
@inject
async def get_post(
    post_id: str,
    notice_service: NoticeService = Depends(Provide[ServerContainer.notice_service]),
) -> NoticeResponseDto:
    return await notice_service.get_data_by_data_id(data_id=post_id)

@router.put("/posts/{post_id}", summary="특정 게시물 수정", tags=["게시판"])
@inject
async def get_post(
    post_id: str,
    update_data : UpdateNoticeRequestDto,
    user_id: int = Depends(validate_and_get_user_id),
    notice_service: NoticeService = Depends(Provide[ServerContainer.notice_service]),
) -> UpdateNoticeResponseDto:
    return await notice_service.update_data_by_data_id(
        data_id=post_id, update_data=update_data, user_id=user_id
    )

@router.delete("/posts/{post_id}", summary="게시물 삭제", tags=["게시파 "])
@inject
async def signup(
    post_id: str,
    user_id: int = Depends(validate_and_get_user_id),
    notice_service: NoticeService = Depends(Provide[ServerContainer.notice_service]),
) -> int:
    return await notice_service.delete_data_by_data_id(data_id=post_id, user_id=user_id)
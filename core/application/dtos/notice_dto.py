from datetime import datetime
from typing import Optional

from core.application.dtos.base import BaseRequest, BaseResponse

class CreateNoticeRequestDto(BaseRequest):
    title: str
    content: str

class UpdateNoticeRequestDto(BaseRequest):
    title: Optional[str] = None
    content: Optional[str] = None

class NoticeResponseDto(BaseResponse):
    id: str
    title: str
    content: str
    user_id: int 
    created_at: datetime
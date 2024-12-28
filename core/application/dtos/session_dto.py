from datetime import datetime

from core.application.dtos.base import BaseRequest, BaseResponse

class CreateUserSessionRequestDto(BaseRequest):
    user_id: int
    token: str


class UserSessionsResponseDto(BaseResponse):
    id: int
    user_id: int
    token: str
    created_at: datetime
from datetime import datetime
from typing import Optional

from core.application.dtos.base import BaseRequest, BaseResponse

class CreateAuthRequestDto(BaseRequest):
    email: str
    password_hash: str 

class UpdateAuthRequestDto(BaseRequest):
    email: Optional[str] = None
    password_hash: Optional[str] = None

class AuthResponseDto(BaseResponse):
    id: int
    email: str
    password_hash: str
    created_at: datetime
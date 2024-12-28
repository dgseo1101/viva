from typing import Optional
from core.application.dtos.base import BaseResponse

class UpdateNoticeResponseDto(BaseResponse):
    matched_count: int
    modified_count: int
    acknowledged: bool
    upserted_id: Optional[str] = None
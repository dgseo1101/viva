from datetime import datetime
from typing import Optional

from core.domain.entities.entity import Entity

class CreateNoticeRequestEntity(Entity):
    title: str
    content: str

class UpdateNoticeRequestEntity(Entity):
    title: str
    content: str

class NoticeResponseEntity(Entity):
    id: str
    title: str
    content: str 
    user_id: int
    created_at: datetime
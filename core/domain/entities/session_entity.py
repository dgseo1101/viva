from datetime import datetime
from typing import Optional

from core.domain.entities.entity import Entity

class CreateUserSessionRequestEntity(Entity):
    user_id: int
    token: str

class UserSessionResponseEntity(Entity):
    id: int
    user_id: int
    token: str
    created_at: datetime
from datetime import datetime
from typing import Optional

from core.domain.entities.entity import Entity

class CreateAuthRequestEntity(Entity):
    email: str
    password_hash: str 

class UpdateAuthRequestEntity(Entity):
    email: Optional[str] = None
    password_hash: Optional[str] = None

class AuthResponseEntity(Entity):
    id: int
    email: str
    password_hash: str
    created_at: datetime
    updated_at: datetime
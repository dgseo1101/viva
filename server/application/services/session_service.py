# -*- coding: utf-8 -*-
import logging

from core.application.services.base_service import BaseService
from core.application.dtos.session_dto import (
    UserSessionsResponseDto,
    CreateUserSessionRequestDto,
)
from server.infrastructure.repositories.session_repository import SessionRepository


class SessionService(BaseService):
    def __init__(self, session_repository: SessionRepository) -> None:
        super().__init__(base_repository=session_repository)
        self.logger = logging.getLogger(__name__)
        self.session_repository = session_repository

    @property
    def create_dto(self):
        return CreateUserSessionRequestDto

    @property
    def response_dto(self):
        return UserSessionsResponseDto
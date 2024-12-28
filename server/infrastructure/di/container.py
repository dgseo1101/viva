# -*- coding: utf-8 -*-

from core.infrastructure.di.container import CoreContainer
from server.infrastructure.repositories.notice_repository import NoticeRepository
from server.infrastructure.repositories.session_repository import SessionRepository
from server.infrastructure.repositories.users_repository import UsersRepository

from server.application.services.session_service import SessionService
from server.application.services.notice_service import NoticeService
from server.application.services.users_service import UsersService

from dependency_injector import providers

class ServerContainer(CoreContainer):
    users_repository = providers.Singleton(
        UsersRepository, session=CoreContainer.database.provided.session
    )

    session_repository = providers.Singleton(
        SessionRepository, session=CoreContainer.database.provided.session
    )

    notice_repository = providers.Singleton(
        NoticeRepository, config=CoreContainer.config
    )

    users_service = providers.Factory(
        UsersService,
        users_repository=users_repository,
        session_repository=session_repository,
        config=CoreContainer.config
    )

    session_service = providers.Factory(
        SessionService,
        session_repository=session_repository
    )

    notice_service = providers.Factory(
        NoticeService,
        notice_repository=notice_repository
    )


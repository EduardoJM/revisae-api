from uuid import UUID
from abc import ABC, abstractmethod

from domain.entities.subject import Subject
from application.interfaces.paginator_port import Page

class SubjectPort(ABC):
    @abstractmethod
    async def find_by_id(self, subject_id: UUID) -> Subject | None: ...

    @abstractmethod
    async def find_by_user_paginated(
        self,
        user_id: UUID,
        offset: int = 0,
        limit: int = 10,
        search: str = ''
    ) -> Page[Subject]: ...

    @abstractmethod
    async def save(self, subject: Subject) -> None: ...

    @abstractmethod
    async def delete(self, subject_id: UUID) -> None: ...

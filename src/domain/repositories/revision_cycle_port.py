from uuid import UUID
from abc import ABC, abstractmethod

from domain.entities.revision_cycle import RevisionCycle
from application.interfaces.paginator_port import Page

class RevisionCyclePort(ABC):
    @abstractmethod
    async def find_by_id(self, revision_cycle_id: UUID) -> RevisionCycle | None: ...

    @abstractmethod
    async def find_by_user_paginated(
        self,
        user_id: UUID,
        offset: int = 0,
        limit: int = 10,
        search: str = ''
    ) -> Page[RevisionCycle]: ...

    @abstractmethod
    async def save(self, revision_cycle: RevisionCycle) -> None: ...

    @abstractmethod
    async def delete(self, revision_cycle_id: UUID) -> None: ...

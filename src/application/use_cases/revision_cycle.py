from uuid import UUID, uuid4

from domain.entities.revision_cycle import RevisionCycle
from domain.repositories.revision_cycle_port import RevisionCyclePort
from domain.exceptions.revision_cycle import RevisionCycleNotFound
from domain.value_objects.hex_color import HexColor
from application.schemas.revision_cycle import (
    RevisionCycleOutput, CreateRevisionCycleInput, PaginatedRevisionCycleOutput,
    UpdateRevisionCycleInput
)

def _revision_cycle_to_output(revision_cycle: RevisionCycle) -> RevisionCycleOutput:
    return RevisionCycleOutput(
        id=revision_cycle.id,
        name=revision_cycle.name,
        days=revision_cycle.days,
        created_at=revision_cycle.created_at
    )

class CreateRevisionCycle:
    def __init__(
        self,
        revision_cycle_repo: RevisionCyclePort,
    ) -> None:
        self._revision_cycles = revision_cycle_repo

    async def execute(self, user_id: UUID, data: CreateRevisionCycleInput) -> RevisionCycleOutput:
        revision_cycle = RevisionCycle(
            revision_cycle_id=uuid4(),
            user_id=user_id,
            name=data.name,
            days=data.days,
        )
        await self._revision_cycles.save(revision_cycle)

        return _revision_cycle_to_output(revision_cycle)

class ListRevisionCycles:
    def __init__(self, revision_cycle_repo: RevisionCyclePort) -> None:
        self._revision_cycles = revision_cycle_repo

    async def execute(
        self,
        user_id: UUID,
        offset: int = 0,
        limit: int = 10,
        search: str = '',
    ) -> PaginatedRevisionCycleOutput:
        data = await self._revision_cycles.find_by_user_paginated(user_id, offset, limit, search)

        return PaginatedRevisionCycleOutput(
            results=[_revision_cycle_to_output(cycle) for cycle in data.results],
            total=data.total
        )

class GetRevisionCycle:
    def __init__(self, revision_cycle_repo: RevisionCyclePort) -> None:
        self._revision_cycles = revision_cycle_repo

    async def execute(self, user_id: UUID, revision_cycle_id: UUID) -> RevisionCycleOutput:
        revision_cycle = await self._revision_cycles.find_by_id(revision_cycle_id)
        if not revision_cycle:
            raise RevisionCycleNotFound(revision_cycle_id)
        if not revision_cycle.belongs_to(user_id):
            raise RevisionCycleNotFound(revision_cycle_id)
        return _revision_cycle_to_output(revision_cycle)

class UpdateRevisionCycle:
    def __init__(self, revision_cycle_repo: RevisionCyclePort) -> None:
        self._revision_cycles = revision_cycle_repo

    async def execute(self, user_id: UUID, revision_cycle_id: UUID, data: UpdateRevisionCycleInput) -> RevisionCycleOutput:
        revision_cycle = await self._revision_cycles.find_by_id(revision_cycle_id)
        if not revision_cycle:
            raise RevisionCycleNotFound(revision_cycle_id)
        if not revision_cycle.belongs_to(user_id):
            raise RevisionCycleNotFound(revision_cycle_id)
        
        revision_cycle.update(
            name=data.name,
            days=data.days
        )
        await self._revision_cycles.save(revision_cycle)
        return _revision_cycle_to_output(revision_cycle)

class DeleteRevisionCycle:
    def __init__(self, revision_cycle_repo: RevisionCyclePort) -> None:
        self._revision_cycles = revision_cycle_repo

    async def execute(self, user_id: UUID, revision_cycle_id: UUID) -> RevisionCycleOutput:
        revision_cycle = await self._revision_cycles.find_by_id(revision_cycle_id)
        
        if not revision_cycle:
            raise RevisionCycleNotFound(revision_cycle_id)
        if not revision_cycle.belongs_to(user_id):
            raise RevisionCycleNotFound(revision_cycle_id)
        
        await self._revision_cycles.delete(revision_cycle_id)

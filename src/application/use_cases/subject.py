from uuid import UUID, uuid4

from domain.entities.subject import Subject
from domain.repositories.subject_port import SubjectPort
from domain.exceptions.subject import SubjectNotFound
from domain.value_objects.hex_color import HexColor
from application.schemas.subject import (
    SubjectOutput, CreateSubjectInput, PaginatedSubjectOutput,
    UpdateSubjectInput
)

def _subject_to_output(subject: Subject) -> SubjectOutput:
    return SubjectOutput(
        id=subject.id,
        name=subject.name,
        color=str(subject.color),
        created_at=subject.created_at
    )

class CreateSubject:
    def __init__(
        self,
        subject_repo: SubjectPort,
    ) -> None:
        self._subjects = subject_repo

    async def execute(self, user_id: UUID, data: CreateSubjectInput) -> SubjectOutput:
        subject = Subject(
            subject_id=uuid4(),
            user_id=user_id,
            name=data.name,
            color=data.color,
        )
        await self._subjects.save(subject)

        return _subject_to_output(subject)

class ListSubjects:
    def __init__(self, subject_repo: SubjectPort) -> None:
        self._subjects = subject_repo

    async def execute(
        self,
        user_id: UUID,
        offset: int = 0,
        limit: int = 10,
        search: str = '',
    ) -> PaginatedSubjectOutput:
        data = await self._subjects.find_by_user_paginated(user_id, offset, limit, search)

        return PaginatedSubjectOutput(
            results=[_subject_to_output(subject) for subject in data.results],
            total=data.total
        )

class GetSubject:
    def __init__(self, subject_repo: SubjectPort) -> None:
        self._subjects = subject_repo

    async def execute(self, user_id: UUID, subject_id: UUID) -> SubjectOutput:
        subject = await self._subjects.find_by_id(subject_id)
        if not subject:
            raise SubjectNotFound(subject_id)
        if not subject.belongs_to(user_id):
            raise SubjectNotFound(subject_id)
        return _subject_to_output(subject)

class UpdateSubject:
    def __init__(self, subject_repo: SubjectPort) -> None:
        self._subjects = subject_repo

    async def execute(self, user_id: UUID, subject_id: UUID, data: UpdateSubjectInput) -> SubjectOutput:
        subject = await self._subjects.find_by_id(subject_id)
        if not subject:
            raise SubjectNotFound(subject_id)
        if not subject.belongs_to(user_id):
            raise SubjectNotFound(subject_id)
        
        subject.update(
            name=data.name,
            color=HexColor(data.color) if data.color else None,
        )
        await self._subjects.save(subject)
        return _subject_to_output(subject)

class DeleteSubject:
    def __init__(self, subject_repo: SubjectPort) -> None:
        self._subjects = subject_repo

    async def execute(self, user_id: UUID, subject_id: UUID) -> SubjectOutput:
        subject = await self._subjects.find_by_id(subject_id)
        
        if not subject:
            raise SubjectNotFound(subject_id)
        if not subject.belongs_to(user_id):
            raise SubjectNotFound(subject_id)
        
        await self._subjects.delete(subject_id)

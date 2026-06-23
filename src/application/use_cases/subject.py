from uuid import UUID, uuid4

from domain.entities.subject import Subject
from domain.repositories.subject_port import SubjectPort
from application.schemas.subject import SubjectOutput, CreateSubjectInput, PaginatedSubjectOutput

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

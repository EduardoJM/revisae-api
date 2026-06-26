from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends

from presentation.http_schemas.subject import (
    CreateSubjectRequest, SubjectResponse, PaginatedSubjectResponse, UpdateSubjectRequest
)
from application.schemas.subject import CreateSubjectInput, UpdateSubjectInput
from application.use_cases.subject import (
    CreateSubject, ListSubjects, GetSubject, DeleteSubject, UpdateSubject
)
from presentation.dependencies import get_current_user_id

router = APIRouter(
    prefix="/subjects",
    tags=["Subjects"],
    dependencies=[Depends(get_current_user_id)]
)


@router.post("/", response_model=SubjectResponse, status_code=201, summary="Create a new subject")
@inject
async def create_subject(
    body: CreateSubjectRequest,
    use_case: FromDishka[CreateSubject],
    user_id: UUID = Depends(get_current_user_id)
) -> SubjectResponse:
    result = await use_case.execute(
        user_id,
        CreateSubjectInput(
            name=body.name,
            color=body.color,
        )
    )
    print(result)
    return SubjectResponse.model_validate(result.model_dump())

@router.get("/", response_model=PaginatedSubjectResponse, status_code=201, summary="List subjects")
@inject
async def list_subject(
    use_case: FromDishka[ListSubjects],
    user_id: UUID = Depends(get_current_user_id),
    offset: int = 0,
    limit: int = 10,
    search: str = '',
) -> PaginatedSubjectResponse:
    result = await use_case.execute(user_id, offset, limit, search)
    return PaginatedSubjectResponse.model_validate(result.model_dump())

@router.get("/{subject_id}", response_model=SubjectResponse, summary="Get a single subject")
@inject
async def get_subject(
    subject_id: UUID,
    use_case: FromDishka[GetSubject],
    user_id: UUID = Depends(get_current_user_id),
) -> SubjectResponse:
    result = await use_case.execute(user_id, subject_id)
    return SubjectResponse.model_validate(result.model_dump())

@router.patch("/{subject_id}", response_model=SubjectResponse, summary="Update subject fields")
@inject
async def update_subject(
    subject_id: UUID,
    body: UpdateSubjectRequest,
    use_case: FromDishka[UpdateSubject],
    user_id: UUID = Depends(get_current_user_id),
) -> SubjectResponse:
    result = await use_case.execute(
        user_id,
        subject_id,
        UpdateSubjectInput(
            name=body.name,
            color=body.color,
        ),
    )
    return SubjectResponse.model_validate(result.model_dump())

@router.delete("/{subject_id}", status_code=204, summary="Delete a subject")
@inject
async def delete_subject(
    subject_id: UUID,
    use_case: FromDishka[DeleteSubject],
    user_id: UUID = Depends(get_current_user_id),
) -> None:
    await use_case.execute(user_id, subject_id)

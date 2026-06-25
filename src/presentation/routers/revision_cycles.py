from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends

from presentation.http_schemas.revision_cycle import (
    CreateRevisionCycleRequest, RevisionCycleResponse,
    PaginatedRevisionCycleResponse, UpdateRevisionCycleRequest
)
from application.schemas.revision_cycle import (
    CreateRevisionCycleInput, UpdateRevisionCycleInput
)
from application.use_cases.revision_cycle import (
    CreateRevisionCycle, ListRevisionCycles, GetRevisionCycle,
    DeleteRevisionCycle, UpdateRevisionCycle
)
from presentation.dependencies import get_current_user_id

router = APIRouter(
    prefix="/revision-cycles",
    tags=["Revision Cycles"],
    dependencies=[Depends(get_current_user_id)]
)


@router.post("/", response_model=RevisionCycleResponse, status_code=201, summary="Create a new revision cycle")
@inject
async def create_revision_cycle(
    body: CreateRevisionCycleRequest,
    use_case: FromDishka[CreateRevisionCycle],
    user_id: UUID = Depends(get_current_user_id)
) -> RevisionCycleResponse:
    result = await use_case.execute(
        user_id,
        CreateRevisionCycleInput(
            name=body.name,
            days=body.days
        )
    )
    return RevisionCycleResponse.model_validate(result.model_dump())

@router.get("/", response_model=PaginatedRevisionCycleResponse, status_code=201, summary="List revision cycles")
@inject
async def list_revision_cycles(
    use_case: FromDishka[ListRevisionCycles],
    user_id: UUID = Depends(get_current_user_id),
    offset: int = 0,
    limit: int = 10,
    search: str = '',
) -> PaginatedRevisionCycleResponse:
    result = await use_case.execute(user_id, offset, limit, search)
    return PaginatedRevisionCycleResponse.model_validate(result.model_dump())

@router.get("/{revision_cycle_id}", response_model=RevisionCycleResponse, summary="Get a single revision cycle")
@inject
async def get_revision_cycle(
    revision_cycle_id: UUID,
    use_case: FromDishka[GetRevisionCycle],
    user_id: UUID = Depends(get_current_user_id),
) -> RevisionCycleResponse:
    result = await use_case.execute(user_id, revision_cycle_id)
    return RevisionCycleResponse.model_validate(result.model_dump())

@router.patch("/{revision_cycle_id}", response_model=RevisionCycleResponse, summary="Update revision cycle fields")
@inject
async def update_revision_cycle(
    revision_cycle_id: UUID,
    body: UpdateRevisionCycleRequest,
    use_case: FromDishka[UpdateRevisionCycle],
    user_id: UUID = Depends(get_current_user_id),
) -> RevisionCycleResponse:
    result = await use_case.execute(
        user_id,
        revision_cycle_id,
        UpdateRevisionCycleInput(
            name=body.name,
            days=body.days,
        ),
    )
    return RevisionCycleResponse.model_validate(result.model_dump())

@router.delete("/{revision_cycle_id}", status_code=204, summary="Delete a revision cycle")
@inject
async def delete_revision_cycle(
    revision_cycle_id: UUID,
    use_case: FromDishka[DeleteRevisionCycle],
    user_id: UUID = Depends(get_current_user_id),
) -> None:
    await use_case.execute(user_id, revision_cycle_id)


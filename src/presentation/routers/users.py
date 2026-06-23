from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends

from presentation.http_schemas.user import RegisterUserRequest, UserResponse
from application.schemas.user import RegisterUserInput
from application.use_cases.user import RegisterUser, AuthenticatedUser
from presentation.dependencies import get_current_user_id

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponse, status_code=201, summary="Register a new user")
@inject
async def register_user(
    body: RegisterUserRequest,
    use_case: FromDishka[RegisterUser],
) -> UserResponse:
    result = await use_case.execute(
        RegisterUserInput(
            email=body.email,
            password=body.password,
            full_name=body.full_name,
        )
    )
    return UserResponse.model_validate(result.model_dump())

@router.get('/whoami', response_model=UserResponse, status_code=200, summary="Retrieve the authenticated user")
@inject
async def authenticated_user(
    use_case: FromDishka[AuthenticatedUser],
    user_id: UUID = Depends(get_current_user_id)
) -> UserResponse:
    result = await use_case.execute(user_id)
    return UserResponse.model_validate(result.model_dump())

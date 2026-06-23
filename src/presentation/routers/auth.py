from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter

from presentation.http_schemas.auth import LoginRequest, TokenResponse, RefreshRequest
from application.use_cases.auth import Login, RefreshTokens, Logout
from application.schemas.auth import LoginInput, RefreshInput

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse, summary="Obtain access and refresh tokens")
@inject
async def login(
    body: LoginRequest,
    use_case: FromDishka[Login],
) -> TokenResponse:
    result = await use_case.execute(LoginInput(email=body.email, password=body.password))
    return TokenResponse.model_validate(result.model_dump())


@router.post("/refresh", response_model=TokenResponse, summary="Rotate refresh token")
@inject
async def refresh(
    body: RefreshRequest,
    use_case: FromDishka[RefreshTokens],
) -> TokenResponse:
    result = await use_case.execute(RefreshInput(refresh_token=body.refresh_token))
    return TokenResponse.model_validate(result.model_dump())


@router.post("/logout", status_code=204, summary="Revoke refresh token")
@inject
async def logout(
    body: RefreshRequest,
    use_case: FromDishka[Logout],
) -> None:
    await use_case.execute(RefreshInput(refresh_token=body.refresh_token))

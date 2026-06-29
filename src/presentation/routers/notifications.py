from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends

from presentation.http_schemas.notification import (
    NotificationResponse, PaginatedNotificationResponse
)
from application.use_cases.notification import (
    GetNotification, ListNotifications, MarkNotificationAsReaded
)
from presentation.dependencies import get_current_user_id

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
    dependencies=[Depends(get_current_user_id)]
)

@router.get("/", response_model=PaginatedNotificationResponse, status_code=201, summary="List Notifications")
@inject
async def list_notifications(
    use_case: FromDishka[ListNotifications],
    user_id: UUID = Depends(get_current_user_id),
    offset: int = 0,
    limit: int = 10,
    search: str = '',
) -> PaginatedNotificationResponse:
    result = await use_case.execute(user_id, offset, limit, search)
    return PaginatedNotificationResponse.model_validate(result.model_dump())

@router.get("/{notification_id}", response_model=NotificationResponse, summary="Get a single notification")
@inject
async def get_notification(
    notification_id: UUID,
    use_case: FromDishka[GetNotification],
    user_id: UUID = Depends(get_current_user_id),
) -> NotificationResponse:
    result = await use_case.execute(user_id, notification_id)
    return NotificationResponse.model_validate(result.model_dump())

@router.put("/{notification_id}/read", response_model=NotificationResponse, summary="Mark a notification as readed")
@inject
async def mark_notification_readed(
    notification_id: UUID,
    use_case: FromDishka[MarkNotificationAsReaded],
    user_id: UUID = Depends(get_current_user_id),
) -> NotificationResponse:
    result = await use_case.execute(
        user_id,
        notification_id,
    )
    return NotificationResponse.model_validate(result.model_dump())

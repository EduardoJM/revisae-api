from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class NotificationOutput(BaseModel):
    id: UUID
    title: str
    description: str
    is_readed: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PaginatedNotificationOutput(BaseModel):
    results: list[NotificationOutput]
    total: int
    per_page: int

    model_config = ConfigDict(from_attributes=True)

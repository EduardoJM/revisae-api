from datetime import datetime
from uuid import UUID
from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict, AfterValidator

from domain.validators.revision_cycle_days import validate_revision_cycle_days


class CreateRevisionCycleRequest(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    days: list[Annotated[int, AfterValidator(validate_revision_cycle_days)]]

class UpdateRevisionCycleRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    days: list[Annotated[int, AfterValidator(validate_revision_cycle_days)]] | None = None

class RevisionCycleResponse(BaseModel):
    id: UUID
    name: str
    days: list[int]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PaginatedRevisionCycleResponse(BaseModel):
    results: list[RevisionCycleResponse]
    total: int

    model_config = ConfigDict(from_attributes=True)

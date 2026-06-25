from datetime import datetime
from uuid import UUID
from typing import Annotated

from pydantic import BaseModel, ConfigDict, AfterValidator

from domain.validators.revision_cycle_days import validate_revision_cycle_days


class CreateRevisionCycleInput(BaseModel):
    name: str
    days: list[Annotated[int, AfterValidator(validate_revision_cycle_days)]]

class UpdateRevisionCycleInput(BaseModel):
    name: str | None = None
    days: list[Annotated[int, AfterValidator(validate_revision_cycle_days)]] | None = None

class RevisionCycleOutput(BaseModel):
    id: UUID
    name: str
    days: list[int]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PaginatedRevisionCycleOutput(BaseModel):
    results: list[RevisionCycleOutput]
    total: int
    per_page: int

    model_config = ConfigDict(from_attributes=True)

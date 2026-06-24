from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CreateSubjectInput(BaseModel):
    name: str
    color: str # TODO: add validations

class UpdateSubjectInput(BaseModel):
    name: str | None = None
    color: str | None = None # TODO: add validations

class SubjectOutput(BaseModel):
    id: UUID
    name: str
    color: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PaginatedSubjectOutput(BaseModel):
    results: list[SubjectOutput]
    total: int

    model_config = ConfigDict(from_attributes=True)
